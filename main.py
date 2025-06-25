from src.input import parse_cmd_line, parse_file
from src.solution import process_graph
from src.graph import Graph


def main():
    in_file, plot_graph, solver = parse_cmd_line()
    vertices, edges = parse_file(in_file)

    graph = Graph(vertices, edges)
    graphs = graph.extract_connected_subgraphs()
    for i, g in enumerate(graphs):
        print(f"\033[92m    Subgraph {i + 1} of {len(graphs)}\033[0m")
        process_graph(g, plot_graph, solver)


if __name__ == "__main__":
    main()
