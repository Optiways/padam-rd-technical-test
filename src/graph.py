from __future__ import annotations
from collections import defaultdict, deque
from copy import deepcopy

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

Coordinates = tuple[float, float]
Edge = tuple[int, int, int, Coordinates, Coordinates]


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
        self.adj_list = [set() for _ in range(len(vertices))]
        self.edge_map = defaultdict(Edge)
        self.build_adjacency_list()

    def build_adjacency_list(self):
        self.adj_list = [set() for _ in range(len(self.vertices))]
        self.edge_map = defaultdict(Edge)
        # i is used as a unique id for edges as islands.txt containst parallel edges
        for i, edge in enumerate(self.edges):
            self.adj_list[edge[0]].add((edge[1], i))
            self.adj_list[edge[1]].add((edge[0], i))
            self.edge_map[(edge[0], edge[1], i)] = edge
            self.edge_map[(edge[1], edge[0], i)] = edge

    def get_odd_vertices(self) -> list[int]:
        return [i for i, u in enumerate(self.adj_list) if len(u) % 2]

    def is_connected(self) -> bool:
        """Check full connectivity in graph using BFS search"""
        return self.extract_connected_vertices() == set(
            range(len(self.vertices))
        )

    def extract_connected_vertices(self, start: int = 0) -> set[int]:
        """BFS search for connectivity in graph"""
        open = deque([start])
        closed = set()
        while open:
            current = open.pop()
            closed.add(current)
            for adj in self.adj_list[current]:
                if adj[0] not in closed:
                    open.append(adj[0])
        return closed

    def extract_connected_subgraphs(self) -> list[Graph]:
        """Extract a list of connected subgraph of self using BFS search.
        Vertex indices in subgraph are then rescaller to range(0,n)"""
        nodes = set(range(len(self.vertices)))
        ret = []
        while nodes:
            sub = self.extract_connected_vertices(nodes.pop())
            vertices = [self.vertices[i] for i in sub]
            edges = [e for e in self.edges if e[0] in sub or e[1] in sub]
            old = list({e[0] for e in edges} | {e[1] for e in edges})
            edge_dict = {o: i for i, o in enumerate(old)}
            for i, e in enumerate(edges):
                edges[i] = (edge_dict[e[0]], edge_dict[e[1]], e[2], e[3], e[4])
            ret.append(deepcopy(Graph(vertices, edges)))
            nodes -= sub
        return ret

    def plot(self):
        """
        Plot the graph.
        """
        weights = list(set(edge[2] for edge in self.edges))
        colors = plt.cm.get_cmap("viridis", len(weights))
        _, ax = plt.subplots()
        for i, weight in enumerate(weights):
            lines = [
                [edge[-2][::-1], edge[-1][::-1]]
                for edge in self.edges
                if edge[2] == weight
            ]
            ax.add_collection(
                LineCollection(
                    lines,
                    colors=colors(i),
                    alpha=0.7,
                    label=f"weight {weight}",
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
                ax.annotate(
                    str(edge_index),
                    xytext=edge[3],
                    xy=edge[4],
                    arrowprops=dict(arrowstyle="->", color=colors(path_index)),
                )
        plt.show()
