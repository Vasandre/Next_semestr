
# https://new.contest.yandex.ru/47939/problem?id=215/2023_03_20/jC7rL9y8fd

# Решение:

stack = []
ans = []

q = int(input())

for _ in range(q):
    query = input().split()
    
    if query[0] == '1':
        stack.append(int(query[1]))
    else:
        stack.pop()
    
    if stack:
        ans.append(stack[-1])
    else:
        ans.append(-1) 
    
print(*ans, sep="\n")
