from collections import deque

# Graph as adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'F'],
    'C': ['H'],
    'D': [],
    'F': ['G'],
    'H': ['K'],
    'G': ['I', 'J'],
    'I': ['L'],
    'J': ['L'],
    'K': [],
    'L': []
}

# BFS Implementation
def bfs(graph, start):
    visited = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            queue.extend(graph[node])
    return visited

# DFS Implementation (recursive)
def dfs(graph, node, visited=None):
    if visited is None:
        visited = []
    if node not in visited:
        visited.append(node)
        for neighbor in graph[node]:
            dfs(graph, neighbor, visited)
    return visited

# Run the algorithms
start_node = 'A'

print("BFS Traversal:", bfs(graph, start_node))
print("DFS Traversal:", dfs(graph, start_node))
