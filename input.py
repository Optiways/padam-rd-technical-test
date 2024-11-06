from __future__ import annotations
import argparse
import numpy as np


def parse_cmd_line() -> tuple(str, bool):
    """
    Parses command line from standard input.

    Returns
    -------
    tuple(str, bool)
        path to input graph file, whether to plot the graph.
    """
    parser = argparse.ArgumentParser("Padam R&D Test")
    parser.add_argument("-i", "--in_file", help="path to graph txt file", dest="in_file", required=True)
    parser.add_argument(
        "-p",
        "--plot",
        help="whether to plot the graph",
        action="store_true",
        dest="plot_graph",
        default=False,
        required=False,
    )
    args = parser.parse_args()
    return args.in_file, args.plot_graph


def parse_file(file_name: str) -> tuple[list[tuple], list[tuple]]:
    """
    Parse graph file input.

    Parameters
    ----------
    file_name : str
        txt file, with list of vertices coordinates, and list of edges.

    Returns
    -------
    tuple[list[tuple], list[tuple]]
        list of vertices coordinates, list of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
    """
    with open(file_name, "r") as file:
        lines = file.readlines()
    vertices, edges = [], []
    for i, line in enumerate(lines):
        if i == 0:
            continue
        splitted_line = line.strip("\n\r").split(" ")
        if len(splitted_line) == 2:
            vertices.append((float(splitted_line[0]), float(splitted_line[1])))
        elif len(splitted_line) == 3:
            vertex_1, vertex_2 = int(splitted_line[0]), int(splitted_line[1])
            weight = int(splitted_line[2])
            coordinates_1 = vertices[vertex_1]
            coordinates_2 = vertices[vertex_2]
            edges.append((vertex_1, vertex_2, weight, coordinates_1, coordinates_2))

    return vertices, edges


def get_weights_matrix(file_name: str) -> tuple[list[int], list[tuple[int, int]], np.ndarray]:
    """
    Get the list of vertices ids and the matrix of weights of the edges.

    Parameters
    ----------
    file_name : str
        txt file, with list of vertices coordinates, and list of edges.

    Returns
    -------
    tuple[list[int], list[tuple[int, int]], np.ndarray]
        list of vertices ids,
        list of edges as tuple (id 1, id 2),
        matrix of weights of each edge (the value on the i-th line and the j-th column is the weigth of the edge between vertex i and vertex j).
    """
    with open(file_name, "r") as file:
        lines = file.readlines()
    edges_ids = []
    for i, line in enumerate(lines):
        splitted_line = line.strip("\n\r").split(" ")
        if i == 0:
            num_vertices = int(splitted_line[0])
            vertices_ids = [j for j in range(num_vertices)]
            weights_matrix = np.zeros((num_vertices, num_vertices))
        elif len(splitted_line) == 3:
            vertex_1, vertex_2 = int(splitted_line[0]), int(splitted_line[1])
            weight = int(splitted_line[2])
            edges_ids.append((vertex_1, vertex_2))
            weights_matrix[vertex_1, vertex_2] = weight
            weights_matrix[vertex_2, vertex_1] = weight

    return vertices_ids, edges_ids, weights_matrix
