#Problem Set 0
#Write a program that does the following in order:
#    1. Asks the user to enter a number “x”
#    2. Asks the user to enter a number “y”
#    3. Prints out number “x”, raised to the power “y”.
#    4. Prints out the log (base 2) of “x”.

import numpy

x = float(input("Enter number x: "))
y = float(input("Enter number y: "))
power = x**y
print(str(x)+"^"+str(y)+" = ",power)
log = numpy.log2(x)
print("log"+str(x)+" = ", log)