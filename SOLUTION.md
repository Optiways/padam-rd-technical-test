# Padam Mobility R&D Technical Test

## Goal

Given an undirected weighted graph G(V,E), find the shortest path covering every edge of E at least once (Pseudo-eulerian).
Also known as the Chinese Postman Problem.

## Solution plan

1. Find odd degree vertices in G
2. If there is 0 or 2 odd then an Eulerian path exists in G got 5.
3. Eulerize the graph:
1. Minimum Weight Perfect Matching of the odd vertices
2. In G Duplicate the edges join the formed pair of odd vertices
5. Find and return the Eulerian path in G

## Odd vertices

For any graph G, the best path is, if it exists, is a path going through all vertices exactly once.
Such path exists if a graph is at least semi-Eulerian.

A graph is Eulerian iff it is connected and has no odd degree vertices
A graph is semi-eurian iff it is connected and has 2 odd degree vertices
Any other connected graph is not Eulerian, it can be converted to a semi-Eulerian one by joining 2 by 2 every but 2 odd vertices
Disconnected graphs are separated into connected subgraphs (without breaking any edge) and treated independently

## Minimum Weight Perfect Matching

For none Eulerian graph, the time limiting step is the pairing of odd vertices.
Brute force computing distances with Dijstra's for every combination of odd vertices and brute force pair matching would give the best solution but at the cost of combinatorial time complexity.

A workaround could be to heuristically predict distances between nodes combinations with an O(1) calculation such as Manhattan distance.
Vertices are then greedily paired. The actual path is finally computed for the formed pairs with dijstra's.

A second approach was implemented using PyMatching, a wrapper library of a C++ implementation of the sparse-blossom algorithm.
It is state of the art for MWPM in the field of Quantum Error Correction.
In our case, it still greatly outperforms the heuristic approach in run time while giving the optimal matching.

```
python main.py -i ./instances/paris_map.txt -s blossom
python main.py -i ./instances/paris_map.txt -s heuristic
```

## Eulerian path

At stage 6 all graphs are at least semi-eulerian. An Eulerian path can be found in linear time using Hierholzer’s algorithm.

## Results

| Metric      | hard_to_choose | islands 1    | islands 2  | islands 3    | paris | paris blossom |
|-------------|----------------|--------------|------------|--------------|-------|---------------|
| Vertices    | 35             | 20           | 20         | 20           | 11348 | 11348         |
| Edges       | 595            | 190          | 380        | 190          | 17958 | 17958         |
| Odd nodes   | 20             | 20           | 0          | 20           | 7318  | 7318          |
| Edge Weight | 1200           | 477          | 936        | 483          | 22924 | 22924         |
| Path Weight | 1200           | 493          | 936        | 499          | 27925 | 31759         |
| Path Length | 595            | 201          | 380        | 202          | 22219 | 24999         |
| RunTime (s) | 0.677          | 0.697 (file) | 0.697 file | 0.697 (file) | 92.0  | 3.041         |

## Improvement path

- Add tests
- Add a graph generator for automated testing and benchmarking
- Implement Edge and Node classes or use NetworkX for graph management
- Implement a visualizer to understand the heuristic's pitfalls
- Try other heuristics
- Benchmark blossom solution on larger graph
