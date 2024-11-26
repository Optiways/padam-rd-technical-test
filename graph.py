from collections import defaultdict
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from tqdm import tqdm

import sys
# Increase the recursion limit for is_connected 
sys.setrecursionlimit(10000) 

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
        self.adjacency_list = self.build_adjacency_list()
        self.odd_vertices = []

    def is_connected(self):
        """
        Check if the graph is connected using Depth First Search (DFS).
        Returns True if the graph is connected, False otherwise.
        """
        visited = [False] * len(self.vertices)

        def dfs(node):
            visited[node] = True
            for neighbor, _ in self.adjacency_list[node]:
                if not visited[neighbor]:
                    dfs(neighbor)

        # Start DFS from the first vertex
        dfs(0)

        # If all vertices are visited, the graph is connected
        return all(visited)


    def build_adjacency_list(self):
        """
        Build adjacency list for the graph.
        """
        adj_list = defaultdict(list)
        for u, v, weight, _, _ in self.edges:
            adj_list[u].append((v, weight))
            adj_list[v].append((u, weight))
        return adj_list

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

    def find_odd_degree_vertices(self):
        """
        Identify vertices with odd degree.
        """
        self.odd_vertices = [v for v, neighbors in self.adjacency_list.items() if len(neighbors) % 2 == 1]
        return self.odd_vertices

    def compute_shortest_paths(self):
        """
        Compute shortest paths between all pairs of vertices.
        Returns a dictionary of shortest distances.
        """
        num_vertices = len(self.vertices)
        dist = {i: {j: float("inf") for j in range(num_vertices)} for i in range(num_vertices)}
        for i in range(num_vertices):
            dist[i][i] = 0
        for u, v, weight, _, _ in self.edges:
            dist[u][v] = weight
            dist[v][u] = weight

        for k in range(num_vertices):
            for i in range(num_vertices):
                for j in range(num_vertices):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist

    def compute_shortest_paths_faster(self, odd_vertices):
        """
        Compute shortest paths between all odd vertices using Dijkstra's algorithm.
s
        I chose Dijkstra's algorithm because the previous algorithm has a time complexity of O(V^3),
        which is too slow for large graphs.

        Returns a dictionary of shortest distances.
        """
        distances = {}
        for src in tqdm(odd_vertices, desc="Computing shortest paths"):
            # Initialize distances and visited set
            dist = {i: float("inf") for i in range(len(self.vertices))}
            dist[src] = 0
            visited = set()

            while len(visited) < len(self.vertices):
                # Find the unvisited vertex with the smallest distance
                current_vertex = None
                current_distance = float("inf")
                for vertex in range(len(self.vertices)):
                    if vertex not in visited and dist[vertex] < current_distance:
                        current_vertex = vertex
                        current_distance = dist[vertex]

                # If no such vertex exists, stop
                if current_vertex is None:
                    break

                # Mark the vertex as visited
                visited.add(current_vertex)

                # Update distances to neighbors
                for neighbor, weight in self.adjacency_list[current_vertex]:
                    if neighbor not in visited:
                        new_distance = dist[current_vertex] + weight
                        if new_distance < dist[neighbor]:
                            dist[neighbor] = new_distance

            distances[src] = dist

        return distances


    def minimum_weight_matching(self, odd_vertices, distances):
        """
        Perform minimum weight matching on the odd degree vertices using shortest path distances.
        Returns a list of edges to add to the graph.
        """
        pairs = list(combinations(odd_vertices, 2))
        pairs = sorted(pairs, key=lambda x: distances[x[0]][x[1]])

        matched = set()
        matching = []
        for u, v in pairs:
            if u not in matched and v not in matched:
                matching.append((u, v, distances[u][v]))
                matched.update([u, v])

        return matching

    def augment_graph(self, matching):
        """
        Augment the graph by adding duplicate edges from the matching.
        """
        for u, v, weight in matching:
            self.edges.append((u, v, weight, self.vertices[u], self.vertices[v]))
            self.adjacency_list[u].append((v, weight))
            self.adjacency_list[v].append((u, weight))

    def eulerian_path(self):
        """
        Compute Eulerian path using Hierholzer's algorithm.
        Returns the path and the total weight.
        """
        adj_list = defaultdict(list, {k: v[:] for k, v in self.adjacency_list.items()})

        stack = []
        circuit = []
        current_vertex = 0

        while stack or adj_list[current_vertex]:
            if not adj_list[current_vertex]:
                circuit.append(current_vertex)
                current_vertex = stack.pop()
            else:
                stack.append(current_vertex)
                next_vertex, _ = adj_list[current_vertex].pop()
                adj_list[next_vertex].remove((current_vertex, _))
                current_vertex = next_vertex

        circuit.append(current_vertex)
        return circuit[::-1], sum(edge[2] for edge in self.edges)

    def solve_problem(self):
        """
        Solve the Problem.
        """

        # Step 0: Check connectivity
        if not self.is_connected():
            raise ValueError("The graph is not connected. Cannot solve the problem.")
        
        # Step 1: Identify odd-degree vertices
        odd_vertices = self.find_odd_degree_vertices()

        # Step 2: Compute shortest paths
        #distances = self.compute_shortest_paths()

        # Step 2BIS: Compute shortest paths
        distances = self.compute_shortest_paths_faster(odd_vertices)
        
        # Step 3: Perform minimum weight matching
        matching = self.minimum_weight_matching(odd_vertices, distances)

        # Step 4: Augment the graph
        self.augment_graph(matching)

        # Step 5: Find Eulerian path
        path, total_weight = self.eulerian_path()
        return path, total_weight
