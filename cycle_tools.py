def correction(cycle, added_edges, removed_edges):
    """
    Fonction qui "corrige" la sortie du cycle fourni sur le graphe modifié.
    Elle va expliciter les aretes qui ont été ajouté et celles supprimé lors de l'étape où le graphe a été transformé en graph eulerien
    """


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



def add_back_and_forth(cycle, removed_edges):
    """
    Implementer une fonction qui permet d'ajouter un aller retour lorsque on arrive sur un noeud faisant parti d'une arete "supprimé"

    ex : cycle [1,2,3,4,5,4,3,2,1] arete_supprimées = [(2,6),(5,7)]
     sortie : [1,2,6,2,3,4,5,7,5,4,3,2,1]

    