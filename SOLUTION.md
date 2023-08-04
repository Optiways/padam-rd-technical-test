# Solution (Jean Leprovost)

The idea is to use an approach of the kind genetic algorithm. We generate N paths randomly and operate a resampling (selection) by drawing N new paths with replacement from the N paths generated, according to weights. The better the path, the higher its weight so that good paths have more chance to reproduce. Then, we only keep the first h steps of the paths. We repeat the process by generating the paths now starting at step h. Then resample the paths again, only keep the 2*h first steps, and so on.
At the end, we keep the shortest path which is the best solution found.

The function 'GenSol' apply this algorithm, but take as an argument an imposed sarting node for the path. To find a global solution (a path that can start at any node), we can apply GenSol with all the nodes as starting node and keep the best. 
Another solution is to just remove this argument from the function and choose a random starting vertex for each particule.

## Note

The solution implemented is incomplete and therefore cannot be run.
I spent between 3 and 5 hours on the exercise I would say (plus a bit more to understand the given code, and to write this document and a few comments).


