file = open('input.txt','r')

lines = [line for line in file]
print(lines)

def difference(s1, s2):
    max_len = min(len(s1), len(s2))
    diff = abs(len(s1)-len(s2))
    for i in range(shortest):
        if(s1[i] != s2[i]):
            diff += 1
    return diff
        
for i, line1 in enumerate(lines):
    for line2 in enumerate(lines[i:]):
        diff = difference(line1, line2)
        if diff == 1:
            print(f"Line 1 is {line1}, Line 2 is {line2}")