import heapq

def sma_star(graph, start, goal, heuristic, cost, memory_limit=5):
    frontier = []
    heapq.heappush(frontier, (heuristic[start], 0, start, [start]))
    explored = {}

    while frontier:
        if len(frontier) > memory_limit:
            # Remove node with highest f-cost to respect memory limit
            frontier.sort(reverse=True)
            frontier.pop(0)
            heapq.heapify(frontier)

        f, g, node, path = heapq.heappop(frontier)
        if node == goal:
            return path, g
        explored[node] = f

        for neighbor in graph[node]:
            if neighbor not in path:
                new_g = g + cost[(node, neighbor)]
                new_f = new_g + heuristic[neighbor]
                if neighbor not in explored or new_f < explored[neighbor]:
                    heapq.heappush(frontier, (new_f, new_g, neighbor, path + [neighbor]))
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
    memory_limit = int(input("Enter memory limit (number of nodes in frontier): "))
    if start not in graph or goal not in graph:
        print("Error: Start or goal node not found in graph.")
    else:
        path, total_cost = sma_star(graph, start, goal, heuristic, cost, memory_limit)
        if path:
            print(f"SMA* path from {start} to {goal}: {path} with total cost {total_cost}")
        else:
            print("No path found.")