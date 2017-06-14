#!/usr/bin/env python3
import sys
import os
import re
import json
import tempfile
import signal
from subprocess import Popen, PIPE, call


EDITOR = os.environ.get('EDITOR', 'vim')


def signal_handler(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


class Pyculate:

    def execute(filename):

        print("Executing", filename)

        processedFile = """
import atexit
import json

traces = dict()

def exit_handler():
    print(json.dumps(traces))

atexit.register(exit_handler)

def trace(linenumber, result):
    if not linenumber in traces:
        traces[linenumber] = []
    traces[linenumber].append(result)
"""

        lines = list()
        with open(filename, 'r') as myfile:
            lines = myfile.readlines()

        i = -1
        for line in lines:
            i += 1
            m = re.match("([\t ]*)([^\#]*)\#()(?!\#)(.*)", line)
            if m:
                tabs = m.group(1)
                code = m.group(2)
                processedFile += "%s_ = %s;trace(%d, _)#>\n" % (tabs, code, i)
            else:
                processedFile += line

        print("Running...")
        p = Popen(['python3'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (stdout_data, stderr) = p.communicate(input=processedFile.encode())

        try:
            traces = dict()
            traces = json.loads(stdout_data.split(b"\n")[-2].decode())
        except ValueError as e:
            print("Tracing failed")
            traces = dict()

        j = -1
        for line in lines:
            j += 1
            i = str(j)
            m = re.match("([^\#]*\#(?!\#)).*", line)
            if m:
                r = ""
                if i in traces:

                    def sanitize(s):
                        s = str(s)
                        s = s.replace("\n", "\\n")
                        s = s.replace("\r", "\\n")
                        return s


                    if len(traces[i]) > 6:
                        boundary = traces[i][:3]+["..."] + traces[i][-3:]
                        r = ", ".join(sanitize(a) for a in boundary)
                    else:
                        r = ", ".join(sanitize(a) for a in traces[i][:3])
                lines[j] = "%s %s\n" % (m.group(1), r)

        return ("".join(lines), stderr.decode())

    def execution_loop(filename):

        while True:
            call([EDITOR, filename])
            (newContent, stderr) = Pyculate.execute(filename)

            if len(stderr) > 0:
                print(stderr)

            input("Press enter to edit again. Ctrl+c to quit.")

            if newContent == "":
                exit()

            with open(filename, "w") as file:
                file.write(newContent)


# Run with temporary file
if len(sys.argv) == 1:
    initial_message = "import numpy, sympy\nfrom math import *\n\n\n\n\n\n"

    with tempfile.NamedTemporaryFile(suffix=".pyculator.py") as tf:
        tf.write(initial_message.encode())
        tf.flush()
        Pyculate.execution_loop(tf.name)


# Run with the file given as a parameter
if len(sys.argv) == 2:
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        exit("Invalid File")

    Pyculate.execution_loop(filename)