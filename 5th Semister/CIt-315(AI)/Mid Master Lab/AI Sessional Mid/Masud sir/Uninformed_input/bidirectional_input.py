from collections import deque

def bidirectional_search(graph, start, goal):
    if start == goal:
        return [start]
    # Initialize frontiers
    frontier_start = deque([start])
    frontier_goal = deque([goal])
    # Visited sets and parent maps
    visited_start = {start}
    visited_goal = {goal}
    parent_start = {start: None}
    parent_goal = {goal: None}

    while frontier_start and frontier_goal:
        # Expand from start side
        current_start = frontier_start.popleft()
        for neighbor in graph[current_start]:
            if neighbor not in visited_start:
                visited_start.add(neighbor)
                parent_start[neighbor] = current_start
                frontier_start.append(neighbor)
                if neighbor in visited_goal:
                    return build_path(parent_start, parent_goal, neighbor)
        # Expand from goal side
        current_goal = frontier_goal.popleft()
        for neighbor in graph[current_goal]:
            if neighbor not in visited_goal:
                visited_goal.add(neighbor)
                parent_goal[neighbor] = current_goal
                frontier_goal.append(neighbor)
                if neighbor in visited_start:
                    return build_path(parent_start, parent_goal, neighbor)
    return None

def build_path(parent_start, parent_goal, meeting_node):
    # Build path from start to meeting node
    path_start = []
    node = meeting_node
    while node:
        path_start.append(node)
        node = parent_start[node]
    path_start.reverse()
    # Build path from meeting node to goal
    path_goal = []
    node = parent_goal[meeting_node]
    while node:
        path_goal.append(node)
        node = parent_goal[node]
    return path_start + path_goal

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
        path = bidirectional_search(graph, start, goal)
        if path:
            print(f"Bidirectional Search path from {start} to {goal}: {path}")
        else:
            print("No path found.")