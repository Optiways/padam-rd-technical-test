# Approach to the R&D problem

## Format

### main.py

Separates the computation depending on 3 cases, each case calls a function:

- a non-connected graph,
- a connected and semi-eulerian one,
- a connected and not semi-eulerian one.

All the functions are all defined in `eulerian.py`.

### eulerian.py

Includes 3 functions:

- `semi_eulerian_path`: finds directly an Eulerian path because the graph is semi-Eulerian.
- `pseudo_eulerian_path`: computes new edges that minimize the global weight and transform the graph into a semi-Eulerian one (all the odd vertices become even).
- `non_connected_eulerian_path`: the 2 previous functions are applied to each connected subgraph depending on if it is semi-Eulerian or not.

## Solutions for each instance - global approach

### Global approach - change all the odd-degree vertices into even-degree ones

For a non semi-Eulerian graph, the method used is the following one:

- find the odd vertices
- find the shortest paths between all the odd vertices
- find the minimum weight matches between each pair of odd vertices (there is always an even number of them)
- add these new edges to the graph, which is now semi-Eulerian (all the vertices are even)
- compute an Eulerian path by switching the non real edges with the shortest way from real edges

### Instance 1 - hard_to_choose

This instance is Eulerian: all the vertices are even. The minimum weight is then the total weight of the graph.

**Computed minimum weight**: 1200

### Instance 2 - islands

This instance is not connected, it is composed of 3 "islands". Each subgraph is handled separately and the total weight is then the sum of each subtotal.

- **Island 1 - Id 0 to 19:** The first island is not semi-Eulerian. The global approach explained above is applied. All the 20 vertices are odd, then only 10 edges are needed to be travelled twice. Each one has a weight of 1. The total weight for this island is then the total weight of the subgraph + 10, which gives 487.
- **Island 2 - Id 20 to 39:** The second island is semi-Eulerian. The minimum weight is then the total weight of the subgraph, which is 936.
- **Island 3 - Id 40 to 59:** The third island is just like the first one, which gives a minimum weight of 493.

**Computed minimum weight**: 1916

### Instance 3 - paris_map

This instance has a huge amount of vertices and edges, both odd and even-degree vertices.
The previous method is too time-consuming and computationally demanding, and an optimisation is needed.
I did not yet succed in creating an optimal algorithm to find a minimum weight for this instance, but the following points highlight optimisation ideas:

- All the paths are computed between the odd vertices:
  Other algorithms than `nx.all_pairs_dijkstra_path_length` can be more efficient, such as Floyd-Warshall. Algorithms which compute shorter paths in parallel might also be more efficient. In addition, a search only on the k-nearest neighbors for each odd vertice, with Dijkstra, A* or another, might reduce the computation demand.
- The algorithm of minimum matching is intensive:
  Other algorithms than `nx.algorithms.min_weight_matching` might be more efficient, such as the Blossom one.
  Besides, matching approximations might be efficient enough to find a total weight close to the minimum one.
