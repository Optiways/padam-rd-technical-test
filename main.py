from input import parse_cmd_line, parse_file
from graph import Graph
from response import lowerBound, min_semi_eurelian_path, check_solution
import numpy as np


def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)
    if plot_graph:
        graph.plot()

    #CHECK CONNEXITE : PARCOURS EN LARGEUR
    if graph.isConnex_non_recursive():
        print("Graph is connex")
    else:
        print("Graph is not connex, \nThe answer is then +infinity but we can still compute semi-eulerian paths for all the connected part of the graph")
        return
    #compute lower bound
    lb = lowerBound(graph)
    print("Lower bound = ", lb)
    #compute min semi-eulerian path
    path, vpath, pathCost = min_semi_eurelian_path(graph)
    print("Semi Eulerian path's cost = ", pathCost)
    print("len path = ", len(path))
    print("len vpath = ", len(vpath))
    print("Vertices' path :", vpath)
    # print("Edges' path : ", path)
    #CHECK SOLUTION
    check_solution(graph, path, vpath, 0)
if __name__ == "__main__":
    main()
