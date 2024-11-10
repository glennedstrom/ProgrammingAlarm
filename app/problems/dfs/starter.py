from typing import Dict, List

def dfs_traversal(graph: Dict[int, List[int]], source: int) -> List[int]:
    """
    Performs a depth-first search traversal of an undirected graph starting from a given source node.
    
    Args:
        graph (Dict[int, List[int]]): An adjacency list representation of the graph,
            where keys are nodes and values are lists of neighboring nodes.
        source (int): The starting node for the DFS traversal.
            
    Returns:
        List[int]: A list of nodes in the order they were visited during DFS.
            
    Example:
        >>> graph = {0: [2, 1], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
        >>> dfs_traversal(graph, 2)
        [2, 0, 1, 3]
    """
    # Your code here
    pass
