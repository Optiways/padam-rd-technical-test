#@Author: Padam Mobility
# Modified by Marie Latil
# Date: 2024-12-01
# Description: Main file to run the pseudo-Eulerian path algorithm
# Job offer: R&D Engineer 

from input import parse_cmd_line, parse_file
from eulerian import pseudo_eulerian_path, semi_eulerian_path, non_connected_eulerian_path
from graph import Graph
import networkx as nx
import time

def main():
    start = time.time()

    in_file, plot_graph,compute = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    
    if plot_graph:
        graph.plot()
    
    if compute:
        # Build the graph
        graph = nx.MultiGraph()
        for u, v, weight, coord_u, coord_v in edges:
            graph.add_edge(u, v, weight=weight, coord_u=coord_u, coord_v=coord_v)
            
        # Compute the semi-eulerian or pseudo_eulerian path
        if not nx.is_connected(graph): # Check if the graph is connected
            print("The graph is not connected. The subconnected graphs are computed.")
            path_coordinates, total_weight = non_connected_eulerian_path(graph, vertices, edges)
        elif nx.has_eulerian_path(graph): # Check if the graph is semi-eulerian
            print("The graph is semi-eulerian.")
            path_coordinates, total_weight = semi_eulerian_path(graph, vertices, edges)
        else: # Compute a pseudo-eulerian path
            print("The graph is not semi-eulerian. A pseudo-eulerian path is computed.")
            path_coordinates, total_weight = pseudo_eulerian_path(graph, vertices, edges)

        print(f"Total weight for the instance: {total_weight}")
    print(f"Execution time: {time.time() - start:.2f}s")

if __name__ == "__main__":
    main()
