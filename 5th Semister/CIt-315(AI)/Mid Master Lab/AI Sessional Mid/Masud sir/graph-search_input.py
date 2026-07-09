def graph_search(graph, start, goal):
    frontier = [[start]]
    visited = set()
    while frontier:
        path = frontier.pop(0)
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                frontier.append(new_path)
    return None

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
    goal = input("Enter goal node: ").strip()
    if start not in graph or goal not in graph:
        print("Error: Start or goal node not found in graph.")
    else:
        path = graph_search(graph, start, goal)
        if path:
            print(f"Graph Search path from {start} to {goal}: {path}")
        else:
            print("No path found.")