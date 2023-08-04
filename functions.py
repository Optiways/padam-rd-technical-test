from __future__ import annotations
import matplotlib.pyplot as plt
import networkx as nx

def weight_connect_degree_mat(graph):
    vertices = graph.vertices
    edges = graph.edges
    V = len(vertices)
    W = [[0 for _ in range(V)] for _ in range(V)]
    D = [[0 for _ in range(V)] for _ in range(V)]
    C = [[0 for _ in range(V)] for _ in range(V)] # adjacency matrix, C[u][v] = 1 if u & v connected, 0 otherwise

    for edge in edges:
        (u, v, w, _, _) = edge
        w0 = W[u][v]  
        C[u][v] = 1     # u and v are connected
        C[v][u] = 1
        if w0 == 0: 
            W[u][v] = w    
            W[v][u] = w        
            D[u][u] += 1
            D[v][v] += 1
        else:
            W[u][v] = min(w,w0)     # we keep the shortest path
            W[v][u] = min(w,w0)
        
    return W, C, D

def neighbors(graph) -> list[list[tuple]]:  # return neighbors_list. neighbors_list[u] is the list of adjacent nodes and weights (v,weight) of u
    vertices = graph.vertices
    edges = graph.edges
    V = len(vertices)
    W, _, _ = weight_connect_degree_mat(graph)

    neighbors_list = [[] for _ in range(V)]
    for u in range(V):
         for v in range(V):
              w = W[u][v] 
              if w != 0:
                   neighbors_list[u].append((v,w))
    return neighbors_list

def nx_type_graph(graph):
    vertices = graph.vertices
    edges = graph.edges
    V = len(vertices)
    W, C, D = weight_connect_degree_mat(graph)
    N = neighbors(graph)

    G = nx.Graph()
    G.add_nodes_from([i for i in range(V)])
    for i in range(V):
        for j in range(V):
            if W[i][j] != 0:
                G.add_edge(i, j, weight=W[i][j])
    return G

def display_nxgraph(graph):
    G = nx_type_graph(graph)   
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=150, font_size=7, font_weight='bold', edge_color='gray', width=0.5)
    plt.show()                 

