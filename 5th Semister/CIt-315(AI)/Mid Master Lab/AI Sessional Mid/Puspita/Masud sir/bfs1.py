from collections import deque
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C':[],
    'D':[],
    'E': []
}
def bfs(tree, start):
    visited = []
    queue = deque([start])

    while queue:
        node = queue.popleft()

        if node not in visited:
            print(node, end = " ")
            visited.extend(node)
            queue.extend(tree[node])
start_node = input("enter a number : ")
bfs(tree, start_node)