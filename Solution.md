The code solves the pseudo-Eulerian problem for a given graph. The procedure to run it is the same as for the template. The program delivers a non continuous path for the hard_to_choose.txt and islands.txt files. This is because it "forgets" to take into account the edges that are visited several times. For the paris_map.txt file, the program cannot go through all the edges in a reasonable time.

The followed approach, results and improvements and described bellow.

# Methodology
The methodology follows a greedy approach. The most intuitive solution is given, and no perturbation procedure is performed.

First, one initial vertex is selected. For simplicity reasons it is the one with the lowest index.
Then, for every visited vertex, the adjacent edges are identified.
Among them, the ones that have not been visited yet are kept.
If there is only one edge that has not been visited, then it chosen as the next one in the path.
If there are more than one, the one with the lowest weight is selected. The idea behind this is that if the path has to go through the same edge twice, it should be through the least costly one.
If none is available, an exploration process starts.
    New edges are searched corresponding to order 2,3,...,n neighbors, limiting the number of times the same edge is crossed.
    If several same order neighbors are founded, the subpath that has the lowest weight is selected.
Once a new edge is founded, the path and the list of edges remaining to visit are updated.
The algorithm stops once this list is empty.

# Results

For the hard_to_choose.txt file, the algorithm only revisits an edge once. Theoretically, the graph is Eulerian, so the output result is only one weight value away from the optimised solution.

For the islands.txt file, the graph is disconnected into three connected subgraphs. Therefore finding a continuous pseudo-Eulerian path is impossible. However, the problem can be reinterpreted into finding a pseudo-Eulerian path for each subgraph. This is done by studying the subgraphs sequentially. A better approach would be to parallise this search, having the number of threads being equal to the number of subgraphs.

For the paris-map.txt file, the program stops after visiting 5178 edges. Two explanations can be provided. Either, the solving time for finding the next edge is too long. Or, the program is stuck in a while loop.

# Improvements

The main issue of this program is that it gives a path that contains holes. When an edge is revisited, it is not taken into account in the path, making it discontinuous. To solve this issue, the list of visited edges in the exploration phase should be memorised. Then, among the subpaths that lead to a new edge, the one with the lowest weight should be selected.

From a computational point of view, the exploration algorithm is inneficent. First, all of the neighbors from order 1 to n are involved. Yet, if all the neighbor vertices from order 1 to n-1 lead to already visited edges, then only the order n neighbors have to be studied. Second, in the explored subpaths, the ones that backtrack to lower order neighbors are also considered. Whereas, the local optimum subpath must only move forward. 
Thus, too many vertices and edges are considered in this process, making it exponential. The number of edges and vertices in the hard_to_choose.txt and islands.txt files is limited, so it has a marginal impact on the computational cost. However, for the paris_map.txt file, the graph is much larger, which increases the risk of having a non-reasonable time solving procedure.

Another improvement would be to automatically detect the disconnections in the graph. For the case of the island.txt file, the problem was addressed "manually". This also might be a reason why the program fails with the Paris map: the program gets stuck in a while loop. Once the subgraphs are identified, a parallel approach can be used to reduce the computing time.

A marginal improvement concerns the initialisation of the algorithm. By starting from an isolated vertex (for example a dead-end street), it prevents travelling the same edge twice. Moreover, in the case of a disconnected graph, one point can be chosen by subgraph. Furthermore, to improve the quality of the solution, several starting points can be given, and the one with the lowest cost function is retained.

From a visualisation point of view, the solution can be plotted in a dynamic image, having a traveller going through all the edges of the graph.

Finally, a more complex method can be used. For example, one can involve metaheuristics. The output of the program is a local optimum path, that might not be global. To find a better solution, the obtained solution can be perturbed.