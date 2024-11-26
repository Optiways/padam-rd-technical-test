### Here's the reasoning behind my approach


The `degree()` function calculates the degree of each vertex by counting the connected edges. The `odd_vertices()` function identifies vertices with odd degrees, which are key to determining if an Eulerian path exists.

The `has_eulerian_path()` function checks if there are either zero or two odd-degree vertices. If true, Hierholzer’s algorithm is used to construct the path by starting at an odd-degree vertex and following unused edges until all edges are visited. The path is then reconstructed in the correct order.

