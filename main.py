"""Entry point of this technical test. Run `python3 main.py --help` to see how it works."""

from graph import Graph
from input import parse_cmd_line, parse_file


def main():
    """Entry point of this technical test. It fetches the selected instance's information and processes it."""
    in_file, N, D, plot_graph = parse_cmd_line()
    print(f"Loading graph '{in_file}' - Algorithm settings 'N = {N}' and 'D = {D}'")
    vertices, edges = parse_file(in_file)
    print(f"Graph has {len(edges)} edges and {len(vertices)} vertices")
    graph = Graph(vertices, edges)
    if plot_graph:
        graph.plot()


if __name__ == "__main__":
    main()
