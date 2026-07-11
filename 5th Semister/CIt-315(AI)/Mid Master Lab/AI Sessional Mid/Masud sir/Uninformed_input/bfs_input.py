from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            order.append(node)
            queue.extend(neighbor for neighbor in graph[node] if neighbor not in visited)
    return order


if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    start = input("Enter starting node: ").strip()
    if start not in graph:
        print(f"Error: Start node '{start}' not found in graph.")
    else:
        result = bfs(graph, start)
        print("BFS traversal order:", result)