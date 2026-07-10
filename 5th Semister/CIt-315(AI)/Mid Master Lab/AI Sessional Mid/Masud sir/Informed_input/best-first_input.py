import heapq

def best_first_search(graph, start, goal, heuristic):
    visited = set()
    queue = []
    heapq.heappush(queue, (heuristic[start], start, [start]))

    while queue:
        h, node, path = heapq.heappop(queue)
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(queue, (heuristic[neighbor], neighbor, path + [neighbor]))
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
    heuristic = {
        'A': 5,
        'B': 4,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 0
    }
    start = input("Enter starting node: ").strip()
    goal = input("Enter goal node: ").strip()
    if start not in graph or goal not in graph:
        print("Error: Start or goal node not found in graph.")
    else:
        path = best_first_search(graph, start, goal, heuristic)
        if path:
            print(f"Best-First Search path from {start} to {goal}: {path}")
        else:
            print("No path found.")