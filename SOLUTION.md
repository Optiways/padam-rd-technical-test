# Approach

My approach was first to check if each instance was connected or not. If one of them wasn't connected, then i would try to decompose the graph into sub-graphs.
To check if an instance is connected, i run a DFS algorithm through the graph until it went through every vertices.
If an instance is connected, then i would check if it has an Eulerian path or not, or even a Eulerian cycle if all properties about vertices' degrees are checked (i.e. if all degrees are even, or if i only have at most 2 odd degrees). 
If an instance is indeed connected and has an Eulerian path/Eulerian cycle, then it means i can go through every edge only once. In this case, the minimum total distance traveled is just the sum of all edges' weights. And to find the path, i would use the DFS algorithm first (however it wasn't working for the paris_map instance, and i didn't have the time to try with BFS), starting from any vertex if it was an Eulerian circuit, or one of the vertices with an odd degree if it was an Eulerian path.
If an instance is not connected, then i would try to decompose the graph into connected subgraph. 
To do this, i would perform another DFS from a random vertex, until it finds all vertices connected between them. Several lists would be created to follow the creation of the connected sub-graph. 
Using a boolean dict for every vertex, once a sub-graph is found i delete all its vertices from the boolean dict, and start from another vertex to find the next connected sub-graph. I perform this until every vertex from the initial graph has been checked.
Then i perform the same step as for a connected graph, which is checking if those sub-graph have an Eulerian path or Eulerian circuit.

If any graph has no Eulerian path or Eulerian circuit, then i would find all the pair with odd vertices and double the edges  with the minimum weight in order to have at least an Eulerian path with only 2 odd degrees at most. However i didn't have the time to try this, and i'm not even sure it would give me the path with the minimum total distance traveled.
