1. **Objectif du programme**
   Ce code vise à produire un **parcours eulérien** (ou quasi-eulérien) dans un graphe non orienté pondéré, en doublant certaines arêtes si nécessaire pour rendre tous les degrés pairs.

   * S’il est déjà eulérien, on applique l’algorithme de Hierholzer directement.
   * Sinon, on identifie les sommets de degré impair et on utilise :

     1. Dijkstra pour calculer les plus courts chemins entre ces sommets.
     2. L’algorithme de Blossom pour trouver un couplage de poids minimal entre ces sommets (fermé ou « ouvert »).
     3. On duplique les arêtes du graphe selon ce couplage pour obtenir un multigraphe eulérien, puis on génère le parcours.

2. **Importations et réglages**

   ```python
   import heapq
   from collections import deque
   import sys

   sys.setrecursionlimit(1000000)
   ```

   * `heapq` : file de priorité min pour Dijkstra.
   * `deque`  : file FIFO pour la recherche de chemin augmentant dans Blossom.
   * `sys.setrecursionlimit` : permet d’éviter les limites de récursion lors du DFS.

3. **Fonction `blossom_min_weight_matching(edges)`**

   * **But** : trouver un **couplage parfait** de poids total minimal dans un graphe complet implicite défini par une liste d’arêtes pondérées.
   * **Paramètre** :

     * `edges` : liste de triplets `(u, v, w)` décrivant une arête entre nœud `u` et `v` de poids `w`.
   * **Retour** : liste de triplets `(u, v, w)` correspondant au couplage trouvé.

   **Étapes** :

   1. Construction de l’ensemble des nœuds et correspondance index ↔ nœud.
   2. Création d’une matrice de poids initialisée à −∞, puis remplissage avec `-w` pour convertir la recherche de poids minimal en maximum.
   3. Structures de données :
      * `match[i]`  : index du nœud apparié avec `i` (−1 si libre).
      * `label[i]`  : étiquette (0 pour blancs, 1 pour gris, −1 non étiqueté).
      * `parent[i]` : parent dans l’arbre de recherche de chemins augmentants.
      * `in_blossom` : gestion des contractions de fleurs.
   4. Recherche en largeur (BFS modifiée) pour trouver un **chemin augmentant** ou détecter une **fleur** (cycle impair).
      * `find_base` identifie la base d’une fleur commune.
      * Contraction de la fleur : réétiquetage et ajustement des parents.
   5. Dès qu’un chemin augmentant est trouvé, on **augmente** le couplage.
   6. Après convergence, construction de la liste de couplage avec poids d’origine `−weights[i][j]`.


4. **Fonction `sol(graph)`**

   * **But** : renvoyer la liste d’arêtes (avec répétitions) formant un parcours eulérien dans `graph`.
   * **Paramètre** :
     * `graph.vertices` : liste des sommets (numérotés `0…n−1`).
     * `graph.edges`    : liste de quintuplets `(u, v, w, ..., ...)` où seul `u, v, w` sont utilisés ici.
   * **Retour**  : liste d’arêtes (mêmes format que `graph.edges`) dans l’ordre du parcours.

   **Étapes** :

   1. Calcul des degrés de chaque sommet, identification de la liste `T` de sommets de degré impair.
   2. **Cas 1 :** si `T` est vide → graphe déjà eulérien → Hierholzer direct avec DFS récursif.
   3. **Cas 2 :** `k = len(T) > 0` → deux options de couplage des sommets impairs :
      * **Fermé** (tous couplés entre eux) → calcul de `closed_matching` via Blossom.
      * **Ouvert** (deux sommets libres) → on ajoute deux nœuds fictifs, on recalcule un couplage `open_matching`.
      * On compare les coûts `M0` et `M_open` pour choisir la meilleure solution.
   4. On déduit la **multiplicité** de chaque arête du graphe initial selon le couplage retenu (chaque chemin de couplage fait « doubler » certaines arêtes).
   5. Construction d’un **multigraphe** où chaque arête peut apparaître plusieurs fois.
   6. Application de l’algorithme de Hierholzer amélioré (DFS récursif) pour produire la séquence d’arêtes `path_edge_indices`.
   7. Conversion des indices en arêtes originales et renvoi.

5. **Complexités et remarques**

   * La partie Blossom a un coût élevé (complexité théorique $O(n^3)$), mais se limite au nombre de sommets impairs.
   * Dijkstra est exécuté $k$ fois ($k$ = nombre de sommets impairs) $\to$ $O(k (m + n)\log n)$.
   * L’algorithme convient pour des graphes de taille modérée (quelques centaines de sommets).
   * L’usage de poids négatifs dans la matrice de Blossom sert à transformer un problème de minimisation en maximisation.

6. **Application aux exemples**

   1. **small\_test.txt** (4 nœuds, 6 arêtes)

      * J'ai implémenté cet exemple pour vérifier rapidement si la solution est à la fois faisable et minimale.
      * Le programme trouve un circuit eulérien minimal qui parcourt chaque arête exactement une fois.
      * Vérification : toutes les arêtes sont couvertes sans répétition, confirmant le bon traitement du cas déjà eulérien.

   2. **island.txt** et **hard\_to\_choose.txt**

      * Le code applique Dijkstra puis Blossom pour dupliquer certaines arêtes et rendre le graphe eulérien.
      * On observe que le nombre total d’arêtes parcourues dépasse le nombre initial (certaines arêtes ont une multiplicité > 1).
      * Temps d’exécution : < 1 seconde sur machine standard, ce qui montre que l’algorithme reste efficace pour de petits à moyens graphes.

   3. **paris_map.txt** 

      * Quand la taille du graphe devient trop important, la phase de couplage Blossom et les multiples exécutions de Dijkstra peuvent devenir prohibitifs en temps et en mémoire.
      * Sur de telles instances, l’algorithme peut ne pas converger ou simplement planter (manque de mémoire, temps trop long).
      * Pour traiter ce type de cas, il faut alors :
        * soit préfiltrer ou réduire heuristiquement la liste des sommets impairs avant de lancer Blossom,
        * soit recourir à une version approchée du couplage (greedy matching, algorithme LEMON, etc.),

---

**Perspectives d’amélioration**

* **Heuristiques de préfiltrage** des sommets impairs pour diminuer la taille du problème avant Blossom.
* **Matching approché** pour les instances trop grandes (algorithmes gloutons, relaxation linéaire suivie de rounding).
* **Optimisation mémoire** (libération dynamique des matrices, structures de données compactes).
* **Parallélisation** des calculs de plus court chemin et du traitement des fleurs.
* **Extension de la suite de tests** avec des graphes réels (réseaux routiers, topologies urbaines) pour valider robustesse et performances.
