from collections import deque

tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G', 'H'],
    'F': [],
    'G': [],
    'H': ['P'],
    'P': []
}

def bfs(tree, start):
    visited = []
    queue = deque([start])   # start node diye queue initialize
    while queue:
        node = queue.popleft()   # ekta node ber kori
        if node not in visited:
            print(node, end=" ")
            visited.append(node)
            queue.extend(tree[node])  # children gula queue te add kori
start_node = input("Enter starting node: ")
bfs(tree, start_node)
