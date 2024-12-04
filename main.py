from input import parse_cmd_line, parse_file
from graph import Graph
from hierholzer import hierholzer
from cycle_tools import correction


def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    cycle = hierholzer(graph.edges)
    full_cycle = correction(cycle, graph.added_edge, graph.removed_edges)
    
    # Tel quel le cycle ne contient que le chemin, pas le poids associé.
    # Pour trouver le poids de la route, il suffit de faire une fonction qui suit le chemin et ajoute les poids. 

    if plot_graph:
        graph.plot()

    return full_cycle


if __name__ == "__main__":
    main()
