from collections import defaultdict, deque

def hierholzer(edges):
    # Étape 1 : Construire le graphe en tant que dictionnaire d'adjacence
    graph = defaultdict(list)
    for edge in edges:
        u, v, weight = edge
        graph[u].append((v, weight))
        graph[v].append((u, weight))  # Graphe non orienté
    
    # Vérification : tous les sommets doivent avoir un degré pair
    for vertex in graph:
        if len(graph[vertex]) % 2 != 0:
            raise ValueError("Le graphe n'a pas un degré pair pour tous les sommets : Pas de cycle eulérien.")
    
    # Étape 2 : Trouver le cycle eulérien
    def find_eulerian_cycle(start):
        stack = [start]
        cycle = deque()
        while stack:
            node = stack[-1]
            if graph[node]:  # Si le sommet a des voisins
                next_node, _ = graph[node].pop()
                # Supprimer l'arête dans les deux directions
                graph[next_node].remove((node, _))
                stack.append(next_node)
            else:  # Plus de voisins, ajouter au cycle
                cycle.appendleft(stack.pop())
        return list(cycle)
    
    # Trouver un sommet de départ avec des voisins
    start_vertex = next(iter(graph))
    return find_eulerian_cycle(start_vertex)