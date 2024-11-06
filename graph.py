from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import heapq
import random


class Graph:
    def __init__(self,
                 vertices: list[tuple],
                 edges: list[tuple],
                 vertices_ids: list[int],
                 edges_ids: list[tuple[int, int]],
                 weights_matrix: np.ndarray):
        """
        Parameters
        ----------
        vertices : list[tuple]
            list of vertices coordinates.
        edges : list[tuple]
            list of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
        vertices_ids : list[int]
            list of the ids of the vertices.
        edges_ids : list[tuple[int, int]]
            list of the edges as tuple (id 1, id 2).
        weights_matrix : np.ndarray
            matrix of weights of each edge (the value on the i-th line and the j-th column is the weigth of the edge between vertex i and vertex j).
        """
        self.vertices = vertices
        self.edges = edges
        self.vertices_ids = vertices_ids
        self.edges_ids = edges_ids
        self.weights_matrix = weights_matrix
        self.visited_edges = []


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


    def select_vertex_max_edges(self) -> int:
        """
        Select the vertex with the most edges.

        Returns
        -------
        tuple[int, int]
        """
        non_zeros_mask = self.weights_matrix != 0
        numbers_of_edges = np.sum(non_zeros_mask, axis=1)
        return np.argmax(numbers_of_edges)


    def get_nearest_neighbor(self,
                     vertex : int) -> int:
        """
        Get the neighbor of the vertex with unvisited edge with minimal weight.

        Parameters
        ----------
        vertex : int
            id of the vertex from which the edge has to be linked.

        Returns
        -------
        int
            id of the neighbor of the vertex linked by the unvisited edge with minimal weight.
        """
        # Determine the list of unvisited neighbors of vertex
        vertex_weights_edges = self.weights_matrix[vertex, :]
        unvisited_neighbors = [j for j in range(len(vertex_weights_edges))
                                 if (vertex,j) not in self.visited_edges
                                    and (j, vertex) not in self.visited_edges
                                    and vertex_weights_edges[j]!=0]

        if unvisited_neighbors:
            # if there are unvisited neighbors, select the neighbor linked by smallest weight
            neighbor = unvisited_neighbors[np.argmin(vertex_weights_edges[unvisited_neighbors])]
            return neighbor

        return None


    def shortest_path(self, start_vertex: int, target_vertex: int) -> list[int]:
        """
        Determine the shortest path between start_vertex and target_vertex using Dijkstra algorithm.

        Parameters
        ----------
        start_vertex : int
            id of the start vertex
        target_vertex : int
            if of the target vertex

        Returns
        -------
        list[int]
            path from start_vertex to target_vertex with lowest weight
        """
        # initialization of distances
        distances = {v: float('infinity') for v in range(len(self.vertices))}
        distances[start_vertex] = 0

        # initialization of the queue of vertices to explore
        queue = [(0, start_vertex)]
        previous_vertices = {v: None for v in range(len(self.vertices))}

        while queue:
            current_distance, current_vertex = heapq.heappop(queue)

            if current_distance > distances[current_vertex]:
                continue

            # explore neighbors of current_vertex
            for neighbor in range(len(self.weights_matrix[current_vertex])):
                weight = self.weights_matrix[current_vertex][neighbor]
                if weight > 0:  # if a edge exists
                    distance = current_distance + weight
                    if distance < distances[neighbor]:
                        # actualize distances and path to go to the neighbor
                        distances[neighbor] = distance
                        previous_vertices[neighbor] = current_vertex
                        # update queue
                        heapq.heappush(queue, (distance, neighbor))

        # get the path to go to target_vertex
        path = []
        while target_vertex is not None:
            path.append(target_vertex)
            target_vertex = previous_vertices[target_vertex]
        path.reverse()

        return path if distances[path[-1]] != float('infinity') else []


    def is_connected(self) -> bool:
        """
        Verify that all the vertices are connected. If it is not, we can't find a path that cover every edge !

        Returns
        -------
        bool
            True if graph is connected, False else.
        """
        start_vertex = 0
        visited = set()
        stack = [start_vertex]

        # DFS
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                # Add unvisited neighbors to stack
                for neighbor in range(len(self.weights_matrix[vertex])):
                    if self.weights_matrix[vertex][neighbor] > 0 and neighbor not in visited:
                        stack.append(neighbor)

        # If all vertices are covered, graph is connex, else it's not
        return len(visited) == len(self.vertices)


    def get_path(self) -> tuple[list[int], int]:
        """
        Find a path that cover all edges of the graph.

        Returns
        -------
        tuple[list[int], int]
            list of vertices in the order of the path, cost of the path.
        """
        # choose the first vertex
        vertex = self.select_vertex_max_edges()
        # initialize path and path_cost
        path = [vertex]
        path_cost = int(0)

        while len(self.visited_edges)<len(self.edges_ids):
            # while every edges haven't been visited, extend the path

            neighbor = self.get_nearest_neighbor(vertex)

            if neighbor:
                # if current vertex has neighbors with unvisited edge, go to nearest unvisited neighbor
                path.append(neighbor) # actualize path
                path_cost += self.weights_matrix[vertex, neighbor] # actualize path_cost
                self.visited_edges.append((vertex, neighbor)) # actualize visited edges
                vertex = neighbor # actualize current vertex

            else:
                # if vertex has no neighbors with unvisited edge, select an unvisited edge and go there
                unvisited_edges = [(u, v) for u, v in self.edges_ids
                                          if (u, v) not in self.visited_edges
                                            and (v, u) not in self.visited_edges]

                if unvisited_edges:
                    # choose aleatorly an unvisited edge
                    # TO DO : determine how to choose judiciously the next edge to visit
                    random_edge = random.choice(unvisited_edges)
                    # choose the first vertex of this edge
                    # TO DO : change the code to choose the nearest vertex of the selected edge from the current vertex
                    target_vertex = random_edge[0]
                    # determine shortest path between vertex and target_vertex
                    shortest_path_to_target_vertex = self.shortest_path(vertex, target_vertex)
                    if shortest_path_to_target_vertex:
                        # actualize path, path_cost and visited_edges
                        for i in range(len(shortest_path_to_target_vertex) - 1):
                            path.append(shortest_path_to_target_vertex[i + 1])
                            path_cost += self.weights_matrix[shortest_path_to_target_vertex[i], shortest_path_to_target_vertex[i + 1]]
                            if ((shortest_path_to_target_vertex[i], shortest_path_to_target_vertex[i + 1]) not in self.visited_edges) \
                                and ((shortest_path_to_target_vertex[i+1], shortest_path_to_target_vertex[i]) not in self.visited_edges):
                                # if the edge hasn't been visited, add it to visited_edges
                                self.visited_edges.append((shortest_path_to_target_vertex[i], shortest_path_to_target_vertex[i + 1]))
                        vertex = shortest_path_to_target_vertex[-1]
                    else:
                        continue

                else:
                    break

        return path, int(path_cost)
