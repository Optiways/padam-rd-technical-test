from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def vertices_degree(edge, size):
    """
    Returning a list containing the degree of each vertices
    """
    degrees = [0]*size
    for first_vertex, second_vertex, *_ in edge:
        degrees[first_vertex] += 1
        degrees[second_vertex] += 1
    
    return degrees

def odd_even(degrees):
    """
    Returning the index of odd and even vertices as two lists
    """
    odd = []
    even = []
    for index, value in enumerate(degrees):
        if value%2 == 0: even.append(index)
        else: odd.append(index)

    return odd, even

def distance(graph, start, end):
    pass
    #TO DO
            

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
        self.adjacency_list = [[] for n in range(len(self.vertices))]
        for i, j, weight, *_ in self.edges:
            if not (i, j, weight) in self.adjacency_list[i]:
                self.adjacency_list[i].append((i, j, weight))
            if not (j, i, weight) in self.adjacency_list[j]:
                self.adjacency_list[j].append((j, i, weight))

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

    def get_optimal_path(self):
        odd, _ = odd_even(vertices_degree(self.edges, len(self.vertices)))
        print(odd)
        if len(odd) <= 2:
            if not(odd):
                return self.get_eulerian_path(1)
            else:
                return self.get_eulerian_path(odd[0])
        
        else:
            virtual_edges = [(odd[index], 
                              odd[index+1], 
                              distance(self.adjacency_list, odd[index], odd[index+1]),
                              self.vertices[odd[index]],
                              self.vertices[odd[index+1]]
                              ) for index in range(len(odd)//2)]
            
            virtual_graph = Graph(self.vertices, self.edges + virtual_edges)
            return virtual_graph.get_eulerian_path(odd[0])



    def get_eulerian_path(self, start):

        stack = [start]
        path = []
        total_weight = 0

        while stack:
            current_vertex = stack[-1]
            if self.adjacency_list[current_vertex]:
                edge = self.adjacency_list[current_vertex].pop()
                self.adjacency_list[edge[1]].remove((edge[1], edge[0], edge[2]))
                stack.append(edge[1])
                total_weight+= edge[2]
            else:
                path.append(stack.pop())

        self.eulerian_path = path
        self.total_weight = total_weight
        return path, total_weight
            

