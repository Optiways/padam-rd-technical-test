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
        colors = plt.cm.get_cmap("viridis", len(weights))
        _, ax = plt.subplots()
        for i, weight in enumerate(weights):
            lines = [[edge[-2][::-1], edge[-1][::-1]] for edge in self.edges if edge[2] == weight]
            ax.add_collection(LineCollection(lines, colors=colors(i), alpha=0.7, label=f"weight {weight}"))
        ax.plot()
        ax.legend()
        plt.title(f"#E={len(self.edges)}, #V={len(self.vertices)}")
        plt.show()


    def build_neighbors(self) -> dict[[tuple], list[tuple]]:
        """
        Create a dictionary with the list of neighbors of each vertex.

        Returns
        -------
        dict[[tuple], list[tuple]]
            dictionary that associate to each vertex its list of neighbors
            {
                (vertex1_coordinate_x, vertex1_coordinate_y):
                    [(neighbor1_coordinate_x, neighbor2_coordinate_y), (neighbor2_coordinate_x, neighbor2_coordinate_y), ...],
                ...
            }
        """
        # Initialiser un dictionnaire pour les voisins avec chaque sommet ayant une liste vide au départ
        neighbors = {vertex: [] for vertex in self.vertices}
        
        # Ajouter les voisins pour chaque arête
        for edge in self.edges:
            id1, id2, weight, coord1, coord2 = edge
            neighbors[coord1].append(coord2)
            neighbors[coord2].append(coord1)

        return neighbors