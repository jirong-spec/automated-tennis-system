labels = {}
with open("labels.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        filename, p1, p2 = parts[0], int(parts[1]), int(parts[2])
        labels[filename] = (p1, p2)
