
# https://new.contest.yandex.ru/41243/problem?id=149944/2022_11_05/kQZsLlsTGU

# Решение:

def make_matrix(size, value=0):
    ans = []
    if isinstance(size, int):
        for i in range(size):
            ans.append([])
            for _ in range(size):
                ans[i].append(value)
    else:
        for i in range(size[1]):
            ans.append([])
            for _ in range(size[0]):
                ans[i].append(value)
    return ans