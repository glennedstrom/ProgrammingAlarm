# solution.py
from collections import deque
from typing import Dict, List

"""
Performs a breadth-first search traversal of an undirected graph starting from a given source node,
returning all nodes reachable from the source in BFS order.

Time Complexity:
    - O(V + E) where V is the number of vertices and E is the number of edges
    - We visit each reachable vertex once and explore each connected edge once

Space Complexity:
    - O(V) for the visited set and queue
    - In the worst case, we might need to store all reachable vertices in the queue

Args:
    graph (Dict[int, List[int]]): An adjacency list representation of the graph
        where keys are nodes and values are lists of neighboring nodes.
    source (int): The starting node for the BFS traversal.

Returns:
    List[int]: A list of nodes reachable from the source in BFS traversal order.
"""


def bfs_traversal(graph: Dict[int, List[int]], source: int) -> List[int]:
    # Handle empty graph or invalid source
    if not graph or source not in graph:
        return []

    visited = set()
    result = []
    queue = deque([source])
    visited.add(source)

    while queue:
        current = queue.popleft()
        result.append(current)

        # Visit neighbors in the order they appear in the adjacency list
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

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
