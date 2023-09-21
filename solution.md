\# R&D Test

\## Solution Lisa HAUSCARRIAGUE

\## Projet setup

- The file 'modif\_main.py' should be run by 'python main.py -i island.txt -p'
- The file 'prim\_algo.py' contains all the function to solve the problem

\## Presentation of the solution

The aim is to compute a path which travels each edge at least one time at minimum cost (the cost is the weight on the edges)

I used an adaptation of the Prim's algorithm because I want an optimal spanning tree.

I will present my solution step by step :

- I build a list 'List\_node' containing all the nodes that have to be connected. I delete elements from that list as they are connected to the rest.
- I build a set S of the connected nodes, so I add elements to this set.
- To find an edge induced by the subset S at minimum cost, and to reduce the complexity, first, I sort the edges of the original graph according to their weights, using an insertion sort.
- While the list 'List\_node' is not empty, I add a node to S which is at minimum cost from any vertices of S.

`	`- if an edge connecting the new node to S exists, I add it to T (final set of edges)

`	`- if no edge exists, it means that I cannot connect more vertices to the subset S, so I create a new separated group of node. I add an arbitrary node from 'List\_node' to S and I restrat the process.

\## Issues encountered

- In the file island.txt, all the nodes cannot be connected. That's why I decided to connect the maximum of vertices when it is possible, even if it's creating more groups.
- I have a high complexity. The code is fast for 'island.txt' and for 'hard\_to\_choose.txt'. But it takes 01:45:54 (1 hour 45 min!!) for 'paris\_map.txt' with a huge number a vertices and edges.

\## ToDo

- Reduce the complexity
- Plot the graph with different colors for separated group of vertices


I hope you will enjoy my project and I look forward to your feedback.

Lisa Hauscarriague
