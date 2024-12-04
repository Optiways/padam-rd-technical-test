def expliciter_cycle(cycle, added_edge):
    # Créer un dictionnaire des arêtes cachées
    hidden_edges = {}
    for edge in added_edge:
        noeud1, noeud2, chemin = edge[0], edge[1], edge[2]
        hidden_edges[(noeud1, noeud2)] = chemin
        hidden_edges[(noeud2, noeud1)] = chemin[::-1]  # Ajouter dans l'autre sens

    # Construire le nouveau cycle
    explicit_cycle = []
    for i in range(len(cycle) - 1):
        noeud1, noeud2 = cycle[i], cycle[i + 1]
        if (noeud1, noeud2) in hidden_edges:
            chemin = hidden_edges[(noeud1, noeud2)]
            if explicit_cycle and explicit_cycle[-1] == chemin[0]:  # Éviter les doublons
                explicit_cycle.extend(chemin[1:])
            else:
                explicit_cycle.extend(chemin)
        else:
            explicit_cycle.append(noeud1)

    # Ajouter le dernier nœud du cycle
    explicit_cycle.append(cycle[-1])

    return explicit_cycle


# Exemple d'utilisation
cycle = [1, 2, 3, 4, 2, 1, 3]
added_edge = [
    [2, 3, [2, 4, 3]],
    [1, 3, [1, 5, 6, 3]]
]

nouveau_cycle = expliciter_cycle(cycle, added_edge)
print("Cycle explicité :", nouveau_cycle)