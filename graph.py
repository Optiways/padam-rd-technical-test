from __future__ import annotations

from enum import nonmember

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

## Solve some recursion issues
import sys
sys.setrecursionlimit(5000)

import logging

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

        #Logger configuration
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.info("Graph initialized with %d vertices and %d edges.", len(vertices), len(edges))

        # Solution path
        self.path = None
        self.silly_path = None

        # For connectivity
        self.adj_list = None
        self.build_adj_list()
        self.is_connect = self.is_connected()

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

    def build_adj_list(self):
        """
        Build an adjacency list representation of the graph.

        Returns
        -------
        dict
            A dictionary where keys are vertex ids and values are sets of adjacent vertex ids.
        """
        self.logger.info("Building a adjacency list.")
        self.adj_list = {i: set() for i in range(len(self.vertices))}
        for edge in self.edges:
            v1, v2, _, _, _ = edge
            self.adj_list[v1].add(v2)
            self.adj_list[v2].add(v1)  # Since the graph is undirected
        self.logger.info("Adjacency list built. Leaving build_adj_list")
        return self.adj_list

    def print_adj_list(self):
        """
        Prints the adjacency list of the graph.
        """
        print("Adjacency List:")
        for vertex, neighbors in self.adj_list.items():
            print(f"Vertex {vertex}: {sorted(neighbors)}")

    def is_connected(self):
        """
        Check if the graph is connected. If not, return the connected components.

        Returns
        -------
        bool
            True if the graph is connected, False otherwise.
        list[dict]
            A list of connected components' adjacency lists if the graph is not connected.
        """
        self.logger.info("Checking if the graph is connected.")
        adj_list = self.build_adj_list()
        visited = [False] * len(self.vertices)  # List to track visited vertices
        connected_components = []  # List to store connected components' adjacency lists

        def dfs(vertex, component_vertices):
            """Recursive DFS function to visit all vertices in the same component."""
            visited[vertex] = True
            component_vertices.append(vertex)
            for neighbor in adj_list[vertex]:
                if not visited[neighbor]:
                    dfs(neighbor, component_vertices)

        # Perform DFS starting from each vertex
        for vertex in range(len(self.vertices)):
            if not visited[vertex]:
                component_vertices = []
                dfs(vertex, component_vertices)
                # Now we have the list of vertices for the current component
                component_adj_list = {v: set() for v in component_vertices}
                for edge in self.edges:
                    v1, v2, _, _, _ = edge
                    # Add the edge if both vertices are in the current component
                    if v1 in component_vertices and v2 in component_vertices:
                        component_adj_list[v1].add(v2)
                        component_adj_list[v2].add(v1)
                connected_components.append(component_adj_list)

        # If all vertices were visited in a single DFS, the graph is connected
        if len(connected_components) == 1:
            self.logger.info("The graph is connected. Leaving is_connected.")
            return True, None
        else:
            self.logger.info("The graph is not connected. Returning connected components.")
            return False, connected_components

    def print_silly_path(self):
        """
        Affiche le chemin emprunté dans le graphe (listes d'arêtes parcourues).

        Parameters
        ----------
        path : list[tuple]
            Liste des arêtes parcourues sous forme de tuples (vertex1, vertex2, weight, coord1, coord2).
        """
        if not self.silly_path:
            print("Le chemin est vide.")
            return

        print("Chemin parcouru (listes d'arêtes) :\n")
        for idx, edge in enumerate(self.silly_path):
            vertex1, vertex2, weight, coord1, coord2 = edge
            print(f"Arête {idx + 1}: {vertex1} -> {vertex2} avec poids {weight:.2f}")
            print(f"   Coordonnées : ({coord1[0]}, {coord1[1]}) -> ({coord2[0]}, {coord2[1]})")

    def silly_path(self):
        """
        Create a path in the simplest and most straightforward way.

        Returns
        -------
        list[list[tuple]]
            List of lists of edges, one list for each connected component.
        """
        self.logger.info("Entering silly_path.")

        if not self.edges:
            return []

        edges_to_visit = self.edges[:]       # edges to visit list
        self.silly_path = []                            # crossed edges list

        current_edge = edges_to_visit.pop(0) # Visit the first edge in the list
        self.silly_path.append(current_edge)

        v1, v2, weight, coord1, coord2 = current_edge
        self.logger.debug(
            "Starting with edge: from vertex %d to vertex %d with weight %.2f: Coordinates (%f, %f) -> (%f, %f)",
            v1, v2, weight, coord1[0], coord1[1], coord2[0], coord2[1])

        current_vertex = v1  # Start from the first vertex of the first edge

        # Continue until all edges are visited
        while edges_to_visit:
            for i, edge in enumerate(edges_to_visit):
                vertex1, vertex2, _, _, _ = edge
                # We traverse an edge if one of its vertices matches the current vertex
                if vertex1 == current_vertex:
                    self.silly_path.append(edge)
                    current_vertex = vertex2
                    #logging
                    v1, v2, weight, coord1, coord2 = edge
                    self.logger.debug("New edge: from vertex %d to vertex %d with weight %.2f: Coordinates (%f, %f) -> (%f, %f)",
                        v1, v2, weight, coord1[0], coord1[1], coord2[0], coord2[1])
                    break
                elif vertex2 == current_vertex:
                    self.silly_path.append(edge)
                    current_vertex = vertex1
                    #logging
                    v1, v2, weight, coord1, coord2 = edge
                    self.logger.debug("New edge: from vertex %d to vertex %d with weight %.2f: Coordinates (%f, %f) -> (%f, %f)",
                        v1, v2, weight, coord1[0], coord1[1], coord2[0], coord2[1])
                    break
            else:
                self.logger.info("All edges have been traversed.")
                break
