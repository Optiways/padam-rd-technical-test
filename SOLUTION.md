# Solution : Parcours Continu de toutes les arêtes d'un graph

## Première approche

Pour un parcours continu des arêtes, nous pouvons :

1 - Choisir une arête de départ arbitraire (la première).  
2 - Trouver parmi les arêtes restantes celle qui commence là où s'est terminée l'arête précédente.  
3 - Répéter jusqu'à avoir traversé toutes les arêtes.  

Testons cette première idée.