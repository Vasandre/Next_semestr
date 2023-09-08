
# https://new.contest.yandex.ru/41242/problem?id=149944/2022_10_21/q5x4e7gb7c

# Решение:

def split_numbers(line):

    str = line.split(" ")
    ans = tuple([int(i) for i in str])
    return ans