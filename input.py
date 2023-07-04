from __future__ import annotations

import argparse


def parse_cmd_line() -> tuple[str, int, int, bool]:
    """Parses command line from standard input and returns the parameters.

    Returns
    -------
    str
        Path to input graph file `G`.
        
    int
        Number of nodes to select in the considered graph `G`.
    
    int
        Distance to nearest selected node to be considered as covered.
        
    bool
        Whether to plot the graph or not.
    """
    parser = argparse.ArgumentParser("Padam R&D - Technical Test")
    parser.add_argument("-i", "--in_file", help="Path to graph '*.txt' file", dest="in_file", required=True)
    parser.add_argument(
        "-n", 
        "--nb_nodes", 
        help="Number of nodes to cover the graph",
        type=int,
        dest="nb_nodes", 
        required=True,
    )
    parser.add_argument(
        "-d", 
        "--distance_to_nearest_node", 
        help="Distance to nearest selected node to be considered as covered",
        type=int, 
        dest="distance_to_nearest_node", 
        required=True,
    )
    parser.add_argument(
        "-p",
        "--plot",
        help="Whether to plot the graph or not",
        action="store_true",
        dest="plot_graph",
        default=False,
        required=False,
    )
    args = parser.parse_args()
    return (args.in_file, args.nb_nodes, args.distance_to_nearest_node, args.plot_graph)


def parse_file(file_name: str) -> tuple[list[tuple], list[tuple]]:
    """Parses graph file input.

    Parameters
    ----------
    file_name : str
        txt file, with list of vertices coordinates, and list of edges.

    Returns
    -------
    tuple[list[tuple], list[tuple]]
        list of vertices coordinates, list of edges as tuple (id 1, id 2, distance, coordinates 1, coordinates 2).
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
            distance = int(splitted_line[2])
            coordinates_1 = vertices[vertex_1]
            coordinates_2 = vertices[vertex_2]
            edges.append((vertex_1, vertex_2, distance, coordinates_1, coordinates_2))

    return vertices, edges
