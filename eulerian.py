#@Author: Marie Latil
# Date: 2024-12-01
# Description: Three computation functions of the pseudo-Eulerian path
# Job offer: R&D Engineer 

import networkx as nx
import numpy as np

def semi_eulerian_path(graph, vertices, edges):
    """
    Parameters
    ----------
    graph : nx.MultiGraph
        graph with vertices and edges.
    vertices : list[tuple]
        list of vertices coordinates.
    edges : list[tuple]
        list of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
    
    Returns
    -------
    tuple[list[tuple], int]
        list of path coordinates, total weight.
    """
    # Compute the Eulerian path
    eulerian_path = list(nx.eulerian_path(graph))
   
    # Calculate the total weight
    used_edges = {}
    total_weight = 0
    for u, v in eulerian_path:
        for key, data in graph[u][v].items(): # Check available instances between u and v
            edge_instance = (min(u, v), max(u, v), key)  # (u, v) and (v, u) are not distinguished
            if edge_instance not in used_edges:
                total_weight += data['weight']  # add the weight of the specific edge
                used_edges[edge_instance] = True  # this edge has been used
                break  # take only one weight per edge

    # Build the final path with coordinates
    path_coordinates = []
    u0 = eulerian_path[0][0]
    for u, v in eulerian_path:
        coord_u = vertices[u-u0]
        coord_v = vertices[v-u0]
        path_coordinates.append((coord_u, coord_v))
    
    # eulerien_index = [u for u, v in eulerian_path] + [eulerian_path[-1][1]]
    # print(f"Path vertices indices: {eulerien_index}")
    print(f"Total weight with the computed path: {total_weight}")
    print(f"Total weight from the original graph: {np.sum(edge[2] for edge in edges)}")
    return path_coordinates, total_weight


def pseudo_eulerian_path(graph, vertices, edges): 
    """
    Parameters
    ----------
    graph : nx.MultiGraph
        graph with vertices and edges.
    vertices : list[tuple]
        list of vertices coordinates.
    edges : list[tuple]
        list of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
    
    Returns
    -------
    tuple[list[tuple], int]
        list of path coordinates, total weight.
    """
    ## TODO: Optimize the following part for the paris_map instance
    ## Idea: For the odd vertices, only look for the k-nearest odd vertices 
    
    # Find the shortest paths between odd vertices
    shortest_paths = {}
    for source, target_lengths in nx.all_pairs_dijkstra_path_length(graph, weight='weight'):
        for target, length in target_lengths.items():
            if source != target and graph.degree(source) % 2 == 1 and graph.degree(target) % 2 == 1:
                shortest_paths[(source, target)] = length

    # Find the minimum weight matches between odd vertices
    g_odd_complete = nx.Graph()
    for k, v in shortest_paths.items():
        g_odd_complete.add_edge(k[0], k[1], distance=v, weight=v)
    odd_matching = nx.algorithms.min_weight_matching(g_odd_complete, True)
       
    # Add the minimum matching edges to the graph
    graph_aug = nx.MultiGraph(graph.copy())
    for pair in odd_matching:
        graph_aug.add_edge(pair[0], pair[1])

    # Find the Eulerian path with the new edges (not necessarily the original edges)
    eulerian_path0 = list(nx.eulerian_path(graph_aug))
    
    # Create the Eulerian path with real edges from the original graph
    eulerian_path = []
    for edge in eulerian_path0:    
        if graph.has_edge(edge[0], edge[1]): # If `edge` exists in original graph, add it to the Eulerian path
            eulerian_path.append((edge[0], edge[1])) 
        else: # If `edge` does not exist in original graph, find the shortest path between its nodes
            aug_path = nx.shortest_path(graph, edge[0], edge[1], weight='weight')
            aug_path_pairs = list(zip(aug_path[:-1], aug_path[1:]))
            for edge_aug in aug_path_pairs:
                eulerian_path.append((edge_aug[0], edge_aug[1]))
            
    # Compute the total weight
    total_weight = 0
    for u, v in eulerian_path:
        for key, data in graph[u][v].items(): # Check available instances between u and v
            total_weight += data['weight'] # add the weight of the specific edge

    # Build the final path with coordinates
    path_coordinates = []
    u0 = eulerian_path[0][0]
    for u, v in eulerian_path:
        coord_u = vertices[u-u0]
        coord_v = vertices[v-u0]
        path_coordinates.append((coord_u, coord_v))
    
    # eulerien_index = [u for u, v in eulerian_path] + [eulerian_path[-1][1]]
    # print(f"Path vertices indices: {eulerien_index}")
    print(f"Total weight with the computed path: {total_weight}")
    print(f"Total weight from the original graph: {np.sum(edge[2] for edge in edges)}")
    
    return path_coordinates, total_weight


def non_connected_eulerian_path(graph, vertices, edges):
    """
    Parameters
    ----------
    graph : nx.MultiGraph
        graph with vertices and edges.
    vertices : list[tuple]
        list of vertices coordinates.
    edges : list[tuple]
        list of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
    
    Returns
    -------
    tuple[list[tuple], int]
        list of path coordinates, total weight.
    """
    results = []
    total_weight = 0
    
    # Find the connected components and apply the algorithm on each of them
    components = list(nx.connected_components(graph))
    for component in components:
        sub_graph = graph.subgraph(component).copy()
        sub_vertices = [v for v in component]
        sub_edges = [(u, v, weight, coordu, coordv) for u, v, weight, coordu, coordv in edges if u in component and v in component]
        
        if nx.has_eulerian_path(sub_graph): # Check if the subgraph is semi-eulerian
            print("The subgraph is semi-eulerian.")
            sub_result, sub_weight = semi_eulerian_path(sub_graph, sub_vertices, sub_edges)
            results.extend(sub_result)
            total_weight += sub_weight
        else: # Compute a pseudo-eulerian path
            print("The subgraph is not semi-eulerian. A pseudo-eulerian path is computed.")
            sub_result, sub_weight = pseudo_eulerian_path(sub_graph, sub_vertices, sub_edges)
            results.extend(sub_result)
            total_weight += sub_weight
        print('\n')
    return results, total_weight
