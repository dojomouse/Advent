# Store the change points /\+ with coordinates in track, a dict keyed on coords.
# Store the carts <>^v with coordinates in carts. Need to iterate over carts in defined order, probably custom sort function.

import numpy as np

class Cart:
    def __init__(self, x, y, icon):
        self.position = np.array([x,y])
        dir_for_icon = {
            '>': [1,0],
            '<': [-1,0],
            '^': [0,-1],
            'v': [0,1]
        }
        self.orientation = np.array(dir_for_icon[icon])
        self.alive = True
        self.turn_state = 0

    def turn_left(self):
        r_matrix_left = np.array([[0,1],[-1,0]])
        self.orientation = np.matmul(r_matrix_left, self.orientation)

    def turn_right(self):
        r_matrix_right = np.array([[0,-1],[1,0]])
        self.orientation = np.matmul(r_matrix_right, self.orientation)

    def move(self):
        self.position += self.orientation
    
    def turn(self, cell):
        if cell == None:
            return
        if cell == "/":
            if self.orientation[0] == 0:
                self.turn_right()
            else:
                self.turn_left()
        if cell == "\\":
            if self.orientation[0] == 0:
                self.turn_left()
            else:
                self.turn_right()
        if cell == "+":
            if self.turn_state % 3 == 0:
                self.turn_left()
            if self.turn_state % 3 == 2:
                self.turn_right()
            self.turn_state += 1

track = dict()

carts = []

#init
with open('input.txt','r') as file:
    for y, line in enumerate(file):
        line = line.rstrip()
        for x, char in enumerate(line):
            if char in "<>^v":
                carts.append(Cart(x,y,char))
            elif char in "/\+":
                track[(x,y)] = char

# Simulate and record crashes.
last_cart = False
while not last_cart:
    # sort carts by location
    #print([cart.position for cart in carts if cart.alive])
    carts.sort(key = lambda c: (c.position[1], c.position[0]))
    #print([cart.position for cart in carts])
    for idx, cart in enumerate(carts):
        if cart.alive == False:
            continue
        cart.move()
        # test for crash
        for other_idx, other_cart in enumerate(carts):
            if idx == other_idx or other_cart.alive == False:
                continue
            if np.array_equal(cart.position, other_cart.position):
                cart.alive = False
                other_cart.alive = False
                print("Crash at: {}".format(cart.position))


        # update orienation based on track
        cart.turn(track.get((cart.position[0],cart.position[1])))
    
    active_carts = [cart for cart in carts if cart.alive]
    if len(active_carts) < 2:
        print("Final cart at: {}".format([cart.position for cart in active_carts]))
        last_cart = True