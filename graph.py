from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


class Graph:
    """Class used to describe a graph with a list of vertices and a list of edges between those vertices."""

    def __init__(self, vertices: list[tuple], edges: list[tuple]):
        """Basic constructor of the `Graph` class.

        Parameters
        ----------
        vertices : list[tuple]
            List of vertices coordinates.

        edges : list[tuple]
            List of edges as tuple (id 1, id 2, distance, coordinates 1, coordinates 2).
        """
        self.vertices = vertices
        self.edges = edges

    def plot(self):
        """Plots this graph."""
        distances = list(set(edge[2] for edge in self.edges))
        colors = plt.cm.get_cmap("viridis", len(distances))
        _, ax = plt.subplots()
        for i, distance in enumerate(distances):
            lines = [[edge[-2][::-1], edge[-1][::-1]] for edge in self.edges if edge[2] == distance]
            ax.add_collection(LineCollection(lines, colors=colors(i), alpha=0.7, label=f"distance {distance}"))
        ax.plot()
        ax.legend()
        plt.title(f"#E={len(self.edges)}, #V={len(self.vertices)}")
        plt.show()
