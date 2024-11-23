import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from input import parse_cmd_line, parse_file
from graph import Graph


def sub_connected_graphs(graph):
    """TODO
    If the initial graph is already connected, there is no change.
    If it is disconnected, it returns the of sub graphs that are connected.

    Parameters
    ----------
    graph : Graph
        Studied graph.
    
    Returns
    -------
    sub_graphs : list[Graph]
        List of the sub graphs that are connected
    """

def id_vertex(graph, vertex):
    """Defines the id of a given vertex"""
    for id, vertex_to_test in enumerate(graph.vertices):
        if vertex_to_test == vertex:
            return id

def create_key_edges(main_graph, sub_graph):
    """Puts the edges in a DataFrame format. 
    The indices define the id of the edges. Necessary because the list of edges is missing a key
    
    Parameters
    ----------
    main_graph : Graph
        Studied graph. May be disconnected
    
    sub_graph : Graph
        Studied sub graph of main_graph. Assumed to be connected.
    
    Returns
    -------
    edges_id : list
        List of the edges id as their index in the main_graph list
    """
    #TODO. Use the sub_connected_graph function to make the disconnected graph case general (and not islands.txt specific)
    if len(sub_graph.vertices) != len(main_graph.vertices): #Sub and main graphs are different
        if sub_graph.edges[0][0] == 0: #sub_graph1
            return list(pd.DataFrame(main_graph.edges).index)[:190]
        elif sub_graph.edges[0][0] == 20: #sub_graph2
            return list(pd.DataFrame(main_graph.edges).index)[190:570]   
        else: #sub_graph3
            return list(pd.DataFrame(main_graph.edges).index)[570:]  
    return list(pd.DataFrame(main_graph.edges).index)

def initialisation(graph):
    """Selects the initial vertex to start from.

    Parameters
    ----------
    graph : Graph
        Studied graph. Assumed to be connected.
    
    Returns
    -------
    vertex_0 : tuple
        Initial vertex
    """
    
    ##TODO:
    # A good initial guess would be an isolated vertex, i.e. a vertex with a low number of edges.
    # This would avoid going through the same edge twice
    # For now we just assume the first vertex to be the start of the path

    ##TODO:
    #Select n starting points far away from each other.
    #With this, we can use parallel programming with n threads
    return graph.vertices[0]

def find_neighbors(main_graph, sub_graph, vertex_i):
    """Fines the neighbors of the vertex_i, i.e. the vertices that have a common edge with vertex_i.
    
    Parameters
    ----------
    main_graph : Graph
        Studied graph. May be disconnected
    
    sub_graph : Graph
        Studied sub graph of main_graph. Assumed to be connected.
    
    vertex_i : tuple | int
        Current location
    
    Returns
    -------
    possible_edges : list[tuple]
        Neighbor vertices of vertex_i
    """
    possible_edges_id, arrival_vertices = [], []
    if type(vertex_i) == tuple: i_v = id_vertex(main_graph, vertex_i) #tuple vertex converted into id
    else: i_v = vertex_i
    for id, edge in enumerate(main_graph.edges):
        if edge[0] < i_v: #The id of the vertex_i will be at location 1 of the edge
            if edge[1] == i_v:
                possible_edges_id.append(id), arrival_vertices.append(edge[0])
        if edge[0] == i_v: #The id of the vertex_i will be at location 0 of the edge
            possible_edges_id.append(id), arrival_vertices.append(edge[1])
    return possible_edges_id, arrival_vertices

def is_not_visited(candidate_edges_id, remaining_edges_id):
    """Selects the edges that have not been visited yet among a list of candidates
    
    Parameters
    ----------
    candidate_edges : Graph
        List of edges to check.
    
    remaining_edges : list[tuple]
        List of the edges that still have to be visited

    Returns
    -------
    edge_to_visit : list[tuple]
        Candidates that have been selected for a first visit
    """
    # TODO: use an implemented pandas functions to filter instead of the for loop
    edge_to_visit_id = []
    for edge_id in candidate_edges_id: 
        if edge_id in remaining_edges_id:
            edge_to_visit_id.append(edge_id) #Only look at vertices that have not been visited
    return edge_to_visit_id

