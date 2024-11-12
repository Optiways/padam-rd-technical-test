# Louis Simon's Answer

## First toughts

My first idea was that I needed to check the conditions for the existence of such a path. If we remove the vertices with no connection from the graph, the subgraph obtained should be connex. This is the first test to perform.

Then, we can use the fact that a graph with at most two vertices of odd degree possesses an eulerian path. It helps us understand that the odd degree vertices will be the place where the path will go more than once. It is important to list these vertices.

We can modify the graph by adding edges to odd degree vertices. By doing so, the graph will only have two odd degree vertices in the end. Then we can find an eulerian path that will be the optimal path of the modified graph.

Yet, if we add an edge between an odd degree vertex and an even degree vertex, we are just pushing the problem. The goal is now to "push" the odd degree vertex until we reach another odd degree vertex and they cancel each other.The path of the coupling should be the shortest possible, so we can use the Djisktra algorithm to find it.To do that, we need to connect odd degree vertices in pairs.

The problem is now to find the pairing that add the least weight to the graph. For example, if we have 4 vertices (A, B, C, D) of odd degree, we need to find whether we (AB, CD), (AC, BD) or (AD, BC) gives the best result.

## Approach

1. Check the connexity of the graph to understand how many connected subgraphs are included in the input. For now, we focus on only the first connex subgraphs but we could iterate for all of the connected components in the graph.
2. Select a connex subgraph and list every odd degree vertices. Depending on the size of the list, we have to modifiy the graph.
3. If there are 0 or 2 odd degree vertices, we can go the step 6.
4. Otherwise, we create a complete graph with these vertices. Associate the distance found with Djiskra's algorithm for every edges.
5. Select the best coupling and add the edges on the original graph. This is still TODO.
6. Compute the eulerian path on the modified graph and return the answer.

## Improvements and TODO

- Iterate over all connected subgraphs to find the answer for each of them, not only the first one.
- Create a better coupling function
- There is a lot of repetition of neighbor computation. There is maybe a good data structure to avoid too much computation.
- The algorithm is quite slow so that paris_map example is taking way too much time. Just to run the dfs algorithm is quite long, and it is an important part of the algorithm. There might be faster approach (maybe dynamic ?) to the problem even if the solution is approximate.
