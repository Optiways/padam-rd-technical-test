def Prim(vertices: list[tuple], edges: list[tuple])->list[tuple]:
    """
    Find the graph connecting all the nodes at minimum cost
    
    ----------
    Parameters
    ----------
    vertices : list[tuple]
        list of vertices coordinates of the original graph.
    edges : list[tuple]
        list of edges of the original graph as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
    
    Returns
    -------
    list[tuple]
        list of edges as tuple (id 1, id 2, weight, coordinates 1, coordinates 2) 
        of the graph connecting all the nodes, that can be connected, at minimum cost
    
    """
    
    "S is the set of nodes connected"
    "T is the final set of edges"
    S,T=[],[]
    
    "List of all the nodes"
    id1=set(edge[0] for edge in edges)
    id2=set(edge[1] for edge in edges)
    List_node=list(id1 | id2)
    
    #print("the list of the nodes is ",List_node)
    #print("n is",n)
    "Put one node in S and delete it from the list of the nodes"
    u=List_node[0]
    List_node.remove(u)
    S.append(u)
    
    "initialize edgemin"
    edgemin=()
    
    """index_new_node is a flag to indicate if: 
        -index_new_node=0 : the new node to add to S is in first position of edgemin
        -index_new_node=1 : the new node to add to S is in second position of the edgemin
        -index_new_node=2 : no more nodes can be connected to the set S, so start a new group
    """
    index_new_node=2
    
    
    edges=Sort(edges)
    #print("sorted edges is", edges)
    
    while len(List_node)>0:
        "while all the points are not connected"
        #print("S is ",S)
        print("len de S is",len(S))
        #print("List_node is ",List_node)
        print("len of List_node is",len(List_node))
        #print("len of T is",len(T))
        #print("T is ",T)
        
        
        "Find the next point to connect at minimum cost"
        edgemin, edges, index_new_node =Edge_Min_Cost(S,edges)
        #print("edgemin is", edgemin)
        #print("the new index is", index_new_node)
        
        if index_new_node<2:
            "there exist at least one point to connect to S"
            T.append(edgemin)
            S.append(edgemin[index_new_node])
            List_node.remove(edgemin[index_new_node])
            "mettre l'indice dans l'autre fonction"
        else :
            "There is no more point to connect, so take another group of points that cannot be connected"
            u=List_node[0]
            List_node.remove(u)
            #S.append(u)
            "we know that no more node can be connected, so to avoid to go over the whole S, we restart it as a new set of nodes"
            S=[u]
    return T

def Sort(edges: list[tuple])-> list[tuple]:
    """
    Insertion sort

    Parameters
    ----------
    edges : list[tuple]
        edges not sorted.

    Returns
    -------
    list[tuple]
        edges sorted according to the weight.

    """
    n=len(edges)
    for i in range(n):
        min_element_index=i
        for j in range(i + 1, n):
            ## checking and replacing the minimum element index
            if edges[j][2] < edges[min_element_index][2]:
                min_element_index = j

		## swaping the current element with minimum element
        edges[i], edges[min_element_index] = edges[min_element_index], edges[i]
    
    return(edges)
    

def Edge_Min_Cost(S: list, edges: list[tuple])->tuple[tuple, list[tuple], int]:
    """
    Find the node connected at minimum cost to the input set of nodes
    
    Parameters
    ----------
    S : list
        list of vertices (id) we want to find the new node connected at minimum cost
    edges : list[tuple]
        list of edges sorted of the original graph as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
    
    Returns
    -------
    tuple
        edge at minimum cost as tuple (id 1, id 2, weight, coordinates 1, coordinates 2).
        list of final edges without edges between two nodes of S
        index in edgemin of the new node to add to S
    """
    
    index_new_node=2
    edgemin=()
    i=0
    n=len(edges)
    while len(edgemin)==0 and i<n:
        e=edges[i]
        if e[0] in S:
            if e[1] in S:
                "the edge connect two nodes of S"
                edges.remove(e)
            else:
                "this edge is at minimum cost and is induced by S"
                index_new_node=1
                edgemin=e
                edges.remove(e)
        else:
            if e[1] in S:
                "this edge is at minimum cost and is induced by S"
                index_new_node=0
                edgemin=e
                edges.remove(e)
        "the edge is not connected to S"
        n=len(edges)
        i=i+1
    return edgemin, edges, index_new_node

