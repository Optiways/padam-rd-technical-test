from functions import weight_connect_degree_mat
import random as rd

def GenSol(graph,N,u_start,h=5):    # TODO adjust h
    vertices = graph.vertices
    edges = graph.edges
    V = len(vertices)
    W, C, D = weight_connect_degree_mat(graph)
    neighbors = neighbors(graph)

    rem, dist = [V-1 for _ in range(N)], [0 for _ in range(V)]
    L = 2*V     # A path can end up being longer than the number of edges since, (but shouldn't be too much since the given instances are quiet dense)
                # TODO 2 is arbitrary and should be adjusted
    paths = [[-1 for _ in range(L)] for _ in range(N)] # each line is a path
    Cs = [C for _ in range(N)] 

    # Initialize paths starting nodes.
    for i in range(N):
        paths[i][0] = u_start
    
    for starting_step in range(1,L,h): 
        for i in range(N):
            if rem[i] > 0: # if their are still some nodes to visit
                path = paths[i]
                C = Cs[i]
                # Generate a random path from the starting_step, of size L maximum
                for step in range(starting_step, L):
                    u = path[step]
                    adj_u = C[u]
                    # Choose next node.
                    v = rd.choices([i for i in range(V)], weights=C[u]) # TODO Here the weights are uniform, they could be adjusted as function of the weights of the edges and degrees of the nodes for example
                    path[step+1] = v # add node to path
                    dist[i] += W[u][v] # keep track of the length of the path
                    rem[i] -= 1
                    
                    # 'Delete' node u. 
                    # TODO this should be adjusted since it should be possible to visit some nodes multiple times
                    for j in range(V):
                        C[u][j] = 0
                        C[j][u] = 0
                    
                Cs[i] = C
        # Resample the paths.
            # TODO : compute the reproducing weight omega of each path.
            #       omega should at first increase with the number of nodes visited by the path, 
            #       and secondly decrease with the lenght of the path (sum of weights).
            # TODO : choose N paths from the N paths (with replacement) according to the reproducing weights.
            #        (the best tracks generated have a higher chance to reproduce)
        
        # Cut the paths.
            paths[starting_step+h:-1] = [[-1 for _ in range(N)] for _ in range(L-(starting_step+h))] # only keep the first starting_step+5 steps of the paths
            # TODO : update Cs, dist and rem to match with the cutted paths.

    # Choose the final best path
        #TODO

