from input import parse_cmd_line, parse_file
from graph import Graph
from prim_algo import Prim


def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    if plot_graph:
        graph.plot()
    
    new_edges = Prim(vertices, edges)
    print(f"#E_final={len(new_edges)}, #V_final={len(vertices)}")
    graph2 = Graph(vertices, new_edges)
    if plot_graph:
        graph2.plot()        

if __name__ == "__main__":
    main()
