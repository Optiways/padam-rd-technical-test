from input import parse_cmd_line, parse_file
from graph import Graph


def main():

    # Parse command-line arguments
    in_file, plot_graph = "instances/hard_to_choose.txt", True 

    # Parse the input file to construct the graph
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")

    # Initialize the graph
    graph = Graph(vertices, edges)

    # Plot the graph if requested
    if plot_graph:
        graph.plot()

    # Solve the Problem
    path, total_weight = graph.solve_problem()

    # Output results
    print("Pseudo-Eulerian Path:", path)
    print("Total Weight of Path:", total_weight)


if __name__ == "__main__":
    main()