# Solution : Continuous Traversal of All Edges in a Graph

## First Approach

For a continuous traversal of the edges, we can:

1 - Choose an arbitrary starting edge (the first one).  
2 - Find among the remaining edges the one that starts where the previous edge ended.  
3 - Repeat until all edges have been traversed.  

Let's test this first idea.

This first idea is, as expected, flawed.  
The "silly path" function does not return a completed path. In fact, it stops as soon as it no longer sees any new edges.  
Moreover, in this approach, it cannot pass through the same edge twice. So, if there is no Eulerian path starting from the initial edge, it will never find a correct path.  
A second issue would be related to the non-connectivity of the graph. We will therefore add a function to check the graph's connectivity. If the graph is not connected, we can create a path for each of its connected components *but there will be no possibility of creating a single path*.
