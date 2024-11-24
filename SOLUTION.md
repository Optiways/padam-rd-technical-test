# Solution : Continuous Traversal of All Edges in a Graph

## First Approach

For a continuous traversal of the edges, we can:

1 - Choose an arbitrary starting edge (the first one).  
2 - Find among the remaining edges the one that starts where the previous edge ended.  
3 - Repeat until all edges have been traversed.  

Let's test this first idea.

The idea here is to take control of the exercise and the pieces of code left for the user.

This first idea is, as expected, flawed.  
The "silly path" function does not return a completed path. In fact, it stops as soon as it no longer sees any new edges.  

Moreover, in this approach, it cannot pass through the same edge twice. So, if there is no Eulerian path starting from the initial edge, it will never find a correct path.  

A second issue would be related to the non-connectivity of the graph. We will therefore add a function to check the graph's connectivity. If the graph is not connected, we can create a path for each of its connected components *but there will be no possibility of creating a single path*.
 
## Graph connectivity

First, let's define a method to determine if the graph is connected. Then, for each connected component, we can apply our silly_path.
To determine if the graph is connected, we need to define a Depth-First Search (DFS) algorithm. We will use this algorithm to count the vertices accessible starting from a given vertex. If the number of accessible vertices is equal to the total number of vertices, then the graph is connected.

To make better progress on this problem, it's better to use an adjacency list. Thus, the build_adj_list method has been created.

By looking at the adjacency list, we quickly realize that in "hard to choose," all the vertices are connected to each other. Similarly, for "islands," all vertices are connected in two separate subgraphs (from vertex 0 to 19, from vertex 20 to 39, from vertex 40 to 59).  

Thus, we quickly realize the importance of considering the weight of the edges when traversing them. The silly_path will be updated accordingly.

## Update of the Approach to Consider Edge Weights and Graph Non-Connectivity

In this section, we will update our silly_path to account for the possibility of having multiple adjacency lists. We also need to update it so that it does not stop as soon as there are no more unvisited edges from the current vertex.

We will also modify the method so that when multiple edges are available, it chooses the lightest edge.

I encountered some difficulties (and so wasted a lot of time) in finding the closest edge in the neighborhood. A function has been added to the method to find a path to the nearest vertex that still has unvisited edges.

