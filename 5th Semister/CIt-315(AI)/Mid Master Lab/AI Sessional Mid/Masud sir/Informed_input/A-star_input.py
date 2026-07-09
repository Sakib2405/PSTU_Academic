import heapq

def a_star_search(graph, start, goal, heuristic, cost):
    open_set = []
    heapq.heappush(open_set, (heuristic[start], 0, start, [start]))  # (f, g, node, path)
    closed_set = set()

    while open_set:
        f, g, node, path = heapq.heappop(open_set)
        if node == goal:
            return path, g
        if node in closed_set:
            continue
        closed_set.add(node)
        for neighbor in graph[node]:
            if neighbor not in closed_set:
                new_g = g + cost[(node, neighbor)]
                new_f = new_g + heuristic[neighbor]
                heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))
    return None, float('inf')

if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    cost = {
        ('A', 'B'): 2,
        ('A', 'C'): 4,
        ('B', 'A'): 2,
        ('B', 'D'): 1,
        ('B', 'E'): 3,
        ('C', 'A'): 4,
        ('C', 'F'): 5,
        ('D', 'B'): 1,
        ('E', 'B'): 3,
        ('E', 'F'): 1,
        ('F', 'C'): 5,
        ('F', 'E'): 1
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
        path, total_cost = a_star_search(graph, start, goal, heuristic, cost)
        if path:
            print(f"A* Search path from {start} to {goal}: {path} with total cost {total_cost}")
        else:
            print("No path found.")
