from input import parse_cmd_line, parse_file
from graph import Graph

import time


def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    start_time = time.time()
    graph.build_neighbors()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Temps d'exécution pour construire le dictionnaire des voisins : {execution_time:.6f} secondes")
    if plot_graph:
        graph.plot()


if __name__ == "__main__":
    main()
