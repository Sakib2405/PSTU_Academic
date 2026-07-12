def dls(graph, start, limit, visited=None, order=None, depth=0):
    if visited is None:
        visited = set()
    if order is None:
        order = []
    visited.add(start)
    order.append(start)
    if depth >= limit:
        return order
    for neighbor in graph[start]:
        if neighbor not in visited:
            dls(graph, neighbor, limit, visited, order, depth + 1)
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
    limit = int(input("Enter depth limit: "))
    if start not in graph:
        print(f"Error: Start node '{start}' not found in graph.")
    else:
        result = dls(graph, start, limit)
        print(f"DLS traversal order up to depth {limit}:", result)