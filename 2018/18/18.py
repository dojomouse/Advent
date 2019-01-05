from collections import Counter

def adjacentCount(grid, loc):
    return Counter([grid.get((x,y)) for x in [loc[0]-1, loc[0], loc[0]+1] for y in [loc[1]-1, loc[1], loc[1]+1] if ((x,y) != loc and grid.get((x,y)) is not None)])


def stringify(grid):
    line = ''
    for y in range(ymax+1):
        for x in range(xmax+1):
            line += grid[(x,y)]
        line += '\n'
    return line

def projected_equivalent(total_minutes, first_seen, next_seen):
    return (total_minutes - first_seen) % (next_seen - first_seen) + first_seen

            
old_grids = dict()
old_values = []

grid = dict()

xmax, ymax = None, None

with open('input.txt','r') as f:
    for y, line in enumerate(f):
        line.rstrip()
        ymax = y
        for x, cell in enumerate(line):
            grid[(x,y)] = cell
            xmax = x

# open becomes trees if adjacent has 3 or more trees, otherwise stays open

# trees become lumber if three or more adjacent are lumber, otherwise nothing

# lumber remains lumber if at least one adjacent lumber and at least one adjacent trees. Otherwise, becomes open.

# resource = wood * lumber

OPEN = '.'
TREE = '|'
YARD = '#'

minutes = 1000000000

print("Initial state:")
print(stringify(grid))

for minute in range(1,minutes+1):
    new_grid = dict()
    for cell, content in grid.items():
        adjacent_count = adjacentCount(grid, cell)
        if content == OPEN:
            new_grid[cell] = TREE if adjacent_count[TREE] >= 3 else OPEN
        elif content == TREE:
            new_grid[cell] = YARD if adjacent_count[YARD] >= 3 else TREE
        elif content == YARD:
            new_grid[cell] = YARD if adjacent_count[YARD] >= 1 and adjacent_count[TREE] >= 1 else OPEN
    grid = new_grid
    counts = Counter(grid.values())
    value = counts[TREE] * counts[YARD]
    old_values.append(value)
    grid_string = stringify(grid)
    exists = old_grids.get(grid_string)
    if exists:
        print("Grid from minute {} repeated at minute {}".format(exists, minute))
        print("Projected final value: {}".format(old_values[projected_equivalent(minutes, exists, minute)]))
        break
    old_grids[grid_string] = minute
    print("After {} minutes: {}".format(minute,value))
    #print(stringify(grid))