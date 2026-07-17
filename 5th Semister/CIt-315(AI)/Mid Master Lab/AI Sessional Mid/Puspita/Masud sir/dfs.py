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

def dfs(tree, node, visited = []):
    if node not in visited:
        print(node, end = " ")
        visited.append(node)
    for node in tree[node]:
        dfs(tree, node, visited)
start_node = input("Enter a node:")
dfs(tree, start_node)