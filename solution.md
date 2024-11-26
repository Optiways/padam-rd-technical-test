# Solution to the Pseudo-Eulerian Path Problem

## Problem Description

The goal of this solution is to compute a path in an undirected graph that traverses each edge at least once while minimizing the total distance traveled. 

This problem is closely related to real-world challenges in mobility.

---

## Steps of the Resolution

### 1. **Verify Graph Connectivity**
The first step ensures that the graph is connected, meaning every vertex can be reached from any other vertex. This is done using a depth-first search (DFS). If the graph is not connected, it is impossible to compute a pseudo-Eulerian path, and the program stops here.


### 2. **Identify Odd-Degree Vertices**
After verifying connectivity, the algorithm identifies vertices with an odd degree (vertices with an odd number of edges). According to Euler's theorem, a graph can have a pseudo-Eulerian path only if all vertices have even degrees or exactly two vertices have odd degrees.


### 3. **Compute Shortest Paths Between Odd-Degree Vertices**
For graphs with odd-degree vertices, the shortest paths between these vertices are calculated. This ensures that when additional edges are added to balance the graph, the total added distance is minimized.


### 4. **Perform Minimum Weight Matching**
All odd-degree vertices are paired in all possible combinations. For each pairing, the program evaluates the cost (total distance of the edges connecting the pairs). The pairing with the smallest total cost is selected to minimize the distance added to the graph.


### 5. **Augment the Graph**
The graph is modified by adding the new edges determined in the previous step. These additional edges make sure that all vertices now have even degrees, the graph has now the conditions for an Eulerian circuit.


### 6. **Construct the Eulerian Path**
A path is built that covers all edges.