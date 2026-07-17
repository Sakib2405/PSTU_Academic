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
from collections import deque
def dfs_limited(tree, start, limit, visited=[]):
    if limit <= 0:
        return
    if start not in visited:
        print(start, end=" ")
        visited.append(start)
    for node in tree[start]:
        dfs_limited(tree, node, limit-1, visited)

def iterative_deepening(tree, start, max_limit):
    for i in range(max_limit):
        print(f"Iteration {i+1} : ", end="")
        dfs_limited(tree, start, i+1, [])
        print()

iterative_deepening(tree, 'A', 4)