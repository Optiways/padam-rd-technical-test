from input import parse_cmd_line, parse_file
from graph import Graph

def solve_instance(file_name, plot_graph):
    vertices, edges = parse_file(file_name)
    graph = Graph(vertices, edges)

    try:
        eulerian_path = graph.find_eulerian_path()
        edge_sequence = []
        for i in range(1, len(eulerian_path)):
            u = eulerian_path[i-1]
            v = eulerian_path[i]
            edge_sequence.append((u,v))

        path_str = " -> ".joint([f"{u}-{v}" for u, v in edge_sequence])
        print(f"Instance: {file_name}")
        print(f"Eulerian Path: {path_str}\n")
    except ValueError:
        print("Of")
        print(f"Instance: {file_name}")
        print(f"Error: {ValueError}")


def main():
    in_file, plot_graph = parse_cmd_line()

    print(f"Instance: {in_file}")

    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    solve_instance(in_file, plot_graph)
    if plot_graph:
        graph.plot()


if __name__ == "__main__":
    main()
