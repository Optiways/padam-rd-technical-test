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