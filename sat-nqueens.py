from pysat.solvers import Glucose4

n = 64 # n x n chessboard

# gather list of (!x || !y) clauses for each pair of squares x and y where a queen on x attacks square y (and the other way around)
clauses = []

def straight_line(x, y, dx, dy):
    index1 = 1 + x + n*y  # variable index, starts at 1
    x += dx
    y += dy
    while (x >= 0) and (y >= 0) and (x < n) and (y < n):
        index2 = 1 + x + n*y
        
        # because we don't want to add each pair (a, b) twice, only add (!a || !b) if a's index is smaller than b so we don't also add (!b || !a)
        if index1 < index2:
            clauses.append([-index1, -index2]) # negated because the variables are negated
        
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
        

# for each row, add a clause that at least one queen should be in this row
for y in range(n):
    clauses.append(list(range(1 + n*y, 1 + n*(y+1)))) # all n variables on the yth row

# add clauses to model
model = Glucose4()
for clause in clauses:
    model.add_clause(clause)

# count the number of clauses
clauses_count = len(clauses)
# also print every clause: no nice print(model) like with pysmt
for i, clause in enumerate(clauses):
    print("(", end="")
    for j, var in enumerate(clause):
        if var < 0:
            print("!", end="")
            var = -var
        print("'", var, "'", end="", sep="")
        if j != (len(clause) - 1):
            print(" & ", end="")
    print(")", end="")
    if i != (len(clauses)-1):
        print(" | ", end="")
    else:
        print("") # end line
print("Clauses:", clauses_count)


if model.solve():
    solution = model.get_model() # list like [1, -2, 3] to make variables 1 and 3 true, variable 2 negative
    # prettyprint the solution
    for y in range(n):
        for x in range(n):
            # if the index is in the list, there's a queen there, otherwise -index is in the list
            print("q" if ((1+x+n*y) in solution) else ".", sep="", end="")
        print("\n", sep="", end="")
else:
    print("No solution found")
