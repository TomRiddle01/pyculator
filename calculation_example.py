## This is an example file.
## Executing pyculator example_calculation.py will execute and edit this file.

from math import *


## Just applying variables
a = 3           # 3
b = sin(2)      # 0.9092974268256817

## Working with terms
a       # 3
a+b     # 3.909297426825682
2+2+2+2+2 # 10


## Calculate the normal vector

## Given a vector like
v = (100,20)

## We can calculate normal vector by first calculating its length
l = sqrt(v[0]**2 + v[1]**2) # 101.9803902718557

## And then dividing each number with the length
v_ = [x/l for x in v] # [0.9805806756909201, 0.19611613513818404]


a+b+2345+sin(3456)   # 2349.154841638403
