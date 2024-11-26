from input import parse_cmd_line, parse_file
from graph import Graph
from computation import Graph_to_eulerian_circuit


def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    if plot_graph:
        graph.plot()

    # Graph_to_eulerian_circuit solver function running all preprocessing and computations
    circuits, total_weights = Graph_to_eulerian_circuit(graph)
    
    for x in total_weights:
        print(f" Subgraph: {x}")
        print(f"     Weight: {total_weights[x]}")
        print(f"     Circuit: {circuits[x]}")
        print("----------------------------")

if __name__ == "__main__":
    main()