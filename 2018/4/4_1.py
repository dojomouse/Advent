import re

file = open('input.txt','r')

logs = []

for line in file:
    logs.append(re.match(r'\[([^<>]+)\]\s(.*)',line).groups())

print(logs[:5])

