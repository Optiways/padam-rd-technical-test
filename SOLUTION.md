## Notes de réflexion

Remarque : les coordonnées des sommets ne sont pas intéressants dans ce problème.

Idées :
1. Une première idée qui semble très coûteuse en temps et en coût de chemin serait de se placer sur un sommet, faire tous les allers-retours possibles sur les arêtes non-visitées de ce sommet, puis se déplacer via une des arêtes de sommet à nouveau sommet et recommencer. Afin de limiter le coût de ce chemin, une fois tous les points visités, on pourrait supprimer les allers-retours inutiles (un aller-retour est inutile si l'arête présente dans cet aller-retour est présente en non-aller-retour dans le chemin). Lorsque l'on arrive à un point toutes les arêtes ont déjà été visitées, il faut se déplacer à une arête non visitée et recommencer le processus.
2. On peut essayer de construire un chemin à faible coût et étudier ensuite les arêtes manquantes. On part d'un sommet ayant beaucoup d'arêtes (on selectionne le premier sommet dont le nombre d'arêtes est maximal), depuis ce sommet, on choisit l'arête dont le coût est le plus faible. Une fois arrivé à un sommet pour lequel toutes les arêtes ont déjà été parcourues, il faut rejoindre une arête qui n'a pas encore été parcourue via le chemin le plus court et recommencer le processus jusqu'à avoir visité toutes les arêtes.


### Mise en place de l'idée n°2
**Étape 1 :** On commence par sélectionner un sommet qui a un nombre maximal d'arêtes (ie qui a un nombre maximal de voisins). La fonction `select_vertex_max_edges` permet d'obtenir ce sommet.
**Étape 2 :** On cherche l'arête de poids minimum liée à ce sommet. Ce sera la première arête parcourue par le chemin. Nous arrivons alors à un nouveau sommet. Depuis ce sommet, on cherche l'arête non parcourue de poids minimal liée à ce nouveau sommet. La fonction `get_min_edge` permet d'obtenir l'arête de poids minimal non parcourue liée à un sommet donné. Afin de connaître les arêtes déjà parcourue, une liste nommée `visited_edges` a été préalablement définie. On réitère ce processus jusqu'à arriver à un sommet depuis lequel toutes les arêtes ont déjà été parcourues.
**Étape 3 :** S'il n'y a plus d'arêtes non visitées, on a visité toutes les arêtes et on est contents. S'il y a encore des arêtes à visiter, on en choisit une de manière aléatoire. On choisit arbitrairement un sommet de cette arête. On utilise un algorithme de chemin le plus court classique pour choisir le chemin qui va nous permettre d'y accéder. Une fois arrivé à cette arête, on recommence l'étape 2. L'algorithme de chemin le plus court le plus classique étant l'algorithme de Dijkstra, la fonction `shortest_path` permet d'obtenir le chemin le plus court d'un sommet S1 à un sommet S2 en appliquant cet algorithme.
**Pistes d'améliorations :**
1. Modifier le choix de l'arête à visiter lors de l'étape 3.
2. Lors de l'étape 3, une fois que la prochaine arête à visiter, au lieu de choisir arbitrairement un des 2 sommets de l'arête, choisir l'arête la plus proche.
3. Sinon, pour améliorer l'algorithme comme dans le point 2 des pistes d'améliorations, un autre choix judicieux, serait de choisir parmi les 2 sommets de cette arête celle qui a le plus (ou le moins, à déterminer) d'arêtes adjacentes non visitées.
4. Cet algorithme est bien trop long !

