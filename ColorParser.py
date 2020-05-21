from sys import stdin

data = stdin.read().split("\n")
data = list(map(lambda x: list((x.split("\t")[0], x.split("\t")[2])), data))
for elem in data:
    print(f"{elem[0]} = ({elem[1]})")