from input import parse_cmd_line, parse_file
from graph import Graph

def dijkstra(graph: Graph, v_start: tuple):
    "Run dijkstra from the vertex v_start to every other vertices in graph"
    unvisited_vertices = graph.vertices.copy()
    shortest_path_value = {}
    previous_vertices = {}
    max_value = len(graph.edges)*5 # TODO : replace by the max distance of the graph
    for vertex in unvisited_vertices:
        shortest_path_value[vertex] = max_value
    shortest_path_value[v_start] = 0
    
    while unvisited_vertices:
        current_min_vertex = None
        for vertex in unvisited_vertices:
            if current_min_vertex == None:
                current_min_vertex = vertex
            elif shortest_path_value[vertex] < shortest_path_value[current_min_vertex]:
                current_min_vertex = vertex
                
        neighbors_cost = [(edge[4], edge[2]) for edge in graph.edges if edge[3] == current_min_vertex] + [(edge[3], edge[2]) for edge in graph.edges if edge[4] == current_min_vertex]
        for neighbor in neighbors_cost:
            tentative_value = shortest_path_value[current_min_vertex] + neighbor[1]
            if tentative_value < shortest_path_value[neighbor[0]]:
                shortest_path_value[neighbor[0]] = tentative_value
                previous_vertices[neighbor[0]] = current_min_vertex
 
        unvisited_vertices.remove(current_min_vertex)

    return previous_vertices, shortest_path_value

def dijkstra_results(previous_vertices, shortest_path_value, v_start, v_target):
        "Return the path and value of the shortest path between v_start and v_target from dijkstra results"
        path = []
        vertex = v_target
        
        while vertex != v_start:
            path.append(vertex)
            vertex = previous_vertices[vertex]
        path.append(v_start)
        
        return path[::-1], shortest_path_value[v_target]

def get_eulerian_path(graph: Graph, v_start: tuple) -> list:
    "Compute the eulerian path of the graph starting from v_start"
    edges = graph.edges.copy()
    total_edges = len(graph.edges)
    path = [v_start]
    vertex = v_start
    neighbors = [edge for edge in edges if edge[3] == v_start or edge[4] == v_start]
    
    while len(edges):
        print(f"{total_edges - len(edges)}/{total_edges}", end="\r")
        if len(neighbors) == 0:
            raise ValueError("Not all edges have been found")
        if len(neighbors) == 1:
            next_edge = neighbors[0]
        else:
            for candidate in neighbors:
                candidate_graph = Graph(graph.vertices, edges.copy())
                [candidate_graph.vertices.remove(v) for v in candidate_graph.vertices if candidate_graph.degrees[v] == 0]
                if not candidate_graph.is_bridge(candidate):
                    next_edge = candidate
                    break

        edges.remove(next_edge)
        if vertex == next_edge[3]:
            vertex = next_edge[4]
        else:
            vertex = next_edge[3]
        path.append(vertex)
        neighbors = [edge for edge in edges if edge[3] == vertex or edge[4] == vertex]
    
    return path

def create_complete_graph(odd_list, initial_graph):
    """Create a complete graph with the list of odd degee vertices, where the value of each edge
    is the shortest path value of the initial graph"""
    complete_graph = Graph(odd_list, [])
    complete_paths = {}
    for start_idx in range(len(odd_list) - 1):
        previous_vertices, shortest_path_value = dijkstra(initial_graph, odd_list[start_idx])
        for end_idx in range(start_idx+1, len(odd_list)):
            path, best_value = dijkstra_results(previous_vertices, shortest_path_value, odd_list[start_idx], odd_list[end_idx])
            complete_graph.edges.append((start_idx, end_idx, best_value, odd_list[start_idx], odd_list[end_idx]))
            complete_paths[(odd_list[start_idx], odd_list[end_idx])] = path
    return complete_graph, complete_paths
            
def find_best_coupling(complete_graph: Graph):
    """we note n = len(complete_graph.vertices)
    the function returns the best coupling in the form [(vertex_1, vertex_2), ... (vertex_n-3, vertex_n-2)], v_start, v_end

    a good algorithm exists in O(n^3) by EDMONDS, J., AND E. JOHNSON, "Matching, Euler Tours and the Chinese Postman Problem," Mathematical Programming 5, 88-124 (1973).
    we can use the geographical information to limit the number of potential candidates
    The task is different from finding the best coupling for all the vertices as we can offload a lot of weight in the euler
    path starting from v_start.

    For now, we can just use the geographical information to match the vertices"""

    coupling = []
    vertices_to_match = complete_graph.vertices.copy()
    while len(vertices_to_match) > 2:
        v1 = vertices_to_match.pop()
        distances = [((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)**0.5 for v2 in vertices_to_match]
        v2_arg = argmin(distances)
        v2 = vertices_to_match[v2_arg]
        vertices_to_match.remove(v2)
        coupling.append((v1, v2))
    return coupling, vertices_to_match[0], vertices_to_match[1]

def argmin(l: list):
    min_val = l[0]
    min_idx = 0
    for idx, value in enumerate(l):
        if value < min_val:
            min_idx = idx
    return min_idx
            
def add_coupling_to_graph(initial_graph: Graph, coupling: list, complete_paths: dict):
    "Once the coupling done, we add the actual paths in the initial graph to reduce the number of odd degree vertices to 2."
    for (v1, v2) in coupling:
        edge_key = [edge for edge in complete_paths.keys() if (edge[0] == v1 and edge[1] == v2) or (edge[1] == v1 and edge[0] == v2)][0]
        path = complete_paths[edge_key]
        for i in range(len(path)-1):
            edge = [edge for edge in initial_graph.edges if (edge[3] == path[i] and edge[4] == path[i+1]) or (edge[4] == path[i] and edge[3] == path[i+1])][0]
            initial_graph.edges.append(edge)


def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    
    # If the graph is not connex (such as islands.txt), we can apply the algorithm on all the connectd subgraphs
    # For the moment, we only select the first one (if the graph is connex, this is the whole initial graph).
    graph.get_connected_subgraphs()
    graph = graph.connected_subgraphs[0]
    print(f"#E={len(graph.edges)}, #V={len(graph.vertices)}")

    # List the odd degree vertices
    odd_list = graph.compute_odd_list()
    print(f"Number of odd degree vertices : {len(odd_list)}")

    if len(odd_list) == 0:
        print("Graph is eulerian, the result is an eulerian cycle")
        result = get_eulerian_path(graph, graph.vertices[0])
        print(f"Start vertex : {result[0]}")
        print(f"End vertex : {result[-1]}")
    elif len(odd_list) == 2:
        print("There is an eulerian path")
        result = get_eulerian_path(graph, odd_list[0])
        v_end = odd_list[1]
        print(f"End vertex is the other odd degree vertex ? {v_end == result[-1]}")
    else:
        print("Too much odd degree vertices : we add coupling between them")
        complete_graph, complete_paths = create_complete_graph(odd_list, graph)
        coupling, v_start, v_end = find_best_coupling(complete_graph)
        add_coupling_to_graph(graph, coupling, complete_paths)
        graph.degrees = graph.compute_degrees()
        print(f"Number of odd degree vertices after the operation ? {len(graph.compute_odd_list())}")
        result = get_eulerian_path(graph, v_start)

    print(f"Number of edges ? graph : {len(graph.edges)}, path : {len(result)-1}")

    if plot_graph:
        graph.plot()


if __name__ == "__main__":
    main()
