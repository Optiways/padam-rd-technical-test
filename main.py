from input import parse_cmd_line, parse_file, get_weights_matrix
from graph import Graph

import time


def main():
    # load graph data
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    vertices_ids, edges_ids, weights_matrix = get_weights_matrix(in_file)

    # create graph object
    graph = Graph(vertices, edges, vertices_ids, edges_ids, weights_matrix)
    if plot_graph:
        graph.plot()

    # determine if graph is connected or not
    start_time = time.time()
    graph_is_connected = graph.is_connected()
    end_time = time.time()
    execution_time = end_time - start_time
    minutes = int(execution_time // 60)
    seconds = execution_time % 60
    print(f"Temps nécessaire pour savoir si le graphe est connexe ou non : {minutes} minutes {seconds:.2f} secondes")

    # if graph is connected, use get_path to find a path
    if graph_is_connected:
        start_time = time.time()
        path, path_cost = graph.get_path()
        end_time = time.time()
        execution_time = end_time - start_time
        minutes = int(execution_time // 60)
        seconds = execution_time % 60
        print(f"Coût du chemin obtenu : {path_cost}")
        print(f"Temps d'exécution pour déterminer le chemin : {minutes} minutes {seconds:.6f} secondes")
    # else, no path is possible
    else:
        print("Le graphe n'est pas connexe, il n'est pas possible de trouver un chemin parcourant toutes ses arêtes.")


if __name__ == "__main__":
    main()
