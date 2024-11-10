from typing import Dict, List
from collections import deque

def bfs_traversal(graph: Dict[int, List[int]], source: int) -> List[int]:
    """
    Performs a breadth-first search traversal of an undirected graph starting from a given source node.

    BFS visits all nodes at the current depth level before moving to nodes at the next depth level.
    To ensure consistent ordering:
    1. Neighbors are processed in the order they appear in the adjacency list
    2. After completing a connected component, continues with the first unvisited node
       when iterating through graph keys

    Time Complexity:
        - O(V + E) where V is the number of vertices and E is the number of edges
        - We visit each vertex once and explore each edge once

    Space Complexity:
        - O(V) for the visited set and queue
        - In the worst case, we might need to store all vertices in the queue

    Args:
        graph (Dict[int, List[int]]): An adjacency list representation of the graph
            where keys are nodes and values are lists of neighboring nodes.
        source (int): The starting node for the BFS traversal.

    Returns:
        List[int]: A list of nodes in the order they were visited during BFS.
    """
    # Handle empty graph or invalid source
    if not graph or source not in graph:
        return []

    def bfs_component(start: int, visited: set) -> List[int]:
        """Helper function to perform BFS on a single connected component."""
        result = []
        queue = deque([start])
        visited.add(start)

        while queue:
            current = queue.popleft()
            result.append(current)
            
            # Visit neighbors in the order they appear in the adjacency list
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result

    # Initialize visited set
    visited = set()
    result = []
    
    # Start with the source node's component
    result.extend(bfs_component(source, visited))
    
    # Process any remaining unvisited components
    # Visit them in order of appearance in graph keys
    for node in graph:
        if node not in visited:
            result.extend(bfs_component(node, visited))

    return result

# Example usage
if __name__ == "__main__":
    example_graph = {
        0: [2, 1],
        1: [0, 3],
        2: [0, 3],
        3: [1, 2],
        4: [5],
        5: [4]
    }
    print("Graph:", example_graph)
    print("BFS traversal from node 2:", bfs_traversal(example_graph, 2))
