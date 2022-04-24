from pysmt.shortcuts import Symbol, And, Or, Equals, Plus, Times, Int, get_model
from pysmt.typing import INT

n = 64 # n x n chessboard

# one variable per square
variables = [Symbol(str(i), INT) for i in range(n*n)]

# constraint that we want exactly n queens
n_queens = Equals(Plus(variables), Int(n))

# because of the previous constraint we have to use integers instead of booleans, so we only want 0 or 1 as the domain
zero_or_one = [Or(Equals(var, Int(0)), Equals(var, Int(1))) for var in variables]


# gather list of (x*y == 0) for each pair of squares x and y where a queen on x attacks square y (and the other way around)
no_attacks = []

def straight_line(x, y, dx, dy):
    index1 = x + n*y  # variable index
    x += dx
    y += dy
    while (x >= 0) and (y >= 0) and (x < n) and (y < n):
        index2 = x + n*y
        
        # because we don't want to add each pair (a, b) twice, only add (a*b == 0) if a's index is smaller than b so we don't also add (b*a == 0)
        if index1 < index2:
            no_attacks.append(Equals(Times(variables[index1], variables[index2]), Int(0)))
        
        x += dx
        y += dy

for x in range(n):
    for y in range(n):
        # find out all squares a queen on (x, y) would attack by checking the 8 lines of attack
        straight_line(x, y, 1, 0)
        straight_line(x, y, -1, 0)
        straight_line(x, y, 1, 1)
        straight_line(x, y, -1, 1)
        straight_line(x, y, 1, -1)
        straight_line(x, y, -1, -1)
        straight_line(x, y, 0, 1)
        straight_line(x, y, 0, -1)
        
                
# count the number of clauses
clauses_count = 1 + len(no_attacks) + len(zero_or_one)

# combine all constraints
formula = And(n_queens, And(no_attacks), And(zero_or_one))
print(formula)
print("Clauses:", clauses_count)

model = get_model(formula)
if model:
    # prettyprint the solution
    for y in range(n):
        for x in range(n):
            print("q" if model.get_value(variables[x+n*y]) == Int(1) else ".", sep="", end="")
        print("\n", sep="", end="")
else:
    print("No solution found")
