from graph import Graph
import time
from copy import copy


def computing_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time() 
        execution_time = end_time - start_time
        print(f"{func.__name__} runtime: {execution_time:.6f}")
        return result
    return wrapper

@computing_time
def Solver(graph_init):
    """
    Algorithm for the full resolution
    1. clean data
    2. check for odd_vertices
    3. add edges to become pseudo Eulerian
    4. compute solution
    5. check if circuit takes full graph i.e., if graph is disconnected
    6. if disconnected, remove previous data and keep going
    7. When there is no more date > end the program

    Parameters:
        graph: the graph we want to solve the problem on

    Returns:
        all_circuits dict[list(int)]: all circuits' paths (only one if graph is connected)
        all_total_weights dict[int]: all circuits' weights
    """
    graph = copy(graph_init)  # copy of the initial graph we will likely destroy in the process 
    number_of_graph=1  # number of subgraph we end up doing
    graph.clean_data()  # remove duplicates from dataset
    counter = 0  # Counter to filter out data used in previous subgraph
    all_circuits = {}  # store all paths
    all_total_weights = {}  # store all paths' weights


    while True:
        print(f"Graph number: {number_of_graph}")
        # Making sure things are empty when loop starts
        circuit = []
        filt_edges = []  # filter for if the graph is disconnected
        filt_vertices = []  # filter for if the graph is disconnected
        vertices_odd = {}

        vertices_odd = graph.get_odd_vertices()
        adj = graph.get_adjacent_vert()
        if vertices_odd:
            dist={}
            # for source in vertices_odd:
            #dist[1] = graph.dijkstra(1, adj)
            pairs_to_add = graph.shortest_paths(vertices_odd)
            graph.add_edges(pairs_to_add)

        circuit = graph.eulerian_circuit()
        total_weight = graph.circuit_weight(circuit)
        all_circuits[number_of_graph] = circuit
        all_total_weights[number_of_graph] = total_weight

        filt_edges, filt_vertices = check_if_graph_disconnected(graph, circuit, counter)

        if not filt_edges:
            print("a")
            print('Computation over')
            return all_circuits, all_total_weights
        else:
            counter += (len(graph.vertices) - (len(filt_vertices)))
            graph.edges = filt_edges
            graph.vertices = filt_vertices
            number_of_graph += 1


        if number_of_graph > 10000:
            print("Error:More than 10000 subgraphs seems weird here")
            exit()

def check_if_graph_disconnected(graph, circuit, counter):
    """
    Checks if it needs to make another subgraph as graph is disconnected
    and filters data to do so
    Parameters:
        graph Graph class: 
            our full graph
        circuit list[int]:
            our Eulerian path
        counter int: 
            counter to match index of new graph
    Returns:
        filt_edges list[graph.edges[items]]:
            filter to remove previous subgraph from dataset (here graph.edges)
        filt_vertices list[graph.vertices[items]]:
            filter to remove previous subgraph from dataset (here graph.vertices)
    """
    filt_edges = []
    filt_vertices = []

    for vertex in graph.edges:
        id1, id2, _, _, _ = vertex

        if id1 not in circuit and id2 not in circuit:
            filt_edges.append(vertex)

            if graph.vertices[id1-counter] not in filt_vertices:
                filt_vertices.append(graph.vertices[id1-counter])
            if graph.vertices[id2-counter] not in filt_vertices:
                filt_vertices.append(graph.vertices[id2-counter])
                
    return filt_edges, filt_vertices
