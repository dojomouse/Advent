file = open('input.txt','r')
count_2 = 0
count_3 = 0

def CountCheck(box_id, count):
    occurrences = dict()
    for char in box_id:
        occurrences[char] = occurrences.get(char,0) + 1
    for val in occurrences.values():
        if val == count:
            return True
    return False

for box_id in file:
    count_2 += 1 if CountCheck(box_id,2) else 0
    count_3 += 1 if CountCheck(box_id,3) else 0

print("Checksum is: {}".format(count_2 * count_3))