from input import parse_cmd_line, parse_file
from graph import Graph


def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    graph = Graph(vertices, edges)

    silly_path = graph.silly_path()

    graph.print_adj_list()
    print(f"Path traversed: {silly_path}")
    print(f"Path weight: {graph.path_weight}")

    graph.checker()

    if plot_graph:
        graph.plot()


if __name__ == "__main__":
    main()