def next_edge(main_graph,sub_graph, vertex_i, remaining_edges):
    """Chooses the next edge to take.
    
    Parameters
    ----------
    main_graph : Graph
        Studied graph. May be disconnected
    
    sub_graph : Graph
        Studied sub graph of main_graph. Assumed to be connected.

    vertex_i : tuple
        Current location
    
    remaining_edges : list[tuple]
        List of the edges that still have to be visited

    Returns
    -------
    id_edge_j : int
        Index of the new edge

    edge_j : tuple
        New location
    """
    order = 1
    neighbor_edges_id, neighbor_vertices = find_neighbors(main_graph, sub_graph, vertex_i) #The next vertex is one of the neighbors
    df_edges = pd.DataFrame(main_graph.edges,columns=["id_v0","id_v1","weight","coord_v0","coord_v1"]) #Transforms the list of edges in a DataFrame format
    ind_to_visit = is_not_visited(neighbor_edges_id, remaining_edges) 
    df_neighbors_to_visit = df_edges.iloc[ind_to_visit] #Filter the edges that have not been visited

    if len(df_neighbors_to_visit.index) !=0:
        # Select the next edge among the ones that have not been visited yet
        id_argmin = df_neighbors_to_visit["weight"].argmin() # Going twice by a low weight edge has less impact than going twice by a large weight edge
        edge_j = df_neighbors_to_visit.iloc[id_argmin].values
        id_edge_j = int(df_neighbors_to_visit.index[id_argmin])
        return id_edge_j, edge_j
    else:   
        # TODO merge both cases with a while loop
        # TODO There are currently holes/jumps in the path when all the neighbor edges have already been visited. 
        # Make sure to add the duplicates of already visited paths
        
        #All the neighbor edges have already been visited: We need to explore further
        neighbor_edges_id_order_n, neighbor_vertices_order_n = neighbor_edges_id, neighbor_vertices
        weight_sum = df_edges.iloc[neighbor_edges_id_order_n].weight
        while len(df_neighbors_to_visit) == 0:
            #Exploration algorithm
            order +=1
            for neighbor_vertex in neighbor_vertices_order_n :
                sub_neighbor_edges_order_n, sub_neighbor_vertices_order_n = find_neighbors(main_graph,sub_graph, neighbor_vertex)
                # TODO inneficient method, the same paths are examinated many times.
                # Idea: only explore around new vertices instead of old and new. Big temporal gainer.
                neighbor_edges_id_order_n = neighbor_edges_id_order_n + sub_neighbor_edges_order_n
                neighbor_vertices_order_n = neighbor_vertices_order_n + sub_neighbor_vertices_order_n
                
            ind_to_visit_n = is_not_visited(neighbor_edges_id_order_n, remaining_edges)
            df_neighbors_to_visit = df_edges.iloc[ind_to_visit_n]
        
        # len(df_neighbors_to_visit) != 0
        id_argmin = df_neighbors_to_visit["weight"].argmin() 
        # TODO select the minimum weight of the set of edges, instead of the last edge
        edge_j = df_neighbors_to_visit.iloc[id_argmin].values
        id_edge_j = int(df_neighbors_to_visit.index[id_argmin])
        return id_edge_j, edge_j

def create_path(main_graph, sub_graph):
    """Creates a pseudo-eulerian path for a given graph.
    
    Parameters
    ----------
    main_graph : Graph
        Studied graph. May be disconnected
    
    sub_graph : Graph
        Studied sub graph of main_graph. Assumed to be connected.
    
    Returns
    -------
    path : list[tuple]
        Path as a ordered list of location
    
    list_cost : list
        List of the cost (weight) of each edge. The sum of this list is the cost of the path to minimise.
    """
    vertex_0 = initialisation(sub_graph)
    remaining_edges = create_key_edges(main_graph, sub_graph)
    path, list_cost = [],[] # Path with and without duplicates
    vertex_path = [vertex_0]
    while len(remaining_edges) != 0:
        #if len(path) %10 ==0:
        print("len(path) =",len(path))
        id_edge,edge = next_edge(main_graph, sub_graph, vertex_path[-1], remaining_edges)
        path.append(edge)
        list_cost.append(edge[2])
        if vertex_path[-1] == edge[3]: #Index 3 of edge is the previous vertex
            vertex_path.append(edge[4]) #Append index 4 of edge as the current vertex
        else: #Index 4 of edge is the previous vertex
            vertex_path.append(edge[3]) #Append index 3 of edge as the current vertex
        if id_edge in remaining_edges: #The chosen edge had not been visited yet
            remaining_edges.remove(id_edge)
    print("Remaining edges =", len(remaining_edges))
    return path, list_cost

def plot(path):
    """TODO
    A function that plots the taken path.
    Can imagine a animated image with a traveller mooving according to the defined edges.
    Add an increasing value of the objective function as the traveller is mooving"""

def main():
    in_file, plot_graph = parse_cmd_line()
    print(in_file, plot_graph)
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    GRAPH = Graph(vertices, edges)
    if len(vertices) == 60: 
        # TODO: use the function sub_connected_graphs instead to generalise the case of a disconnected graph
        sub_graph_1 = Graph(GRAPH.vertices[:20],GRAPH.edges[:190])
        sub_graph_2 = Graph(GRAPH.vertices[20:40],GRAPH.edges[190:570])
        sub_graph_3 = Graph(GRAPH.vertices[40:],GRAPH.edges[570:])
        solution_path_1 = create_path(GRAPH,sub_graph_1)
        solution_path_2 = create_path(GRAPH,sub_graph_2)
        solution_path_3 = create_path(GRAPH, sub_graph_3)
        print("Solution path_1 =",solution_path_1)
        print("Solution path_2 =",solution_path_2)
        print("Solution path_3 =",solution_path_3)

    else:
        solution_path = create_path(GRAPH, GRAPH)
        print("Solution path =", solution_path)
    
    if plot_graph:
        GRAPH.plot()
        if len(vertices) == 60: 
            sub_graph_1.plot()
            sub_graph_2.plot()
            sub_graph_3.plot()


if __name__ == "__main__":
    main()

#/usr/local/bin/python3 /Users/nicolas/Documents/Padam_RD_Test/main.py -i Documents/Padam_RD_Test/instances/islands.txt -p