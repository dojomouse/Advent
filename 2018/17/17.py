import re
import sys
# Start with the spring, flow through the whole environment, cell value always depends on below, left, and right cell values.

# If below is at rest or clay, propagate left+right

def renderSlice():
    print()
    for y in range(0,ymax + 1):
        line = ""
        for x in range(xmin - 2, xmax + 3):
            if (x,y) in clay:
                line += "#"
            elif (x,y) in settled:
                line += "~"
            elif (x,y) in water:
                line += "|"
            else:
                line += "."
        print(line)

    print()


def offset(origin, direction):
    return((origin[0] + direction[0], origin[1] + direction[1]))

def fill(loc, direction):
    '''Water enters loc, flowing in direction, with follow on effects'''
    water.add(loc)
    below = offset(loc, (0,1))
    if below not in clay | water and below[1] <= ymax:
        # Try to fill up below
        fill(below, (0,1))

    if below not in clay | settled:
        # Given we've now tried to fill below, if we've failed it's a drain point; we'll never fill loc
        return False

    left = offset(loc, (-1, 0))
    right = offset(loc, (1,0))

    Left_Full = left in clay or left not in water and fill(left, (-1,0))
    Right_Full = right in clay or right not in water and fill(right, (1,0))

    if direction == (0,1) and Left_Full and Right_Full:
        settled.add(loc)

        while left in water:
            settled.add(left)
            left = offset(left, (-1,0))

        while right in water:
            settled.add(right)
            right = offset(right, (1,0))
    
    return (loc in settled) or \
            (direction == (-1,0) and Left_Full) or \
            (direction == (1,0) and Right_Full)

clay = set()
water = set()
settled = set()

with open('input.txt', 'r') as f:
    for line in f:
        axis1, r1, axis2, r2, r3 = re.match(r'([a-z])\=(\d+)\,\s([a-z])\=(\d+)\.\.(\d+)',line).groups()
        r1, r2, r3 = [int(x) for x in [r1, r2, r3]]
        for a2_ind in range(r2, r3+1):
            x = r1 if axis1 is 'x' else a2_ind
            y = r1 if axis1 is 'y' else a2_ind
            clay.add((x,y))

ymin  = min(clay, key = lambda x: x[1])[1]
ymax  = max(clay, key = lambda x: x[1])[1]
xmin  = min(clay, key = lambda x: x[0])[0]
xmax  = max(clay, key = lambda x: x[0])[0]

print("Ymin: {}".format(ymin))
print("Ymax: {}".format(ymax))

print(sys.getrecursionlimit())
sys.setrecursionlimit(5000)

#renderSlice()


# Start with spring
spring = (500,0)
fill(spring, (0,1))

#print("After fill")

#renderSlice()

print("Number of squares with water in them within range is: {}".format(len([w for w in water if ymin <= w[1] <= ymax])))
print("Number of squares with water in them within range after spring runs dry is: {}".format(len([w for w in settled if ymin <= w[1] <= ymax])))

