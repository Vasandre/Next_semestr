
# https://new.contest.yandex.ru/48673/problem?id=215/2023_03_20/ckYXkoBQRB

# Решение:

keys = {}

q = int(input())

for _ in range(q):
    req = input().split(" ")

    if int(req[0]) == 1:
        keys[int(req[1])] = int(req[2])
    elif keys.get(int(req[1]), None):
        print(keys.get(int(req[1])))
    else:
        print(-1)