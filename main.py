from input import parse_cmd_line, parse_file, get_weights_matrix
from graph import Graph

import time


def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    vertices_ids, edges_ids, weights_matrix = get_weights_matrix(in_file)
    graph = Graph(vertices, edges, vertices_ids, edges_ids, weights_matrix)
    path, path_cost = graph.get_path()
    print(path_cost)
    if plot_graph:
        graph.plot()


if __name__ == "__main__":
    main()
