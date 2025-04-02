# What graph representation?
## What we need
- **Directed** edges
- Each edge has **flow** and **capacity**
- Each edge also has a **residual edge** going in the opposite direction. It helps
  to undo bad augmenting paths which do not lead to max flow.

## Options
- Adjacency Matrix
  + Constant lookup time
  - Space inefficient

- Edge List
  + Space efficient
  - O(E) Lookup time
  
- Adjacency list with dictionaries
  + O(1) average case or O(V + E) amortized lookup time for an edge
  + O(V + E) space complexity

∴ **Adjacency list with dictionaries**

# Glossary
- **Arc:** an edge
- **Augmenting path:** a path of edges in the residual graph with unused capacity
  greater than 0 from sourse `s` to sink `t`. You will know you have reached saturating
  flow when no more augmenting paths remain.
- **Bottleneck of a path:** smallest edge capacity of a path.
- **Augment the flow:** using the bottleneck value to increment the `flow` for each
  arc in the path, and decrement for each residual edge.
- **Residual Edge**: is an edge for every arc, going in the opposite direction,
  with capacity 0, helping to undo bad augmentations.
- **Residual Graph**: is a graph which also contains residual edges.
- **Remaining Capacity** = e.capacity - e.flow

# Ford-Fulkerson Method
- continues finding augmenting paths and augments the flow until no more augmenting
  paths from s -> t exist.
- sum of the bottlenecks of each augmenting path will result in max-flow.
- time complexity depends on the algorithm used to find the augmenting paths.

## Note
- DFS chooses edges in random, so it is possible to pick the worst edge every time,
  killing the time complexity.
- Much better algorithms exists
  - Edmonds-Karp: Uses BFS as a method of finding augmented paths O(E^2V)
  - Capacity Scaling: Picks larger paths first O(E^2log(U))
  - Dinic's Algorithm: Uses combination of BFS and DFS O(V^2E)
