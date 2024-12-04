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
        self.node_parity = node_parity()
        self.removed_edges, self.added_edges = make_all_nodes_even()


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

    def node_parity(self):
        edges = self.edges
        # Création d'un dictionnaire pour compter les arêtes par nœud
        node_degrees = {}
        
        # Traitement des arêtes
        for edge in edges:
            node1, node2, _ ,_ ,_ = edge  # On ignore le poids
            
            # Incrémenter le nombre d'arêtes pour chaque nœud
            if node1 not in node_degrees:
                node_degrees[node1] = 0
            if node2 not in node_degrees:
                node_degrees[node2] = 0
            
            node_degrees[node1] += 1
            node_degrees[node2] += 1
        
        # Calcul de la parité (pair ou impair) pour chaque nœud
        node_parity = {}
        for node, degree in node_degrees.items():
            node_parity[node] = (degree,"pair" if degree % 2 == 0 else "impair")
        
        return node_parity

    def make_all_nodes_even(self):
        # Étape 1 : Récupérer la parité des nœuds
        node_parity = self.node_parity()
        
        # Récupérer les nœuds impairs
        odd_nodes = [node for node, (degree, parity) in node_parity.items() if parity == "impair"]
        removed_edges = []  # Liste des arêtes supprimées
        added_edges = []    # Liste des arêtes ajoutées
        
        # Étape 2 : Supprimer les arêtes entre nœuds impairs
        while odd_nodes:
            node1 = odd_nodes.pop(0)  # Prendre un nœud impair
            
            # Trouver les arêtes connectées à ce nœud
            connected_edges = [(edge,edge[2]) for edge in self.edges if node1 in edge[:2]] # (node1, node2, cost)

            # connected_edges = [(edge, cost) for edge in self.edges if node1 in edge[:2]]
            
            # Filtrer les arêtes reliant deux nœuds impairs
            edges_between_odd_nodes = [
                (edge, cost) for edge, cost in connected_edges if edge[0] in odd_nodes or edge[1] in odd_nodes
            ]
            
            if edges_between_odd_nodes:
                # Trouver l'arête avec le coût minimum
                edge_to_remove, min_cost = min(edges_between_odd_nodes, key=lambda x: x[1])
                
                # Supprimer l'arête
                self.edges.remove(edge_to_remove)
                removed_edges.append(edge_to_remove)
                
                # Mettre à jour les degrés des nœuds connectés
                node_parity[edge_to_remove[0]] = (
                    node_parity[edge_to_remove[0]][0] - 1,
                    "pair" 
                )
                node_parity[edge_to_remove[1]] = (
                    node_parity[edge_to_remove[1]][0] - 1,
                    "pair" 
                )
                
                # Retirer les nœuds pairs de la liste des impairs
                odd_nodes = [node for node in odd_nodes if node_parity[node][1] == "impair"]
            else:
                # Si aucun nœud impair connecté, ajouter une arête
                if not odd_nodes:
                    break  # Aucun nœud impair restant
                
                node2 = odd_nodes.pop(0)  # Prendre un autre nœud impair
                
                # Trouver la distance minimale entre node1 et node2
                path, min_cost = self.find_shortest_distance(node1, node2)  # À implémenter 
                new_edge = (node1, node2, min_cost)
                
                # Ajouter l'arête
                self.edges.append(new_edge)
                added_edges.append(new_edge, path)
                
                # Mettre à jour les degrés des nœuds
                node_parity[node1] = (
                    node_parity[node1][0] + 1,
                    "pair"
                )
                node_parity[node2] = (
                    node_parity[node2][0] + 1,
                    "pair" 
                )
                
                # Retirer les nœuds pairs de la liste des impairs
                odd_nodes = [node for node in odd_nodes if node_parity[node][1] == "impair"]
        
        return removed_edges, added_edges