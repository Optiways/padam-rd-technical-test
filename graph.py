from __future__ import annotations
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import time
import copy


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
        
    def __copy__(self):
        return type(self)(self.vertices, self.edges)

###################################################################################################

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


###################################################################################################
        """
        PROCESSING GRAPH: Transform graph to an Eulerian graph
        TODO: Should format all this in different files and import to the class for readability
        """
###################################################################################################
        
    def clean_data(self):
        """
        remove duplicates from data
        """
        seen = set()
        filt = []
        for data in self.edges:
            pair = (data[0], data[1])
            if pair not in seen:
                filt.append(data)
                seen.add(pair)
        self.edges = filt

    def get_adjacent_vert(self):
        """
        Returns:
            adj: dict{int: list(int)}
                Reprensents each vertex with all adjacent vertices listed
        """
        adj = {}

        for id1, id2, weight, _, _ in self.edges:
            # Ensure both vertices exist in the adjacency list
            if id1 not in adj:
                adj[id1] = []
            if id2 not in adj:
                adj[id2] = []

            # Add the edges in both directions since the graph is undirected
            adj[id1].append((id2, weight))
            adj[id2].append((id1, weight))
        return adj

    def get_odd_vertices(self):
        """
        Find all odd degree vertices in the dataset
        ----------
        Returns
        vertices_odd : dict{int: int}
                dict of odd degree vertices with number of degrees (index: vertex id, value: number of edges).
        """
        vertices_odd = {}
        # TODO: probably a faster way to do this 
        for i, j, _, _, _ in self.edges:  # check both vertex indexes on each edge
            if i not in vertices_odd: 
                vertices_odd[i] = 1
            else:
                vertices_odd[i] += 1
            if j not in vertices_odd:
                vertices_odd[j] = 1
            else:
                vertices_odd[j] += 1

        vertices_odd = {key: value for key, value
                        in vertices_odd.items() if value % 2 != 0}

        return vertices_odd


    def shortest_paths(self, vertices_odd):
        """
        Find the shortest paths between all odd degree vertices

        Parameters
            graph : dict{int: list[int]}
                dict of each vertex with all adjacent vertices (index: vertex id, value: vertex index, weight).
            vertices_odd : dict{int: int}
                dict of odd degree vertices with number of degrees (index: vertex id, value: number of edges).

        Returns
        -------
        pairs_to_add list[(int, int, int),...]:
            Pair of vertices to add to the graph with their weight
        """
        dist = {}                                                               # list of shortest paths
        adj = self.get_adjacent_vert()                                          # get adjacent vertices for all vertex

        for source in vertices_odd: 
            dist[source] = self.dijkstra(source, adj) # Use Dijkstra to compute the shortest paths


        #Greedy algorithm to track pairs with best weights
        used = set()                                                            # Set to track which vertices have been paired
        pairs_to_add = []                                                       # Initializing the output of pairs
        while len(pairs_to_add) < len(adj)/2:                                   # while there are unpaired odd vertex
            for start_vert in vertices_odd:
                if start_vert in used: 
                    continue
                min_dist = 1e+2
                best_vert = None

                for match_vert, weight in adj[start_vert]:                      # for each neighbor of the vertex
                    if match_vert in used:
                        continue
                    if dist[start_vert][match_vert] < min_dist:                 # choose the best one
                        min_dist = dist[start_vert][match_vert]
                        best_vert = match_vert

                if best_vert is not None:                                       # add best pair to the list
                        pairs_to_add.append((start_vert, best_vert, min_dist))
                        used.add(start_vert)
                        used.add(best_vert)
        return pairs_to_add

    def dijkstra(self, source, adj):
        """
        Dijkstra algorithm (pseudocode https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

        Parameters
            source: int
                origin vertex
            adj: dict{int: list(int)}
                Reprensents each vertex with all adjacent vertices listed
        Returns
        -------
        dist : dict{int: int}
            shortest distances for all pairs from source
        """
        """
        TODO: Did not implement priority queue, probably main reason we can't do paris_map.txt
        Since it seems to be stuck on the dijkstra part 
        """
        
        dist = {id: int(1e+2) for id in range(len(self.vertices))}  # Initial distances, 1e+2 is enough to be like infinite here
        Q = [id for id in range(len(self.vertices))]
        dist[source] = 0

        while Q:                                                    # main loop, goes to all vertices
            start_vect = min(Q, key=lambda vert: dist[vert])
            Q.remove(start_vect) 
            
            for neighbor, weight in adj[start_vect]:                # loop on neighbors still in Q
                if neighbor in Q:
                    alt = dist[start_vect] +  weight
                    if alt < dist[neighbor]:                        # update neighbor if new best one
                        dist[neighbor] = alt
        return dist
    
    def add_edges(graph, pairs_to_add):
        for id1, id2, weight in pairs_to_add:
            # Add the new edges to the graph (duplicate edges)
            graph.edges.append((id1, id2, weight, graph.vertices[id1], graph.vertices[id2]))
            
            
###################################################################################################
        """
        COMPUTING PATH: Solve the problem for the (pseudo) Eulerian graph
        TODO: Should format all this in different files and import to the class for readability
        """
###################################################################################################

    def eulerian_circuit(self):
        """
            compute the Eulerian path of our (pseudo) Eulerian graph
            Uses Hierholzer's algorithm (https://en.wikipedia.org/wiki/Eulerian_path#Hierholzer's_algorithm)
        Returns:
            circuit list(int): The circuit we follow
        """
        adj = self.get_adjacent_vert()
        circuit = []                                # eulerian path
        start_id, _, _, _, _ = self.edges[0]
        stack = [start_id]                          #  start at first edge of our graph/subgraph
        
        # TODO: In some cases, there might be a more efficient start
        # there is probably a way to know this

        while stack:                                # continue as long as there are vertices
            current = stack[-1]                     # current vertex

            if adj[current]:                        # check for neighbors
                next, _ = adj[current].pop()        # chose a neighbor and remove it
                adj[next].remove((current, _))      # need to also remove the edge in opposite direction in neighbor list
                stack.append(next)                  # add the next vertex to the stack to keep going
            else:
                circuit.append(stack.pop())         # remove current edge if no neighbor and go back to previous vertex
        return circuit

    def circuit_weight(self, circuit):
        """
        Compute total weight of the Eulerian path

        Parameters:
            circuit list(int): The circuit we follow

        Returns:
            total_weight int: The total weight of the circuit
        """
        total_weight = 0
        
        #  Need a way to unpack the weight for each edge of the graph according to an edge's ids
        #  Ordered the indexes with min max to prevent index error in following loop
        edge_map = {(min(id1, id2), max(id1, id2)): weight for id1, id2, weight, _, _ in self.edges}
        
        for i in range(len(circuit) - 1):
            id1, id2 = circuit[i], circuit[i + 1]
            total_weight += edge_map[(min(id1, id2), max(id1, id2))]

        return total_weight
