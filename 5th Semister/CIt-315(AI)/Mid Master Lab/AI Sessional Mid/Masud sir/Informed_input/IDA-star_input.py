def ida_star(graph, start, goal, heuristic, cost):
    def dfs(path, g, bound):
        node = path[-1]
        f = g + heuristic[node]
        if f > bound:
            return f, None
        if node == goal:
            return f, path
        min_bound = float('inf')
        for neighbor in graph[node]:
            if neighbor not in path:
                new_g = g + cost[(node, neighbor)]
                path.append(neighbor)
                t, result_path = dfs(path, new_g, bound)
                if result_path:
                    return t, result_path
                if t < min_bound:
                    min_bound = t
                path.pop()
        return min_bound, None

    bound = heuristic[start]
    path = [start]
    while True:
        t, result_path = dfs(path, 0, bound)
        if result_path:
            return result_path, t - heuristic[goal]
        if t == float('inf'):
            return None, float('inf')
        bound = t

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
        path, total_cost = ida_star(graph, start, goal, heuristic, cost)
        if path:
            print(f"IDA* path from {start} to {goal}: {path} with total cost {total_cost}")
        else:
            print("No path found.")
