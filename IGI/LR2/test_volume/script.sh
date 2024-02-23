#! /usr/bin/python3

import square
import circle
import os

print('circle area: ', circle.area(float(os.environ['CIRCLE_R'])));
print('circle perimeter: ', circle.area(float(os.environ['CIRCLE_R'])));

print('square area: ', square.area(float(os.environ['SQUARE_A'])));
print('square perimeter: ', square.area(float(os.environ['SQUARE_A'])));

file = open("./test.txt", "w")
file.write("file created by container")
file.close()

print(os.getcwd())

quit()
