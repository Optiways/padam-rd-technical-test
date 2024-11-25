from input import parse_cmd_line, parse_file
from graph import Graph
from computation import Solver


def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    if plot_graph:
        graph.plot()

    # Solver function running all preprocessing and computations to optain paths
    print(range(len(graph.vertices)))
    circuits, total_weights = Solver(graph)
    print(range(len(graph.vertices)))
    print(total_weights[1])
    
    for x in total_weights:
        print(f" Subgraph: {x}")
        print(f"     Weight: {total_weights[x]}")
        print(f"     Path: {circuits[x]}")
        print("----------------------------")

if __name__ == "__main__":
    main()