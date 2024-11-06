# Travail réalisé autour de l'exercice Padam R&D Test

## Notes de réflexion

Remarque : les coordonnées des sommets ne sont pas intéressantes dans ce problème.

Idées :
1. Une première idée qui semble très coûteuse en temps et en coût de chemin serait de se placer sur un sommet, faire tous les allers-retours possibles sur les arêtes non-visitées de ce sommet, puis se déplacer via une des arêtes de ce sommet vers un nouveau sommet et recommencer. Afin de limiter le coût de ce chemin, une fois tous les points visités, on pourrait supprimer les allers-retours inutiles (un aller-retour est inutile si l'arête présente dans cet aller-retour est présente en non-aller-retour dans le chemin). Lorsque l'on arrive à un point où toutes les arêtes ont déjà été visitées, il faut se déplacer à une arête non visitée et recommencer le processus.
2. On peut essayer de construire un chemin à faible coût et étudier ensuite les arêtes manquantes. On part d'un sommet ayant beaucoup d'arêtes (on selectionne un sommet dont le nombre d'arêtes est maximal), depuis ce sommet, on choisit l'arête dont le coût est le plus faible. Une fois arrivé à un sommet pour lequel toutes les arêtes ont déjà été parcourues, on rejoint une arête qui n'a pas encore été parcourue via le chemin le plus court et on recommence le processus jusqu'à avoir visité toutes les arêtes.


## Mise en place de l'idée n°2

L'objectif final est de créer une fonction `get_path` qui permet d'obtenir un chemin relativement court parcourant toutes les arêtes du graphe.

**Étape 1 :** On commence par sélectionner un sommet qui a un nombre maximal d'arêtes (ie qui a un nombre maximal de voisins). La fonction `select_vertex_max_edges` permet d'obtenir ce sommet.

**Étape 2 :** On cherche l'arête de poids minimum liée à ce sommet. Ce sera la première arête parcourue par le chemin. Nous arrivons alors à un nouveau sommet. Depuis ce sommet, on cherche l'arête non parcourue de poids minimal liée à ce nouveau sommet. La fonction `get_min_edge` permet d'obtenir l'arête de poids minimal non parcourue liée à un sommet donné. Afin de connaître les arêtes déjà parcourue, une liste nommée `visited_edges` a été préalablement définie. On réitère ce processus jusqu'à arriver à un sommet depuis lequel toutes les arêtes ont déjà été parcourues.

**Étape 3 :** S'il n'y a plus d'arêtes non visitées, on a visité toutes les arêtes et on est contents. S'il y a encore des arêtes à visiter, on en choisit une de manière aléatoire. On choisit arbitrairement un sommet de cette arête. On utilise un algorithme de chemin le plus court classique pour choisir le chemin qui va nous permettre d'y accéder. Une fois arrivé à cette arête, on recommence l'étape 2. L'algorithme de chemin le plus court le plus classique étant l'algorithme de Dijkstra, la fonction `shortest_path` permet d'obtenir le chemin le plus court d'un sommet S1 à un sommet S2 en appliquant cet algorithme.

## Observations des résultats

J'ai créé un tout petit graphe appelé *mini_graph* afin de faire des tests lors de la mise en place de mon code. Lors de l'exécution de `get_path` sur ce mini graphe, on obtient bien un chemin parcourant toutes les arêtes du graphe et son coût. Le temps d'exécution de `get_path` appliqué à ce graphe sur mon ordinateur personnel est toujours inférieur à 0.0004 seconde, ce qui est plus que convenable. En l'exécutant plusieurs fois, on remarque que les chemins obtenus ont soit un coût de 62, soit un coût de 70.

Lorsque l'on étudie le graphe *hard_to_choose*, la fonction `is_connected` indique que le graphe est bien connexe. Lorsque l'on applique `get_path` au graphe *hard_to_choose*, le temps d'exécution sur mon ordinateur personnel est toujours inférieur à 1 seconde, ce qui est tout à fait convenable. En l'exécutant plusieurs fois, on remarque que l'on a toujours un coût différent (ce qui est logique puisque lorsque l'on arrive à un sommet où toutes les arêtes ont déjà été parcourues, on choisit aléatoirement la prochaine arête non parcourue à laquelle on souhaite accéder). Les coûts que j'ai obtenus sont compris entre 1392 et 1646, la majorité des coûts obtenus sont autour de 1500.

Lorsque l'on étudie le graphe *islands*, la fonction `is_connected` indique que le graphe n'est pas connexe et il n'est donc pas possible de trouver un chemin parcourant toutes les arêtes.

Lorsque l'on étudie le graphe *paris_map*, la fonction `is_connected` indique que le graphe est bien connexe (il faut déjà 16 secondes pour que déterminer la connexité de *paris_map*). En revanche, le temps d'exécution est de `get_path` est beaucoup trop long. Après 30 minutes d'exécution du code, il est reste encore plus de 14000 arêtes non visitées.

Cette méthode permet d'obtenir de façon sûre un chemin parcourant toutes les arêtes. En revanche, le résultat obtenu n'a aucune raison d'être le court. Il s'agit d'un chemin à coût limité puisque lorsque l'on se déplace d'un sommet vers un autre via des arêtes potentiellement déjà visitées, on choisit le chemin le plus court, donc on économise un certain coût. 

**Pistes d'améliorations :**
1. Modifier le choix de l'arête à visiter lors de l'étape 3.
2. Lors de l'étape 3, une fois que la prochaine arête à visiter a été determinée, au lieu de choisir arbitrairement un des 2 sommets de l'arête, choisir le sommet le plus proche.
3. Sinon, pour améliorer l'algorithme comme dans le point 2 des pistes d'améliorations, un autre choix judicieux serait de choisir parmi les 2 sommets de cette arête celle qui a le plus (ou le moins, à déterminer) d'arêtes adjacentes non visitées afin d'arriver dans une zone relativement dense.
4. Lors de l'étape 1, j'ai choisi de sélectionner un sommet ayant un nombre maximal d'arêtes adjacentes afin d'essayer d'être dans une zone 'dense'. Ce choix peut tout à fait être revu. En particulier, si un sommet ne possède qu'une seule arête, on a envie de commencer par ce sommet afin de parcourir son unique arête adjacente une seule fois.
5. Dans le cas où des arêtes sont inaccessibles, l'algorithme tourne en rond. C'est pourquoi j'ai décidé de vérifier que le graphe était connexe avant d'exécuter la recherche de chemin.
6. Lors de l'étape 3, au lieu de choisir le chemin le plus court permettant d'accéder au nouveau sommet, il serait intéressant de construire un chemin passant par le plus d'arêtes non visitées mais avec coût limité. Il faudrait définir ce que l'on entend par 'le plus d'arêtes non visitées mais avec coût limité' et ensuite établir un algorithme permettant d'effectuer une telle recherche.
7. Malheureusement, le temps d'exécution de la fonction `get_path` est beaucoup trop élevé lorsque le graphe contient un très grand nombre d'arêtes (comme dans *paris_map*), il faudrait donc rechercher un autre algorithme permettant de traiter de tels cas.
