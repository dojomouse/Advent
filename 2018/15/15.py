# Actions in reading order

# Unit starts turn by identifying targets; end if no targets.

# ID open squares in range of targets; being those immediately adjacent

# If unit not in range, and no open squares in range, end turn

# If in range; attack

# If not in range, move

def neighbours(loc):
    #return [{'location': (x, y), 'content': cave.get((x,y))} for x,y in [[loc[0]-1, loc[1]],[loc[0]+1, loc[1]],[loc[0], loc[1]-1],[loc[0], loc[1]+1]] if cave.get((x,y)) is not None ]
    return [(x, y) for x,y in [[loc[0]-1, loc[1]],[loc[0]+1, loc[1]],[loc[0], loc[1]-1],[loc[0], loc[1]+1]] if cave.get((x,y)) is not None ]



class Node:
    def __init__(self, location, cost, prev):
        self.location = location
        self.cost = cost
        self.prev = prev

class Unit:
    def __init__(self, x, y, team, elf_power = 3):
        self.attack_power = 3 if team == "G" else elf_power
        self.hit_points = 200
        self.team = team
        self.location = (x,y)
    
    def find_best_move(self, cave):
        origin_node = Node(self.location, 0, None)
        explored = []
        frontier = [origin_node]
        target = "G" if self.team == "E" else "E"
        blocked = "#" + self.team
        while True:
            frontier.sort(key=lambda n: (n.cost, n.location[1], n.location[0]), reverse=True)
            if len(frontier) == 0:
                return origin_node
            #print([(node.location, node.cost) for node in frontier])
            expand_node = frontier.pop()
            #print(expand_node.location)
            explored.append(expand_node)
            for neighbour in neighbours(expand_node.location):
                # Incremental cost is always 1. Anything already in explored will have been reached by shortest path given frontier ordering
                # We don't go through walls or teammates
                if neighbour not in (node.location for node in explored + frontier) and cave[neighbour] not in blocked:
                    # If it's a goal, then should also be best goal via best path
                    # assuming exploration order is correct
                    if cave[neighbour] == target:
                        # iterate back up the expand_node.prev chain to the first move, otherwise add to frontier
                        current = expand_node
                        while current.prev != origin_node and current != origin_node:
                            current = current.prev
                        # one the origin is the node that precedes current, move to current by replacing unit location with a '.'
                        # updating unit location to current, and changing the new location in the cave to an team icon.
                        return current
                    else:
                        frontier.append(Node(neighbour, expand_node.cost + 1, expand_node))
    def move(self, cave, dest):
        cave[self.location] = "."
        self.location = dest.location
        cave[self.location] = self.team

        # Consider all open squares in range of targets, determine which could be reached in fewest steps
        # Break ties based on reading order
        # Reachability is based on CURRENT position of other units only
        # If no open path to any squares in range, end turn.
        # Take a single step along shorest path to closest square.
        # If multiple steps along shortest path, pick the first in reading order.

    def attack(self, creatures, cave):
        target_type = "G" if self.team == "E" else "E"
        targets = [target for target in filter(lambda c: (c.team == target_type and c.hit_points > 0 and c.location in neighbours(self.location)), creatures)]
        #print(targets)
        if len(targets) > 0:
            targets.sort(key=lambda t: (t.hit_points, t.location[1], t.location[0]))
            target = targets[0]
            target.take_hit(self.attack_power)
            if target.hit_points <= 0:
                cave[target.location] = '.'
                #print("Target of type {} at {} died".format(target.team, target.location))


        # determine all targets in range
        # select target with fewest hit points
        # in case of tie, first in reading order
        # Unit attack reduces targets hit points by attack_power. If 0 or less, unit dies and is replaced by a '.'
    def take_hit(self, attack_power):
        self.hit_points = max(0, self.hit_points - attack_power)

def fight(creatures, cave):
    rounds = 0
    while True:
        #print("Round starts")
        #print("Round number: {}".format(rounds))
        creatures.sort(key = lambda u: (u.location[1],u.location[0]))
        #print([(c.location, c.hit_points) for c in creatures if c.hit_points > 0])
        #print_cave(cave)
        #input("Press Enter to continue...")
        for idx, creature in enumerate(creatures):
            if idx == len(creatures)-1:
                rounds += 1
            if creature.hit_points <= 0:
                continue
            #print(creature.location)
            creature.move(cave, creature.find_best_move(cave))
            creature.attack(creatures, cave)
            if (len([unit for unit in creatures if (unit.team == "E" and unit.hit_points > 0)]) == 0 or
                    len([unit for unit in creatures if (unit.team == "G" and unit.hit_points > 0)]) == 0):
                
                #print([(c.location, c.hit_points, c.team) for c in creatures if c.hit_points > 0])
                return rounds

def score(rounds, creatures):
    hp_sum = sum(c.hit_points for c in creatures)
    print(rounds)
    print(hp_sum)
    return rounds * hp_sum

def print_cave(cave):
    line = 0
    print(" 0 ", end='')
    for key, val in cave.items():
        if key[1] > line:
            line += 1
            print("{0: >2} ".format(key[1]), end='')
            #print()
        print(val, end='')
    print()
    print()


cave = dict()
creatures = []

def env_init(elf_power = 3):
    cave = dict()
    creatures = []
    with open('input.txt','r') as file:
        for y, line in enumerate(file):
            line.rstrip()
            for x, cell in enumerate(line):
                cave[(x,y)] = cell
                if cell in "GE":
                    creatures.append(Unit(x,y,cell,elf_power))
    return cave, creatures

# Part 1
cave, creatures = env_init()
rounds = fight(creatures, cave)
print(score(rounds, creatures))

# Part 2

total_elves = len([unit for unit in creatures if unit.team == "E"])
max_power_lose = 3
# Will be faster if we guess an initial max power that's not too high
# Try a multiplier of twice the magnitude by which elves are outnumbered.
min_power_win = len([unit for unit in creatures if unit.team == "G"]) / total_elves * 2 * 3
test_power = min_power_win

while True:
    cave, creatures = env_init(test_power)
    rounds = fight(creatures, cave)
    print(score(rounds, creatures))
    surviving_elves = len([unit for unit in creatures if (unit.team == "E" and unit.hit_points > 0)])
    if surviving_elves < total_elves:
        print("{} elves died with power: {}".format(total_elves - surviving_elves, test_power))
        max_power_lose = max(test_power, max_power_lose)
        if min_power_win <= max_power_lose: # in case our initial min_power_win guess is too low.
            min_power_win *= 2
        test_power = max_power_lose + max(1,(min_power_win - max_power_lose) // 2)
    else:
        print("All elves survived with power: {}".format(test_power))
        min_power_win = test_power
        test_power = max_power_lose + (min_power_win - max_power_lose) // 2
    print('Max power lose: {}'.format(max_power_lose))
    print('Min power win: {}'.format(min_power_win))
    print('Power delta: {}'.format(min_power_win - max_power_lose))
    if min_power_win - max_power_lose == 1:
        print("Lowest power to win: {}".format(min_power_win))
        break