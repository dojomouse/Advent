file = open('input.txt','r')

lines = [line for line in file]

def difference(s1, s2):
    max_len = min(len(s1), len(s2))
    diff = abs(len(s1)-len(s2))
    for i in range(max_len):
        if(s1[i] != s2[i]):
            diff += 1
    return diff

#print(lines[:5])
#lines = lines[:5]

def find_similar(lines):
    for i, line1 in enumerate(lines):
        for line2 in lines[i+1:]:
            #print(f"line1: {line1}, line2: {line2}")
            diff = difference(line1, line2)
            #print(diff)
            if diff == 1:
                return line1, line2

def find_common(s1, s2):
    common = ""
    for i in range(len(s1)):
        if s2[i] and s1[i] == s2[i]:
            common += s1[i]
    return common

line1, line2 = find_similar(lines)
print(f"Line 1 is {line1}, Line 2 is {line2}")
print(f"Common chars are: {find_common(line1, line2)}")

