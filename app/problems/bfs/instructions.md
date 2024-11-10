# Implement Breadth First Search

Requirements:
- Input: 
  - An undirected graph represented as an adjacency list (dictionary where keys are nodes and values are lists of neighbors)
  - A source node to start the traversal from
- Output: A list of nodes in the order they were visited during BFS
- Traversal rules (for consistent, unique solutions):
  - Start from the given source node
  - Process neighbors in the order they appear in the adjacency list
  - Visit all nodes at the current depth before moving to the next depth
  - After completing the connected component containing the source node, if there are unvisited nodes:
    - Pick the first unvisited node when iterating through graph keys
    - Start a new BFS from that node
    - Repeat until all nodes are visited
- Handle disconnected graphs
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
    4: [5],
    5: [4]
}
source = 2

Output: [2, 0, 3, 1, 4, 5]
# Explanation:
# - Start at node 2
# - Visit neighbors of 2 in list order: [0, 3]
# - Visit neighbors of 0: [2(already visited), 1]
# - Visit neighbors of 3: [1(already visited), 2(already visited)]
# - Visit neighbors of 1: [0(already visited), 3(already visited)]
# - Find first unvisited node (4)
# - Visit 4's neighbors: [5]
```

Notes:
- The graph is guaranteed to have nodes numbered from 0 to n-1
- Each edge is represented in both directions in the adjacency list
- The order of neighbors in the adjacency list determines the order of traversal
- The maximum number of nodes is 10^5
- The maximum number of edges per node is 10^4
- The source node is guaranteed to be present in the graph
