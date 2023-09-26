from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


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
        print(weights)
        colors = plt.cm.get_cmap("viridis", len(weights))
        _, ax = plt.subplots()
        for i, weight in enumerate(weights):
            lines = [[edge[-2][::-1], edge[-1][::-1]] for edge in self.edges if edge[2] == weight]
            ax.add_collection(LineCollection(lines, colors=colors(i), alpha=0.7, label=f"weight {weight}"))
        ax.plot()
        ax.legend()
        plt.title(f"#E={len(self.edges)}, #V={len(self.vertices)}")
        plt.show()

        # weights = list(set(edge[2] for edge in self.edges))
        # colors = plt.cm.get_cmap("viridis", 3)
        # print(colors)
        # _, ax = plt.subplots()
        # lines = [[edge[-2][::-1], edge[-1][::-1]] for edge in self.edges if (40>edge[0]>= 20 or 40>edge[1]>=20)]
        # ax.add_collection(LineCollection(lines, colors=colors(0),linestyle='dotted', alpha=0.7, label=f"weight {0}"))
        # lines = [[edge[-2][::-1], edge[-1][::-1]] for edge in self.edges if (edge[0]< 20 or edge[1]<20)]
        # ax.add_collection(LineCollection(lines, colors=colors(1),linestyle='dotted', alpha=0.7, label=f"weight {1}"))
        # lines = [[edge[-2][::-1], edge[-1][::-1]] for edge in self.edges if (edge[0]> 40 or edge[1]>40)]
        # ax.add_collection(LineCollection(lines, colors=colors(2),linestyle='dotted', alpha=0.7, label=f"weight {2}"))
        # ax.plot()
        # ax.legend()
        # plt.title(f"#E={len(self.edges)}, #V={len(self.vertices)}")
        # plt.show()
