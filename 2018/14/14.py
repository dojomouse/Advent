recipes = "37"
#recipes = "37"
# add on to string the number as a string that results from combining the scores of the current recipes.
# next recipes are obtained by iterating through the score list by current_score+1
# first elf has first recipe, second elf has second recipe.
length = 825401

e1_idx = 0
e2_idx = 1
while len(recipes) < length+10:
    e1_current = int(recipes[e1_idx])
    e2_current = int(recipes[e2_idx])
    #print(e1_idx, e2_idx)
    #print(e1_current, e2_current)
    new = e1_current + e2_current
    recipes += str(new)
    #print(recipes)
    e1_idx = (e1_current + 1 + e1_idx) % len(recipes)
    e2_idx = (e2_current + 1 + e2_idx) % len(recipes)
    if len(recipes) % 100 == 0:
        print(len(recipes))

print(recipes[length:length+10])

while recipes.find("825401") == -1:
    for _ in range(10000):
        e1_current = int(recipes[e1_idx])
        e2_current = int(recipes[e2_idx])
        #print(e1_idx, e2_idx)
        #print(e1_current, e2_current)
        new = e1_current + e2_current
        recipes += str(new)
        #print(recipes)
        e1_idx = (e1_current + 1 + e1_idx) % len(recipes)
        e2_idx = (e2_current + 1 + e2_idx) % len(recipes)
        if len(recipes) % 100 == 0:
            print(len(recipes))
print(recipes.find("825401"))