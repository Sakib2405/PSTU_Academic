
import heapq

# Graph representation with costs
graph = {
    'A': [('B', 2), ('C', 4)],
    'B': [('D', 1), ('E', 3)],
    'C': [('F', 5)],
    'D': [],
    'E': [('G', 2), ('H', 1)],
    'F': [],
    'G': [],
    'H': [('P', 3)],
    'P': []
}

def uniform_cost_search(graph, start, goal):
    """
    Uniform Cost Search algorithm to find the lowest cost path from start to goal.
    """
    visited = set()
    # Priority queue: (cost, node, path)
    queue = [(0, start, [start])]

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue
        visited.add(node)

        # If goal node is found
        if node == goal:
            print("\nPath found:")
            print(" -> ".join(path))
            print(f"Total cost: {cost}")
            return

        # Add children with cost
        for neighbor, edge_cost in graph[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (cost + edge_cost, neighbor, path + [neighbor]))

    print("\nNo path found!")

if __name__ == "__main__":
    print("Uniform Cost Search (UCS) Algorithm\n")
    print("Nodes:", ", ".join(graph.keys()))
    start = input("Enter starting node: ").strip()
    goal = input("Enter goal node: ").strip()
    if start not in graph or goal not in graph:
        print("Error: Start or goal node not found in graph.")
    else:
        uniform_cost_search(graph, start, goal)


