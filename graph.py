from __future__ import annotations

from typing import Union

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy.sparse import csr_array

Coordinates = tuple[float, float]
True_Edge = tuple[int, int, int, Coordinates, Coordinates]
Virtual_Edge = tuple[int, int, int, Coordinates, Coordinates, list[True_Edge]]
Edge = Union[None, True_Edge, Virtual_Edge]


class Graph:
    def __init__(
        self,
        vertices: list[Coordinates],
        edges: list[Edge],
    ):
        """Basic constructor of a `Graph` instance.

        Parameters
        ----------
        vertices : list[Coordinates]
            List of vertices coordinates.

        edges : list[Edge]
            List of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
        """
        self.vertices = vertices
        self.edges = edges
        self.real_edges = edges
        self.adjency_computed = False

    def plot(self):
        """
        Plot the graph.
        """
        weights = list(set(edge[2] for edge in self.edges if edge is not None))
        colors = plt.cm.get_cmap("viridis", len(weights))
        _, ax = plt.subplots()
        for i, weight in enumerate(weights):
            lines = [
                [edge[-2][::-1], edge[-1][::-1]]
                for edge in self.edges
                if edge is not None and edge[2] == weight
            ]
            ax.add_collection(
                LineCollection(
                    lines, colors=colors(i), alpha=0.7, label=f"weight {weight}"
                )
            )
        ax.plot()
        ax.legend()
        plt.title(f"#E={len(self.edges)}, #V={len(self.vertices)}")
        plt.show()

    @classmethod
    def display_path(cls, *, path: list[Edge]):
        return cls.display_paths(paths=[path])

    @staticmethod
    def display_paths(*, paths: list[list[Edge]]):
        colors = plt.cm.get_cmap("viridis", len(paths))
        figure = plt.figure()
        ax = figure.add_subplot()
        for path_index, path in enumerate(paths):
            for edge_index, edge in enumerate(path):
                if edge is None:
                    continue
                if edge is True_Edge:
                    ax.annotate(
                        str(edge_index),
                        xytext=edge[3],
                        xy=edge[4],
                        width=1,
                        arrowprops=dict(arrowstyle="->", color=colors(path_index)),
                    )
                if edge is Virtual_Edge:
                    # TODO : more elegant way to display edges travelled twice
                    ax.annotate(
                        f"virtual {edge_index}",
                        xytext=edge[3],
                        xy=edge[4],
                        width=2,
                        arrowprops=dict(arrowstyle="->", color=colors(path_index)),
                    )
        plt.show()

    def compute_adjency(self):
        vertex_adjency = [0 for vertex in self.vertices]
        for edge in self.edges:
            if edge is not None:
                [v1, v2] = edge[:2]
                vertex_adjency[v1] += 1
                vertex_adjency[v2] += 1
        self.vertex_adjency = vertex_adjency
        self.vertices_odd = [
            i for i in range(len(self.vertices)) if vertex_adjency[i] % 2 == 1
        ]
        self.adjency_computed = True
        self.is_eulerian_cache = len(self.vertices_odd) == 0

    def is_eulerian(self):
        if not self.adjency_computed:
            self.compute_adjency()
        return self.is_eulerian_cache

    def odd_vertices(self):
        if not self.adjency_computed:
            self.compute_adjency()
        return self.vertices_odd

    def next(self, input_edge_index: int, vertex_index: int):
        for i, edge in enumerate(self.edges):
            if i == input_edge_index or edge is None:
                continue  # Actually not necessary for Hierholzer since we remove the edge before computing the next
            if edge[0] == vertex_index:
                return [i, edge[1]]
            if edge[1] == vertex_index:
                return [i, edge[0]]
        return [-1, None]

    # TODO instead of None, add a boolean to mark the edge as visited
    # no need to clone this way
    # prevents all the "if edge is None" in the code
    def remove_edge(self, index):
        if not self.adjency_computed:
            self.compute_adjency()
        edge = self.edges[index]
        self.vertex_adjency[edge[0]] -= 1
        self.vertex_adjency[edge[1]] -= 1
        self.edges[index] = None

    def add_virtual_edge(
        self, v1_index: int, v2_index: int, weight: int, path: list[True_Edge]
    ):
        [v1, v2] = [self.vertices[v1_index], self.vertices[v2_index]]
        new_edge: Virtual_Edge = (v1_index, v2_index, weight, v1, v2, path)
        self.edges.append(new_edge)
        self.adjency_computed = False

    def has_unvisited_edges(self):
        if not self.adjency_computed:
            return len(self.edges) > 0
        for e in self.edges:
            if e is not None:
                return True
        return False

    def is_hub(self, vertex):
        if not self.adjency_computed:
            self.compute_adjency()
        return self.vertex_adjency[vertex] > 0

    # Probably a standard method somewhere
    def matrix(self):
        n = len(self.vertices)
        matrix = [[0 for i in range(n)] for i in range(n)]
        for edge in self.edges:
            if edge is not None:
                [i, j, weight] = [edge[0], edge[1], edge[2]]
                matrix[i][j] = weight
                matrix[j][i] = weight
        return csr_array(matrix)

    def clone(self):
        g = Graph(
            [vertex for vertex in self.vertices], [edge for edge in self.real_edges]
        )
        g.real_edges = g.edges
        g.edges = [edge for edge in self.edges]
        return g
