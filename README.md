# Pyculator - python-based calculator

**DISCLAIMER:** Please be careful when using this tool. It is only a small script executing foreign code. Only run your own python code.


Pyculator is a small script that runs other python scripts and outputs intermediate results into the source code.

This enables you to make complex caltulations and repeat these by editing the code again.

[![asciicast](https://asciinema.org/a/5bwbed0is2306d02xacmga6nx.png)](https://asciinema.org/a/5bwbed0is2306d02xacmga6nx)

## Usage

Run pyculator with `./pyculator calculation_example.py` to open an existing file or omit the filename and just run `./pyculator` to use a temporary file. 
The latter is useful if you want to use this as an on-the-fly calculator.
Pyculator will use the editor in your `EDITOR` environment variable.

Write some python code with multiple steps like:

    from math import *

    a = sin(2) #
    b = 5

    a + b #

    for i in range(20):
        i*2

Every line ending with a # will be traced by calculator and the results will be inserted as a comment.

Save the file and close the editor. Pyculator will execute the file, print errors and reopen the editor (after pressing enter).

The file now looks like this.


    a = sin(2) # 0.9092974268256817
    b = 5

    a + b # 5.909297426825682

    for i in range(20):
        i*2 # 0, 2, 4, ..., 34, 36, 38


Lines that are executed multiple times will omit some values to save space. You can write them to a list if you need all values.


