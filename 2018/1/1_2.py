visited = set()
visited.add(0)
freq = 0
done = False

while not done:
    file = open('input.txt','r')
    for line in file:
        freq += int(line)
        if freq in visited:
            print(freq)
            done = True
            break
        visited.add(freq)