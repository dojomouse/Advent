#Find the fuel cell's rack ID, which is its X coordinate plus 10.
#Begin with a power level of the rack ID times the Y coordinate.
#Increase the power level by the value of the grid serial number (your puzzle input).
#Set the power level to itself multiplied by the rack ID.
#Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
#Subtract 5 from the power level.

# 9798

# 300 x 300 grid

import numpy as np

x_range = 300
y_range = 300
grid_serial = 9798

cells = np.zeros([x_range, y_range])

def calc_power(x,y):
    rack_id = x + 10
    power = rack_id * y
    power += grid_serial
    power *= rack_id
    if len(str(power)) < 3:
        return 0
    power = str(power)[-3]
    power = int(power) - 5
    return power

for x in range(x_range):
    for y in range(y_range):
        cells[x][y] = calc_power(x,y)

best_power = -100000000
best_params = None
for size in range(300):
    for x in range(0, x_range-size):
        for y in range(0, y_range-size):
            this_power = cells[x:x+size, y:y+size].sum()
            if this_power > best_power:
                best_params = (x, y, size)
                best_power = this_power
    print("size: {}".format(size))
    print(best_params)

