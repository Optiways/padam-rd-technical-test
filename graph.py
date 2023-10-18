from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np


class Graph:
    def __init__(self, vertices: list[tuple], edges: list[tuple]):
        """
        Parameters
        ----------
        vertices : list[tuple]
            list of vertices coordinates.
        edges : list[tuple]
            list of edges as tuple (idEdge, id 1, id 2, weight, coordinates 1, coordinates 2).
        """
        self.vertices = vertices
        self.edges = edges
        self.degrees = [0 for _ in range(len(vertices))]
        self.adjacencyMatrix = [[0 for _ in range(len(vertices))] for _ in range(len(vertices))]
        for edge in edges:
            self.degrees[edge[1]] += 1
            self.degrees[edge[2]] += 1
            if self.isConnex_non_recursive():
                self.adjacencyMatrix[edge[1]][edge[2]] = edge[3]
                self.adjacencyMatrix[edge[2]][edge[1]] = edge[3]
        self.max_degree = max(self.degrees)
        
        if self.isConnex_non_recursive():
            self.distances = [[0 for _ in range(len(vertices))] for _ in range(len(vertices))]
            self.shortestPaths = [[[] for _ in range(len(vertices))] for _ in range(len(vertices))]
            for i in range(len(vertices)):
               self.dijkstra(i)
        print("Graph initialised")
    
    def get_adjacent_edges(self, vertice):
        adjacent_edges = []
        for edge in self.edges:
            if vertice == edge[1] or vertice == edge[2]:
               adjacent_edges.append(edge)
        return adjacent_edges

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
        plt.savefig("tmp.png")
        
    def minDistance(self, dist, sptSet):
        # Initialize minimum distance for next node
        min = 1e7
 
        # Search nearest vertex not in the
        # shortest path tree
        for v in range(len(self.vertices)):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
        
    def dijkstra(self, src): ## to compute shortest paths between
                             ## the vertices of the graph
        self.distances[src] = [np.inf] * len(self.vertices)
        self.distances[src][src] = 0
        self.shortestPaths[src][src] = [src]
        sptSet = [False] * len(self.vertices)
 
        for _ in range(len(self.vertices)):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(self.distances[src], sptSet)
 
            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(len(self.vertices)):
                if (self.adjacencyMatrix[u][v] > 0 and
                   sptSet[v] == False and
                   self.distances[src][v] > self.distances[src][u] + self.adjacencyMatrix[u][v]):
                    self.distances[src][v] = self.distances[src][u] + self.adjacencyMatrix[u][v]
                    self.shortestPaths[src][v] = self.shortestPaths[src][u] + [v]
                    
    def DFSUtil(self, v, visited):
 
        visited[v] = True # Mark the current node as visited
        adjEdges = self.get_adjacent_edges(v) #all the vertices adjacent to this vertex
        for edge in adjEdges:
            neighbour = -1
            if edge[1] == v and visited[edge[2]] == False:
                neighbour = edge[2]
            if edge[2] == v and visited[edge[1]] == False:
                neighbour = edge[1]
            if neighbour != -1:
                self.DFSUtil(neighbour, visited) # recurvivity
    def isConnex(self):
        visited = [False for _ in range(len(self.vertices))]
        self.DFSUtil(0, visited) # calling recursively the function starting at 0 
        return (sum(visited) == len(visited))
                
    def Non_Recursive_dfs(self, v, visited, temp): # recursivity is too long for paris_map
        stack = [v]
        temp.append(v)

        while stack:
            vertex = stack.pop()
            if visited[vertex]:
                continue
            
            visited[vertex] = True
            adjEdges = self.get_adjacent_edges(vertex)
            for edge in adjEdges:
                neighbour = -1
                if edge[1] == v and visited[edge[2]] == False:
                    neighbour = edge[2]
                    temp.append(neighbour)
                    stack.append(neighbour)
                if edge[2] == v and visited[edge[1]] == False:
                    neighbour = edge[1]
                    temp.append(neighbour)
                    stack.append(neighbour)
     
    
    def isConnex_non_recursive(self):
        visited = [False for _ in range(len(self.vertices))]
        temp = []
        self.Non_Recursive_dfs(0, visited, temp)
        return (sum(visited) == len(visited))
    
    def connected_part(self): ## retrieve all the connected part in a not connected graph
        visited = [False for _ in range(len(self.vertices))]
        cc = []
        for v in range(len(self.vertices)):
            if visited[v]:
                continue
            temp = []
            self.Non_Recursive_dfs(v, visited, temp)
            cc.append(temp)
        return cc