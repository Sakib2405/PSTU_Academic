def dls(graph, node, limit, visited=None, order=None, depth=0):
    if visited is None:
        visited = set()
    if order is None:
        order = []
    visited.add(node)
    order.append(node)
    if depth >= limit:
        return
    for neighbor in graph[node]:
        if neighbor not in visited:
            dls(graph, neighbor, limit, visited, order, depth + 1)
    return order

def iddfs(graph, start, max_depth):
    for depth in range(max_depth + 1):
        visited = set()
        order = []
        dls(graph, start, depth, visited, order)
        print(f"Depth {depth}: {order}")

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
    max_depth = int(input("Enter maximum depth: "))
    if start not in graph:
        print(f"Error: Start node '{start}' not found in graph.")
    else:
        iddfs(graph, start, max_depth)