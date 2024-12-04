# Solution présentée pour le test technique par Jules Garcia

Le but est de trouver le chemin le plus court en passant par toutes les arêtes d'un graphe au moins une fois. J'ai choisi l'approche suivante :

Si un graphe est eulérien, alors il existe un chemin qui passe exactement une fois par toutes les arêtes. Cependant, plusieurs conditions doivent être respectées :
- Le graphe doit être connexe.
- Il doit y avoir 0 ou 2 sommets avec un degré impair.

Or, dans les graphes proposés, ni la parité des sommets ni la connexité ne sont garanties.

Mon approche a donc été de rendre le graphe fourni "pair".

## Démarche suivie

Pour ce faire :
1. **Identification des sommets impairs** : On identifie tous les sommets ayant un degré impair dans le graphe.
2. **Suppression d'arêtes** : On supprime la plus petite arête (celle de poids le plus faible) reliant deux sommets impairs.
3. **Recherche de voisins** : Si un sommet impair n'a pas de voisin impair direct, on recherche le chemin le plus court vers un autre sommet impair et on crée une nouvelle arête entre ces deux.
4. **Application de l'algorithme de Hierholzer** : Une fois qu'il ne reste plus d'arêtes impaires, on applique l'algorithme de Hierholzer pour trouver un cycle eulérien.
5. **Correction du cycle** : On "corrige" le cycle obtenu de la manière suivante :
   - En explicitant les arêtes qui n'étaient pas présentes dans le graphe initial, en les remplaçant par le chemin le plus court calculé précédemment.
   - En ajoutant un aller-retour entre deux sommets dont l'arête a été supprimée. C'est pour cela que l'on a choisi l'arête de poids le plus faible, afin de limiter l'impact de l'aller-retour.

## Remarques

Cet algorithme n'est pas optimal pour déterminer le chemin le plus court, mais j'ai privilégié la rapidité d'exécution pour obtenir une solution rapidement.

## TODO et pistes d'améliorations

N'ayant pas eu le temps de mettre en place toutes les fonctionnalités que j'avais envisagées et de tester la validité de mon code, voici les améliorations possibles :

- **Calcul du chemin le plus court entre deux sommets impairs** : Une fonction permettant de calculer le chemin le plus court entre deux sommets impairs (par exemple, avec Dijkstra ou A*, si un système d'heuristique est possible).
- **Choix des sommets impairs** : Actuellement, le deuxième sommet est choisi de manière aléatoire. Si le temps n'était pas un problème, on pourrait calculer les chemins reliant chaque paire de sommets impairs et sélectionner le plus court.
- **Approximation du TSP** : Si l'on souhaite aller plus loin, on pourrait appliquer une approximation du problème du voyageur de commerce (TSP) pour optimiser les trajets entre les sommets impairs.
- **Correction du cycle final** : Améliorer la fonction qui corrige le cycle final obtenu.
