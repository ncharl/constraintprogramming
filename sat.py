from pysat.solvers import Glucose4

model = Glucose4()
model.add_clause([1]) # a
model.add_clause([2, 3, -1]) # b, c, !a

if model.solve():
    print(model.get_model())
else:
    print("No solution found")