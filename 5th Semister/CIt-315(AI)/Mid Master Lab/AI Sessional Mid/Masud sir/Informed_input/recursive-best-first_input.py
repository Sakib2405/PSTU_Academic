import sys

def rbfs(graph, node, goal, heuristic, cost, path=None, g=0, f_limit=float('inf')):
    if path is None:
        path = [node]
    if node == goal:
        return path, g
    successors = []
    for neighbor in graph[node]:
        if neighbor not in path:
            new_g = g + cost[(node, neighbor)]
            new_f = max(new_g + heuristic[neighbor], g + heuristic[node])
            successors.append((new_f, neighbor, new_g, path + [neighbor]))
    if not successors:
        return None, float('inf')
    successors.sort()
    while successors:
        best_f, best_node, best_g, best_path = successors[0]
        if best_f > f_limit:
            return None, best_f
        alternative = successors[1][0] if len(successors) > 1 else float('inf')
        result_path, result_f = rbfs(graph, best_node, goal, heuristic, cost, best_path, best_g, min(f_limit, alternative))
        if result_path:
            return result_path, result_f
        successors[0] = (result_f, best_node, best_g, best_path)
        successors.sort()
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
        path, total_cost = rbfs(graph, start, goal, heuristic, cost)
        if path:
            print(f"RBFS path from {start} to {goal}: {path} with total cost {total_cost}")
        else:
            print("No path found.")
