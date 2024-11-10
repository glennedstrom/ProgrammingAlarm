from typing import Dict, List

def dfs_traversal(graph: Dict[int, List[int]], source: int) -> List[int]:
    """
    Performs a depth-first search traversal of an undirected graph starting from a given source node.

    DFS explores each path to its deepest level before backtracking.
    To ensure consistent ordering:
    1. Neighbors are processed in the order they appear in the adjacency list
    2. After completing a connected component, continues with the first unvisited node
       when iterating through graph keys

    Time Complexity:
        - O(V + E) where V is the number of vertices and E is the number of edges
        - We visit each vertex once and explore each edge once

    Space Complexity:
        - O(V) for the visited set and recursion stack
        - In the worst case (linear graph), the recursion stack might contain all vertices

    Args:
        graph (Dict[int, List[int]]): An adjacency list representation of the graph
            where keys are nodes and values are lists of neighboring nodes.
        source (int): The starting node for the DFS traversal.

    Returns:
        List[int]: A list of nodes in the order they were visited during DFS.
    """
    # Handle empty graph or invalid source
    if not graph or source not in graph:
        return []

    def dfs_component(node: int, visited: set, result: List[int]) -> None:
        """Helper function to perform DFS on a single connected component."""
        visited.add(node)
        result.append(node)
        
        # Visit neighbors in the order they appear in the adjacency list
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs_component(neighbor, visited, result)

    # Initialize visited set and result list
    visited = set()
    result = []
    
    # Start with the source node's component
    dfs_component(source, visited, result)
    
    # Process any remaining unvisited components
    # Visit them in order of appearance in graph keys
    for node in graph:
        if node not in visited:
            dfs_component(node, visited, result)

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
    print("DFS traversal from node 2:", dfs_traversal(example_graph, 2))
