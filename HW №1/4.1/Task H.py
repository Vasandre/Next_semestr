
# https://new.contest.yandex.ru/41242/problem?id=149944/2022_10_21/4GGEwO93c3

# Решение:

def is_palindrome(pal):

    if isinstance(pal, int):
        pal = str(pal)
    
    lo = 0
    hi = len(pal) - 1

    while lo < hi:
        if pal[lo] != pal[hi]:
            return False

        lo += 1
        hi -= 1
    
    return True