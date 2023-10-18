from graph import *
import numpy as np
import random
from copy import deepcopy
        
def lowerBound(graph):
    return sum([e[3] for e in graph.edges])


def create_new_edges(graph): 
    """
    Creating new edges to make the graph semi-eulerian.

    Parameters
    ----------
    Graph : Graph
        
    Returns
    -------
    """
    odd_degrees = [v for v in range(len(graph.vertices)) if graph.degrees[v]%2 == 1]
    print(odd_degrees)
    nb_edges_to_add = len(odd_degrees)/2-1
    while nb_edges_to_add != 0:
        print(nb_edges_to_add)
        best_dist = np.inf
        best_edge = None
        for v in odd_degrees:
            for u in odd_degrees:
                if u >= v:
                    continue
                if graph.distances[v][u] < best_dist:
                    best_dist = graph.distances[v][u]
                    best_edge = [v, u]
        graph.edges.append([len(graph.edges), best_edge[0], best_edge[1], best_dist, graph.vertices[best_edge[0]],graph.vertices[best_edge[1]]])
        graph.degrees[best_edge[0]] +=1
        graph.degrees[best_edge[1]] +=1
        odd_degrees.remove(best_edge[0])
        odd_degrees.remove(best_edge[1])
        nb_edges_to_add -= 1
    graph.max_degree = max(graph.degrees)
    

def create_edge_path_from_shortestpath(graph, shortestespath):
    epath = []
    dist_tot = 0
    dist = graph.distances[shortestespath[0]][shortestespath[-1]]
    for i in range(len(shortestespath)-1):
        min_distance = 100000
        edge = None
        current_vertex = shortestespath[i]
        next_vertex = shortestespath[i+1]
        for e in graph.get_adjacent_edges(current_vertex):
            if (e[1] == current_vertex and e[2] == next_vertex) or (e[2] == current_vertex and e[1] == next_vertex):
                if e[3] < min_distance :
                    min_distance = e[3]
                    edge = e
        dist_tot += min_distance
        epath.append(edge)
    assert(dist == dist_tot)
    return epath

def find_next_edge_in_cycle(graph, strart_vertex, current_vertex, marked_edges):
    adjEdges = graph.get_adjacent_edges(current_vertex) #check all edges 
    nextEdge = None
    for edge in adjEdges:
        if marked_edges[edge[0]] : #if already marked 
            continue
        else :
            if nextEdge == None: 
                nextEdge = edge
            if current_vertex != strart_vertex and (edge[1] == strart_vertex or edge[2] == strart_vertex): 
                # we want to come back to v as soon as possible
                nextEdge = edge
    if nextEdge == None: ## we are suppose to find cycles 
        print("Error")
        return
    return nextEdge
    
def computeEulerianCycle(graph):
    path = [] ## edges path
    vpath = [0] ## vertices path : starting at 0
    remainingDegrees = graph.degrees
    markedEdges = [False for _ in range(len(graph.edges))]
    oldRemainingDegrees = -1
    currentVertex = 0
    while sum(remainingDegrees) != 0 :
        if (sum(remainingDegrees) == oldRemainingDegrees):
            return
        oldRemainingDegrees = sum(remainingDegrees)
        for v in vpath:
            if remainingDegrees[v] != 0: #check if v still has edges to marked
                # if we change of vertex, we take the shortest path to this new
                # vertex
                if currentVertex != v:
                    shortest_vpath = graph.shortestPaths[currentVertex][v]
                    shortest_epath = create_edge_path_from_shortestpath(graph, shortest_vpath)
                    shortest_vpath = shortest_vpath[1:]
                    vpath += shortest_vpath
                    path += shortest_epath
                        
                currentVertex = v
                newCycle = [] #creating a cycle starting at v
                newvCycle = []
                stoppingCondition = False
                while stoppingCondition != True:
                    nextEdge = find_next_edge_in_cycle(graph, v, currentVertex, markedEdges)
                    
                    newCycle.append(nextEdge)
                    markedEdges[nextEdge[0]] = True
                    remainingDegrees[nextEdge[1]] -= 1
                    remainingDegrees[nextEdge[2]] -= 1
                    if (currentVertex == nextEdge[1]):
                        currentVertex = nextEdge[2]
                    else :
                        currentVertex = nextEdge[1]
                    newvCycle.append(currentVertex)
                    if currentVertex == v: ## if we are back to v
                        stoppingCondition = True
                path= path + newCycle
                vpath= vpath + newvCycle
                break
    return path, vpath
    
