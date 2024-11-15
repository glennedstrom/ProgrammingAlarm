from typing import Dict, List

"""
Performs a breadth-first search traversal of an undirected graph starting from
a given source node, returning all nodes reachable from the source in BFS order

Args:
    graph (Dict[int, List[int]]): An adjacency list representation of the graph
        where keys are nodes and values are lists of neighboring nodes.
    source (int): The starting node for the BFS traversal.

Returns:
    List[int]: A list of nodes reachable from the source in BFS traversal order

Example:
    >>> graph = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
    >>> bfs_traversal(graph, 0)
    [0, 1, 2, 3]
"""


def bfs_traversal(graph: Dict[int, List[int]], source: int) -> List[int]:
    # Your code here
    pass


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
    source = 2
    print("Graph:", example_graph)
    print(f"BFS traversal from node {source}:",
          bfs_traversal(example_graph, source))
