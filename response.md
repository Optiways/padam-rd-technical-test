Steps of the resolution : 

1. The first step is to check wether the graph is connex or not. If not, it is impossible to find an eulerian path. We proceid by doping a depth search

2. The second step is to check wether there are or not vertices with an odd degree. Thanks to Euler's theorem, we know that if all degrees are even, we can find an eulerian path in the graph

3. To create this semi-eurelian path, we create cycles within the graph and we mark the nodes that we visit in these cycles (adding these nodes to the path). When the source vertex has a null degree, we continue by going to the next vertex with a stricly positive degree. 