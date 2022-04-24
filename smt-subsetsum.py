from pysmt.shortcuts import Symbol, And, Or, Equals, Plus, Times, Int, get_model
from pysmt.typing import INT

#X = [4, 14, -6, 9, 1]
#T = 8

X = [-962, -855, -777, -751, -669, -441, -326, -321, -314, -307,
     -168, -166, -122, -51, -39, 4, 48, 142, 155, 193, 241, 257,
     324, 333, 334, 352, 359, 493, 823, 849, 878, 996]
T = -184
#T = 6411

# define a variable per element as an integer that is 0 or 1: do we include this element in the subset or not?
variables = [Symbol(str(i)+":"+str(x), INT) for i, x in enumerate(X)]

# we only want 0 or 1 as the domain
zero_or_one = And([Or(Equals(var, Int(0)), Equals(var, Int(1))) for var in variables])

# the sum of the subset should be T
subset_sum = Equals(Plus([Times(variables[i], Int(x)) for i, x in enumerate(X)]), Int(T))

formula = And(zero_or_one, subset_sum)

print(formula)
print("Number of variables:", len(variables))

import time
t = time.time()

model = get_model(formula)
if model:
    # prettyprint the solution
    first = True
    for i, x in enumerate(X):
        contains = model.get_value(variables[i]) == Int(1)
        if contains:
            if not first:
                print(" + ", sep="", end="")
            else:
                first = False
            
            if x >= 0:
                print(x, sep="", end="")
            else:
                print("(", x, ")", sep="", end="")
    print(" = ", T, sep="")
else:
    print("No solution found")


print(int(time.time() - t))