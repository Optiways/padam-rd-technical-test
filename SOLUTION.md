## Notes de réflexion

Remarque : les coordonnées des sommets ne sont pas intéressants dans ce problème.

Idées :
1. On peut essayer de construire un chemin à faible coût et voir ensuite les arêtes manquantes : on part d'une arête à coût très faible (on choisit aléatoirement une arête parmi les arêtes au coût le plus faible), on choisit aléatoirement une des extrémités de l'arête, depuis cette extrémité, on choisit l'arête dont le coût est le plus faible. Problème : une fois arrivé à un sommet pour lequel toutes les arêtes ont déjà été parcourues, il faut rejoindre une arête qui n'a pas encore été parcourue via le chemin le plus court.
2. On aimerait savoir construire un chemin quelconque permettant de parcourir toutes les arêtes. Une fois qu'on a un tel chemin, essayer de modifier l'algorithme pour avoir un chemin avec un coût plus faible.

### Tentative d'algorithme permettant de parcourir toutes les arêtes du graphe:
Pour chaque sommet, on définit la liste de ces voisins adjacents.