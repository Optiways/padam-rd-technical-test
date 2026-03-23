# Problem

## References 
- https://en.wikipedia.org/wiki/Chinese_postman_problem
-- Kwan, Mei-ko (1960), "Graphic programming using odd or even points", Acta Mathematica Sinica (in Chinese), 10: 263–266, MR 0162630. Translated in Chinese Mathematics 1: 273–277, 1962.
- https://en.wikipedia.org/wiki/Eulerian_path#Hierholzer's_algorithm
--  Fleischner, Herbert (1991), "X.1 Algorithms for Eulerian Trails", Eulerian Graphs and Related Topics: Part 1, Volume 2, Annals of Discrete Mathematics, vol. 50, Elsevier, pp. X.1–13, ISBN 978-0-444-89110-5.
- https://en.wikipedia.org/wiki/Blossom_algorithm
--  Edmonds, Jack (1965). "Paths, trees, and flowers". Can. J. Math. 17: 449–467. doi:10.4153/CJM-1965-045-4.

## Global algorithm

Finding the path of smallest weight that covers all edges of an undirected graph is a **Chinese postman problem**. It has an exact solution with polynomial complexity 🎉

When a solution exists where each edge is travelled exactly once, we have an Eulerian graph, and the solution is called an Eulerian cycle. On an Eulerian graph, each node has an even number of vertices.

When there is no Eulerian graph, the best solution is to add virtual vertices to make the graph Eulerian. Each virtual vertex is an existing path in the graph.

To minimize the additional weight :
+ We only add virtual vertices for edges which need them
  + only betwen edges with even vertices
  + half as many vertices as even edges
+ minimum weight for each vertex : this is a shortest path problem, solvable with a Dijkstra algorithm
+ minimum total weight of added vertices : minimum weight perfect matching problem, solvable with an Edmond's blossom algorithm

Once we have an Eulerian graph, finding a Eulerian cycle can be done with Hierholzer's algorithm.

Since we want a path and not a cycle, we can remove the virtual vertex of max weight from the solution, its edges becoming the start and the finish of the path.

# Implementation choices

I wanted to have code that runs: since Dijkstra is already available in scipy and the global Chinese postman algorithm is simple, I chose to
- **implement Hierholzer's algorithm** : it was core to the solution, and other approachs such as depth first travel looked like they would sacrifice a lot in term of weight without being simpler to write from scratch
- not implement Edmond's blossom algorithm since it's complex and a naive approach, even if real bad weight-wise, would be really easy to write
- keep the existing graph data structure as much as possible to build on what already exists
- added simple instances for tests

# Potential next steps

## Debug
Paris and islands instancs are failing at the naive_matching step

## Performance
- measure time spent in each algorithm to taylor data structure specifically for it ; try with an adjency matrix 

## Solution quality
- Use Edmond's blossom algorithm instead of naive matching to minimize weight

## Code quality
- Have a way to call `edge.vertex[0]` instead of `edge[0]` and `edge.weight()` instead of `edge[2]`
- better handling of errors / None value / empty result
- stronger typing (once performances are stabilized)
- naming consistency (sometimes `vertex` is an `int`, sometimes it's a `list[Coordinates]`)
- organise solver in sub folders for each problem (perfect matching, shortest path, eulerian path, and chinese postman)
- consistency between case (camel, kebab)
- consistency between functional and object oriented style
- create and use a decorator to measure and log time spent in each method
