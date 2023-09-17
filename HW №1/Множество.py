
# https://new.contest.yandex.ru/48672/problem?id=215/2023_03_20/JBeZfdqvZn

# Решение:

q = int(input())
nums = set()

for _ in range(q):
    req = input().split(" ")

    if int(req[0]) == 1:
        nums.add(int(req[1]))
    elif int(req[1]) in nums:
        print(1)
    else:
        print(0)