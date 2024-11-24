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
        self.path_list = None

        # For connectivity
        self.adj_list = None
        self.build_adj_list()
        self.is_connect, self.adj_lists = self.is_connected()

        self.path_weight = 0

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
        if self.adj_lists is None:
            print("Adjacency List:")
            for vertex, neighbors in self.adj_list.items():
                print(f"Vertex {vertex}: {sorted(neighbors)}")
        else:
            i = 1
            for adj_list in self.adj_lists:
                print("Adjacency List: " + str(i))
                for vertex, neighbors in adj_list.items():
                    print(f"Vertex {vertex}: {sorted(neighbors)}")
                i+=1

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
            self.logger.info("The graph is not connected. Returning connected components. Leaving is_connected.")
            return False, connected_components

    def print_silly_path(self):
        """
        Affiche le chemin emprunté dans le graphe (listes d'arêtes parcourues).

        Parameters
        ----------
        path : list[tuple]
            Liste des arêtes parcourues sous forme de tuples (vertex1, vertex2, weight, coord1, coord2).
        """
        if not self.path:
            print("Le chemin est vide.")
            return

        print("Chemin parcouru (listes d'arêtes) :\n")
        for idx, edge in enumerate(self.path):
            vertex1, vertex2, weight, coord1, coord2 = edge
            print(f"Arête {idx + 1}: {vertex1} -> {vertex2} avec poids {weight:.2f}")
            print(f"   Coordonnées : ({coord1[0]}, {coord1[1]}) -> ({coord2[0]}, {coord2[1]})")

    def get_edge_weight(self, edge):
        """
        Returns the weight of the edge given by the tuple (u, v).
        """
        u, v = edge
        for e in self.edges:
            if (e[0] == u and e[1] == v) or (e[0] == v and e[1] == u):
                return e[2]
        return None

    def silly_path(self):
        """
        Create paths using a stupid approach, visiting all edges at least once.
        Handles both connected and non-connected graphs.

        Returns
        -------
        list[list[tuple]]
            A list of paths, one for each connected component.
            Each path is a list of edges traversed.
        """
        self.logger.info("Entering silly_path.")

        # Vérifier si le graphe est connexe ou non
        adj_lists = self.adj_lists if self.adj_lists is not None else [self.adj_list]
        self.path_list = []

        def find_unvisited_edge():
            """
            Find the nearest unvisited edge in this component.
            Returns a tuple (path_to_vertex, unvisited_edge), or (None, None) if no such edge exists.
            """
            queue = [(current_vertex, [])]  # (vertex, path to that vertex)
            visited_vertices = set()

            while queue:
                vertex, path = queue.pop(0)
                visited_vertices.add(vertex)

                # Check if this vertex has an unvisited edge
                for neighbor in adj_list[vertex]:
                    edge = tuple(sorted((vertex, neighbor)))
                    if edge not in visited_edges:
                        return path + [vertex], (vertex, neighbor)

                # Add neighbors to explore further
                for neighbor in adj_list[vertex]:
                    if neighbor not in visited_vertices:
                        queue.append((neighbor, path + [vertex]))

            return None, None

        # Looping for each connected component
        for component_id, adj_list in enumerate(adj_lists):
            self.logger.info(f"Processing connected component {component_id + 1}/{len(adj_lists)}.")

            # Initialization
            path = []
            visited_edges = set()
            current_vertex = next(iter(adj_list))
            total_edges = sum(len(neighbors) for neighbors in adj_list.values()) // 2

            self.logger.debug(f"Starting at vertex {current_vertex} in component {component_id + 1}.")



            # Create path in this component
            while len(visited_edges) < total_edges:
                possible_edges = []

                # Find unvisited edges from this vertex
                for neighbor in adj_list[current_vertex]:
                    edge = tuple(sorted((current_vertex, neighbor)))
                    if edge not in visited_edges:
                        possible_edges.append((neighbor, edge))

                if not possible_edges:  # No unvisited edge available
                    self.logger.debug(
                        f"No new unvisited edges from vertex {current_vertex}. Finding a path to an unvisited edge."
                    )

                    # Find a path onto an unvisited vertex
                    path_to_unvisited, unvisited_edge = find_unvisited_edge()
                    if not unvisited_edge:
                        self.logger.error(f"No unvisited edges found in component {component_id + 1}.")
                        break

                    # Add the path to go to the unvisited vertex
                    for i in range(len(path_to_unvisited) - 1):
                        u, v = path_to_unvisited[i], path_to_unvisited[i + 1]
                        edge = tuple(sorted((u, v)))
                        path.append(edge)  # Add already visited edge to the path
                        self.path_weight += self.get_edge_weight(edge)
                        visited_edges.add(edge)
                        self.logger.debug(f"Revisiting edge: {edge} to reach unvisited edge.")

                    # Go to unvisited edge's vertex
                    current_vertex = unvisited_edge[0]
                    continue

                # Take the lightest edge between all
                neighbor, edge = min(possible_edges, key=lambda x: self.get_edge_weight(x[1]))
                path.append(edge)
                self.path_weight += self.get_edge_weight(edge)
                visited_edges.add(edge)

                # Go to neighbor
                current_vertex = neighbor
                self.logger.debug(f"Traversed edge: {edge}, moved to vertex {neighbor}.")

            # Add the path to the path list (for unconnected graph, the list is > 1 path)
            self.path_list.append(path)
            self.logger.info(f"Finished processing component {component_id + 1}. Path length: {len(path)} edges.")

        self.logger.info("Leaving silly_path.")
        return self.path_list

    def checker(self):
        left_edges = []
        for edge in self.edges:
            left_edges.append((edge[0], edge[1]))
        for path in self.path_list:
            for edge in path:
                if edge in left_edges:
                    left_edges.remove(edge)
                elif edge[::-1] in left_edges:
                    left_edges.remove(edge[::-1])


        if len(left_edges) == 0:
            self.logger.info("The checker says, all edges are visited")
        else:
            self.logger.error("The checker says, all edges are NOT visited")
            print(left_edges)