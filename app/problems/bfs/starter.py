from typing import Dict, List

def bfs_traversal(graph: Dict[int, List[int]]) -> List[int]:
    """
    Perform a breadth-first search traversal of the given undirected graph.
    
    Args:
        graph (Dict[int, List[int]]): An adjacency list representation of the graph,
            where keys are nodes and values are lists of neighboring nodes.
            Nodes are numbered from 0 to n-1.
            
    Returns:
        List[int]: A list of nodes in the order they were visited during BFS,
            starting from node 0.
            
    Example:
        >>> graph = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
        >>> bfs_traversal(graph)
        [0, 1, 2, 3]
    """
    # Your code here
    pass
