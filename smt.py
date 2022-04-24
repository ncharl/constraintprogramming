from pysmt.shortcuts import Symbol, And, GE, LE, Equals, Plus, Times, Int, get_model
from pysmt.typing import INT

# define two integers a and b
letters = [Symbol("a", INT), Symbol("b", INT)]
# both integers should be between 0 and 100: 0 <= a, b <= 100
domains = And([GE(letters[0], Int(0)), GE(letters[1], Int(0)), LE(letters[0], Int(100)), LE(letters[1], Int(100))])
# we want a*a + b*b to be 4181
problem = Equals(Plus(Times(letters[0], letters[0]), Times(letters[1], letters[1])), Int(4181))

formula = And(domains, problem)
print(formula)

model = get_model(formula)
if model:
    print(model)
else:
    print("No solution found")