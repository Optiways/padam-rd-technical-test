## Preliminary

I don't have a specific knowledge on graph theory, but a quick research on internet gives me a first few leads on how to proceed:

<b>1. </b> In the case where the graph has two or zero odd degree vertices, then there is a path visiting all edges exactly once, which is the optimal solution. A first step for my algorithm should be to check whether such a solution exists

<b>2. </b>If the graph has more than two odd degree vertices, then such a solution does not exist. In this case, I can always cut the problem in subgraphs having only two odd vertices. I have then to find a way to optimally cut my original graph in smaller graphs.

My work is then divided in two parts: first to get the pseudo-eulerian path in a graph corresponding to the first case, then to design the partition algorithm required for the second case

## Pseudo-Eulerian pathing

The first two function are vertices_degree and odd_even, computing the degree of every vertices. I proceed to realise that the graph given by "hard_to_choose.txt" has an Eulerian path, and I will use it as a benchmark for this section.

After an other quick search on internet, I find that hierholzer's algorithm seems the most efficient way to proceed to compute the solution, and the function compute_eulerian_path is an implementation of this algorithm. I can now check that the result of my algorithm on "hard_to_choose.txt" indeed gives me the sum of all the weight of the graph, which is the optimal solution. I proceed to implement the pseudo eulerian case by taking the case when there zero odd degree vertices and the case where there are two. I must then tackle the case of graphes with more than two odd degree.

## No eulerian pathing

In the case where there are no eulerian path, I should find a way to split the graph in smaller graph where eulerian paths exist. Upon looking up internet, this problem has a straight forward solution obtained in polynomial time: 

<b>1. </b> Compute the distance between all possible pairing of the odd degree vertices using a pathfinding algorithm such as Dijkstra's. 

<b>2. </b> Find the pairing that minimises the total distance between pairs

<b>3. </b> Then one should construct a new graph by addind the newly found pairing as virtual edge, and compute the Eulerian path on this new graph.

In order to save time, for the sake of the exercise, i will personally skip step 2.
I the end i took three hours-ish, and couldn't complete the distance function in time, so the whole algorithme will not work for paris_map.txt and island.txt, but this additional function should make my algorithm run given a bit more time.