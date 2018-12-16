file = open('input.txt','r')

def update(state_c, predictors):
    state_n = set()
    first = min(state_c) - 2 # No need to eval any idx earlier than this, window guaranteed to be all empty.
    last = max(state_c) + 2 # No need to eval any idx later than this, per above.
    for idx in range(first, last + 1):
        patch = ''.join(["#" if idx + k in state_c else "." for k in range(-2, 3)])
        if patch in predictors:
            state_n.add(idx)
    return state_n
        
predictors = set()
state_c = set()

for idx, line in enumerate(file):
    line = line.split()
    if idx == 0:
        state_c = {i for i, val in enumerate(line[2]) if val == "#"}
    if idx > 1 and line[2] == "#":
        predictors.add(line[0])

#part1
for gen in range(20):
    state_c = update(state_c, predictors)

print(sum(state_c))

#part2
for gen in range(2000):
    prev_sum = sum(state_c)
    state_c = update(state_c, predictors)
    print(f'Gen: {20 + gen}')
    print(f'Sum: {sum(state_c)}')
    print(f'Delta: {sum(state_c)-prev_sum}')

