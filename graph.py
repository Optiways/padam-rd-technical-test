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
        self.degrees = self.compute_degrees()
        self.connected_subgraphs = []

    def compute_degrees(self) -> dict:
        "Compute the degree of every vertices"
        degrees = {self.vertices[idx]: 0 for idx in range(len(self.vertices))}
        for edge in self.edges:
            degrees[edge[3]] += 1
            degrees[edge[4]] += 1
        return degrees

    def compute_odd_list(self) -> list[tuple]:
        "Return a list of all the odd degree vertices"
        odd_list = []
        for vertex in self.vertices:
            if self.degrees[vertex] % 2:
                odd_list.append(vertex)
        return odd_list

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
        ax.scatter([v[1] for v in self.vertices], [v[0] for v in self.vertices])
        ax.legend()
        plt.title(f"#E={len(self.edges)}, #V={len(self.vertices)}")
        plt.show()


    def get_connected_subgraphs(self):
        "Create all the connected subgraphs from the initial graph"
        # TODO : iterate to create multiple subgraphs
        visited = []
        connected_edges = self.dfs(self.vertices[0], visited)
        self.connected_subgraphs.append(Graph(visited, connected_edges))

    def dfs(self, v_start: tuple, visited: list = []):
        "Compute the Depth-First Search from the vertex v_start"
        if self.degrees[v_start] == 0:
            # the vertex is not connected to any other vertices.
            visited.append(v_start)
            return []
        
        if v_start not in visited:
            visited.append(v_start)
            neighbors = [edge[4] for edge in self.edges if edge[3] == v_start] + [edge[3] for edge in self.edges if edge[4] == v_start]
            for neighbor in neighbors:
                self.dfs(neighbor, visited)
        
        connected_edges = []
        for vertex in visited:
            connected_edges += [edge for edge in self.edges if vertex == edge[3]]
        return connected_edges
    
    def is_bridge(self, edge) -> bool:
        "check if an edge is a bridge by computing a dfs, to avoid bridges in the euler path"
        new_edges = self.edges.copy()
        new_edges.remove(edge)
        new_graph = Graph(self.vertices, new_edges)
        visited_vertices = []
        _ = new_graph.dfs(new_graph.vertices[0], visited_vertices)
        if len(visited_vertices) != len(new_graph.vertices):
            return True
        return False