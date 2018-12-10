import re

file = open('input.txt','r')

lines = [line for line in file]

claims = dict()
conflicts = 0

def cells(x,y,w,h):
    cells = []
    for i in range(int(x), int(x) + int(w)):
        for j in range(int(y), int(y) + int(h)):
            cells.append((i,j))
    return cells


for line in lines:
    claim_id, x, y, w, h = re.match(r'#(\d*)\s@\s(\d*),(\d*):\s(\d*)x(\d*)',line).groups()
    for cell in cells(int(x),int(y),int(w),int(h)):
        claims[cell] = 1 if cell not in claims else claims[cell]+1
        if claims[cell] == 2:
            conflicts += 1

print(conflicts)

def isConflicted(claims, x, y, w, h):
    for cell in cells(x,y,w,h):
        if claims[cell] > 1:
            return True
    return False

for line in lines:
    claim_id, x, y, w, h = re.match(r'#(\d*)\s@\s(\d*),(\d*):\s(\d*)x(\d*)',line).groups()
    if not isConflicted(claims, x, y, w, h):
        print(claim_id)


