# Implement Single-Source Breadth First Search

Requirements:
- Input: 
  - An undirected graph represented as an adjacency list (dictionary where keys are nodes and values are lists of neighbors)
  - A source node to start the traversal from
- Output: A list of nodes reachable from the source node in BFS traversal order
- Traversal rules (for consistent, unique solutions):
  - Start from the given source node
  - Process neighbors in the order they appear in the adjacency list
  - Visit all nodes at the current depth before moving to the next depth
  - Only visit nodes that are reachable from the source node
- Do not visit nodes unreachable from source node
- Handle empty graphs and single-node graphs
- Handle invalid source nodes

Example:
```python
Input: 
graph = {
    0: [2, 1],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2],
    4: [5],  # Not reachable from source=2
    5: [4]   # Not reachable from source=2
}

source = 2
```

Output: [2, 0, 3, 1]
# Explanation:
# - Start at node 2
# - Visit neighbors of 2 in list order: [0, 3]
# - Visit neighbors of 0: [2(already visited), 1]
# - Visit neighbors of 3: [1(already visited), 2(already visited)]
# - Visit neighbors of 1: [0(already visited), 3(already visited)]
# - Nodes 4 and 5 are not reachable from source=2, so they are not included
