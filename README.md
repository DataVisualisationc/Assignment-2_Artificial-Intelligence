# Assignment 2A_Tree Based Search

## Graph for Assignment 2A_Tree Based Search so far
<img width="7474" height="5240" alt="Graph Search Algorithms-2026-05-01-151447" src="https://github.com/user-attachments/assets/9d3c04be-31fa-4da0-9884-263ff6cd6995" />


## Usable Variable codes
### `start_node`
Description: The starting node of the search. Parsed from the first plain line in the input file

---

```
print(start_node)
# 'S'
```
---

### `goal`
Description: A single randomly chosen goal node.

```
print(goal)
# 'G'
```
---

### `pos`
Desscription: Maps each node name to its `(x, y)` screen coordinate. Used to compute straight-line (Euclidean) heuristic distances.
```
print(pos)
# {'S': (0, 0), 'A': (1, 2), 'B': (2, 1), 'C': (3, 3), 'G': (5, 5)}
 
x1, y1 = pos['S']
# x1 = 0, y1 = 0
```

### `node_colors`
Description: Parallel list to `list(G.nodes())` that controls node colours in the matplotlib plot. Modify during search to animate exploration.

**Colour conventions used in the codebase:**
 
| Colour | Meaning |
|--------|---------|
| `"blue"` | Default / unvisited |
| `"red"` | Start node or expanded node |
| `"green"` | Goal node (initial state) |
| `"grey"` | Node currently in frontier |
| `"orange"` | Goal node after being found/expanded |

```python
print(node_colors)
# ['red', 'blue', 'blue', 'blue', 'green']
 
# Updating a node's colour during search:
node_list = list(G.nodes())
idx = node_list.index(current)
node_colors[idx] = "grey"   # mark as frontier
node_colors[idx] = "red"    # mark as expanded
node_colors[idx] = "orange" # mark as goal found
```
### `G.neighbors(node)`
Description: Returns all directly reachable successor nodes from `node` via outgoing directed edges.

```python
list(G.neighbors('S'))
# ['A', 'B']
 
# Sorted (required for consistent grading order):
list(sorted(G.neighbors('S')))
# ['A', 'B']
```
---
### `G.nodes()`
Description: All nodes in the graph. Convert to a list when you need index-based access (e.g., for `node_colors`).

```python
list(G.nodes())
# ['S', 'A', 'B', 'C', 'G']
 
node_list = list(G.nodes())
idx = node_list.index('A')
# idx = 1
```
---
### `G.nodes[node]`
Description: Attribute dictionary for a specific node. Used to store and retrieve the `"heuristic"` value in informed searches.

```python
G.nodes['A']['heuristic'] = 3.61   # set
h = G.nodes['A']['heuristic']       # get
# h = 3.61
```
 
---

### `G[src][dest]['weight']`

Description: The weight of a directed edge between `src` and `dest`. Stored as a string from the parsed file.
```python
G['S']['A']['weight']
# '3'
 
int(G['S']['A']['weight'])
# 3
```
 
---
### `predecessor`
| Property | Detail |
|----------|--------|
| **Type** | `dict[str, str]` |
| **Description** | Maps each visited node to the node it was reached from. Used to reconstruct the path after reaching the goal. |
 
**Example output:**
```python
predecessor = {}
 
# After search completes:
predecessor
# {'A': 'S', 'B': 'S', 'C': 'A', 'G': 'C'}
```
### `frontier`
 
| Property | Detail |
|----------|--------|
| **Type** | `list` |
| **Description** | The collection of nodes waiting to be explored. Its behaviour differs by algorithm. |
 
| Algorithm | Data structure | Add | Remove |
|-----------|---------------|-----|--------|
| BFS | Queue (FIFO) | `frontier.append(n)` | `frontier.pop(0)` |
| DFS | Stack (LIFO) | `frontier.append(n)` | `frontier.pop()` |
| GreedyBFS | List sorted by heuristic | `frontier.append(n)` | `min(frontier, key=...)` |
| A* | List sorted by f = g + h | `frontier.append((f, n))` | `frontier.pop(0)` after sort |
 
**Example output:**
```python
frontier = ['S']
 
# After one expansion of 'S':
frontier
# ['A', 'B']
```

---

### `expanded`
 
| Property | Detail |
|----------|--------|
| **Type** | `list[str]` |
| **Description** | Nodes that have already been popped and processed. Used to avoid revisiting nodes. |
 
**Example output:**
```python
expanded = []
 
# After expanding 'S' then 'A':
expanded
# ['S', 'A']
 
if current in expanded:
    continue   # skip already-visited nodes
```
 
---
 
### `path_cost`
 
| Property | Detail |
|----------|--------|
| **Type** | `int` |
| **Description** | Total accumulated edge weight along the found path. Calculated by backtracking through `predecessor` after reaching the goal. |
 
**Example output:**
```python
path_cost = 0
 
# Backtrack pattern:
node = goal
while node != start_node:
    parent = predecessor[node]
    path_cost += int(G[parent][node]['weight'])
    node = parent
 
print(path_cost)
# 9
```

---
### `nodes_created`
 
| Property | Detail |
|----------|--------|
| **Type** | `int` |
| **Description** | Total number of nodes generated during the search. Calculated at goal termination. |
 
**Example output:**
```python
nodes_created = len(frontier) + len(expanded)
print(nodes_created)
# 7
```
 
---
### `path` / `path_str`
 
| Property | Detail |
|----------|--------|
| **Type** | `list[str]` / `str` |
| **Description** | The ordered sequence of nodes from start to goal. Reconstructed by backtracking through `predecessor`, then reversed. |
 
**Example output:**
```python
path = ['S', 'A', 'C', 'G']
 
path_str = " -> ".join(path)
# 'S -> A -> C -> G'
```
 
---
 
## Required Print Block
 
Every search function must print the following five lines upon finding the goal:
 
```python
print(f"Starting Node: {start_node}")
print(f"Destination Node: {goal}")
print(f"Number of nodes created: {nodes_created}")
print(f"Path: {path_str}")
print(f"Path Cost: {path_cost}")
```
 
**Example output:**
```
Starting Node: S
Destination Node: G
Number of nodes created: 7
Path: S -> A -> C -> G
Path Cost: 9
```
 
---


## Python parser code (Test)
Since the lecturer wants us to execute the file by command prompt 
C:\Assignments> python <file.python> <filename> <method> 

I have created a parser code that will parse the input files **Map.txt** and make it into a graph,
That means you guys **don't have to worry about how to parse/process the raw data**, all you guys need to do is understand which variables and methods from library and inside the parser code are usable in your algorithm.
For example, start_node, goals,G.neighbour, G.successors

_The parser.py is made for test only._

Library used: networkx (for data structures) , matplotlib (for drawing)

# How to test the parser file?

## 1 Install networkx and matlib Library

1. open terminal
2. type **pip install networkx matplotlib**
   if cannot then try **python -m pip install networkx matplotlib**

## 2 Open terminal in the folder

<img width="1302" height="1006" alt="image" src="https://github.com/user-attachments/assets/c7e950c8-307a-4f8a-b877-4b4719cc7117" />

## 3 Execute the parser file method "show" (in terminal ,cmd)

**python parser.py <any_map.txt> show**
It will show this (below)
<img width="1479" height="753" alt="image" src="https://github.com/user-attachments/assets/d6da5bcd-e5e5-4821-b102-0af1472142d0" />

**python "Assignment 2A_Tree_Based_Search.py" <anymap.txt> show** if using assignment folder
