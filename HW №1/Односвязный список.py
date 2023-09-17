
# https://new.contest.yandex.ru/50909/problem?id=215/2023_03_20/whpmVzFoJn

# Решение:

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def push(self, pos, val):
        new_node = ListNode(val)
        if pos == 0:
            new_node.next = self
            return new_node
        
        current = self
        count = 0

        while current:
            if count == pos - 1:
                new_node.next = current.next
                current.next = new_node
                break
            
            current = current.next
            count += 1
        
        return self

    def del_value(self, pos):
        if pos == 1:
            return self.next
        
        current = self
        count = 1

        while current:
            if count == pos - 1 and current.next:
                current.next = current.next.next
                break
            
            current = current.next
            count += 1
        
        return self


q = int(input())
listnode = None

for _ in range(q):
    req = input().split()
    
    if req[0] == '1':
        if listnode is None:
            listnode = ListNode(int(req[2]))
        else:
            listnode = listnode.push(int(req[1]), int(req[2]))
    elif req[0] == '2':
        cur = listnode
        numpos = 1
        
        while cur:
            if numpos == int(req[1]):
                print(cur.val)
                break
            
            cur = cur.next
            numpos += 1
    else:
        listnode = listnode.del_value(int(req[1]))
