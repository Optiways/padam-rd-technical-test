from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import math


class Graph:
    def __init__(self, vertices: list[tuple], edges: list[tuple]):
        """
        Parameters
        ----------
        vertices : list[tuple]
            list of vertices coordinates.
        edges : list[tuple]
            list of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
        """
        self.vertices = vertices
        self.edges = edges

    def plot(self):
        """
        Plot the graph.
        """
        weights = list(set(edge[2] for edge in self.edges))
        colors = plt.cm.get_cmap("viridis", len(weights))
        _, ax = plt.subplots()
        for i, weight in enumerate(weights):
            lines = [[edge[-2][::-1], edge[-1][::-1]] for edge in self.edges if edge[2] == weight]
            ax.add_collection(LineCollection(lines, colors=colors(i), alpha=0.7, label=f"weight {weight}"))
        ax.plot()
        ax.legend()
        plt.title(f"#E={len(self.edges)}, #V={len(self.vertices)}")
        plt.show()

    def degree(self):
        degree_dict =  {i: 0 for i in range(len(self.vertices))}
        for edge in self.edges:
            u, v, _,_, = edge
            degree_dict[u] += 1
            degree_dict[v] += 1
        return degree_dict

    def odd_vertices(self):
        degree_dict = self.degree()
        odd_vertices = [v for v, deg in degree_dict.items() if deg % 2 != 0]
        print(f"Odd vertices: {odd_vertices}")
        return odd_vertices

    def has_eulerian_path(self):
        odd_vertices = self.odd_vertices()
        print(f"Number of odd vertices: {len(odd_vertices)}")
        return len(odd_vertices) == 2 or len(odd_vertices) == 0

    def find_eulerian_path(self):
        if not self.has_eulerian_path():
            raise ValueError("The graph does not have an eulerian path.")

        odd_vertices = self.odd_vertices()
        start_vertex = odd_vertices[0] if odd_vertices else 0

        edges_copy = [list(edge) for edge in self.edges]

        def remove_edge(u, v):
            for edge in edges_copy:
                if (edge[0] == u and edge[1] == v) or (edge[0] == v and edge[1] == u):
                    edges_copy.remove(edge)
                    return

        def hierholzer(path, vertex):
            for edge in edges_copy:
                if edge[0] == vertex or edge[1] == vertex:
                    u, v = edge[0], edge[1]
                    if u == vertex:
                        next_vertex = v
                    else:
                        next_vertex = u
                    remove_edge(u,v)
                    hierholzer(path,next_vertex)
            path.append(vertex)

        path = []
        hierholzer(path, start_vertex)
        return path[::-1]