def computeEulerianPath(graph):
    path = []
    remainingDegrees = graph.degrees ## degrees of nodes after we went throught one 
                                     ## of its edge
    markedEdges = [False for _ in range(len(graph.edges))]
    nbOdd = 0
    debut, fin = -1, -1
    for i in range(graph.vertices):
        if (remainingDegrees[i] % 2 == 1):
            if nbOdd == 0:
                debut = i
            if nbOdd == 1:
                fin = i
            nbOdd += 1
    if nbOdd != 2:
        print("Error")
        return
    
    vpath = graph.shortestPaths[debut][fin]
    for i in range(1, len(vpath) - 1):
        remainingDegrees[vpath[i]] -= 2
    remainingDegrees[vpath[0]] -= 1
    remainingDegrees[vpath[-1]] -= 1
    
    for i in range(len(vpath) - 1):
        # Mark edge of the path
        for e in range(len(graph.edges)):
            if graph.edges[e][1] == vpath[i] and graph.edges[e][2] == vpath[i + 1]:
                markedEdges[e] == True 
                path.append(graph.edges[e])
                break
            if graph.edges[e][2] == vpath[i] and graph.edges[e][1] == vpath[i + 1]:
                markedEdges[e] == True 
                path.append(graph.edges[e])
                break
    
    while sum(remainingDegrees) != 0 :
        for v in vpath:
            if remainingDegrees[v] != 0:
                currentVertex = v
                newCycle = []
                newvCycle = [currentVertex]
                stoppingCondition = False
                while stoppingCondition != True:
                    adjEdges = graph.get_adjacent_edges(v)
                    nextEdge = None
                    for edge in adjEdges:
                        if markedEdges[edge[0]] :
                            continue
                        if nextEdge == None:
                            nextEdge = edge
                        if currentVertex != v and (edge[1] == v or edge[2] == v):
                            nextEdge = edge
                    
                    newCycle.append(edge)
                    markedEdges[edge[0]] = True
                    if (currentVertex == edge[1]):
                        currentVertex = edge[2]
                    else :
                        currentVertex = edge[1]
                    newvCycle.append(currentVertex)
                    if currentVertex == v:
                        stoppingCondition = True
                path.append(newCycle)
                vpath.append(newvCycle)
                break
    return path, vpath

def min_semi_eurelian_path(graph):
    graphCopy = deepcopy(graph)
    odd_degrees = [v for v in range(len(graph.vertices)) if graph.degrees[v]%2 == 1]
    if (len(odd_degrees)) == 0:
        path, vpath = computeEulerianCycle(graphCopy)
    else :
        create_new_edges(graphCopy)
        path, vpath = computeEulerianPath(graphCopy)
        
    return path, vpath, sum([e[3] for e in path])
    
    #Postprocess : solution contains inexistent edges that must be transformed with graph.shortestPaths
    

def check_solution(graph, path, vpath, vertex_ini):
    check_path = True
    ## Check if vertices in edges of the path
    if len(vpath)-1 != len(path):
        print(f'Error solution :\n length of vertices path not the same as the edges path')
        check_path = False
    ## Check if vertices in edges of the path
    for i in range(len(path)):
        if vpath[i] == path[i][1] or vpath[i] == path[i][2]:
            continue
        else:
            print(f'Error solution :\n vertex {vpath[i]} not in edge {path[i]}') 
            check_path = False
    
    # Check jumps in the path
    current_vertex = vertex_ini
    for i in range(len(path)-1):
        if path[i] not in graph.get_adjacent_edges(vpath[i]):
            print(f'Error solution :\n vertex {vpath[i]} not linked to vertex {vpath[i+1]}')
            check_path = False
    
    # Check if path is semi-Eulerian
    for edge in graph.edges:
        if edge not in path:
            print(f"Error solution \n edge {edge} not in solution") 
    
    if check_path:
        print("Solution is admissible")
        return 
    else: 
        print("Solution is not admissible")
        return
        