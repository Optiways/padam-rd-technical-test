from input import parse_cmd_line, parse_file
from graph import Graph
from itertools import permutations
import time
#This first part concerns treating eulerien (or semi eulerian graphs) to find an eulerian path
def E(edges):
    # return only edges without cost nor coordinates of vertices
    edges1=[]
    for e in edges:
        edges1.append(e[0:2])
    return edges1
def E1(edges):
    # return only edges without coordinates of vertices
    edges1=[]
    for e in edges:
        edges1.append(e[0:3])
    return edges1
def neighbor(vertices, edges):
    #returns a dict with a list of neighbors for each vertex
    adjacency_dict={}
    for e in edges:
        adjacency_dict[e[0]]=[]
        adjacency_dict[e[1]]=[]
    for e in edges:
        adjacency_dict[e[0]].append(e[1])
        adjacency_dict[e[1]].append(e[0])

    return adjacency_dict

def neighbor_w(vertices, edges):
    #returns a dict with a list of neighbors for each vertex with the weights associated to edges
    adjacency_dict={}
    for e in edges:
        adjacency_dict[e[0]]=[]
        adjacency_dict[e[1]]=[]
    for e in edges:
        adjacency_dict[e[0]].append((e[1],e[2]))
        adjacency_dict[e[1]].append((e[0],e[2]))

    return adjacency_dict
def addEdge(u,v,neighbors,edges):
    # adds an edge to the graph
    edges.append((u,v))
    neighbors[u].append(v)
    neighbors[v].append(u)

def rmvEdge(u, v,neighbors,edges):
    # deletes an edge from the graph
    if (u,v) in edges:
        edges.remove((u,v))
    elif (v,u) in edges:
        edges.remove((v,u))
    neighbors[u].remove(v)
    neighbors[v].remove(u)

#testing if the graph is eulerian, semi eulerian or not eulerian

def test_eulerian(vertices,edges):
    '''returns 1 if the graph is eulerian, i.e if every vertex if of even degree, 0 if it's not eulerian, 
    and 2 if it has exactly 2 vertices with odd degrees'''
    
    adjacency_dict=neighbor(vertices,edges)
    counter=0
    v=0
    for vertex in adjacency_dict:
        if len(adjacency_dict[vertex])==0:
            print('Non connexe graph')
        if len(adjacency_dict[vertex])%2==1:
            counter+=1
            v=vertex
    if counter==0:
        return 1,0
    elif counter==2:
        return 2,v
    else: return 0,0

def DFScount(v, vertices, edges):
    # Counts the number of reachable vertices from v
    stack = [v]
    count = 0
    visited={v: False for v in range(len(vertices))}
    neighbors= neighbor(vertices,edges)
    while stack:
        current = stack.pop()
        if not visited[current]:
            visited[current] = True
            count += 1
            for n in neighbors[current]:
                if not visited[n]:
                    stack.append(n)
    return count    

def test_connexe(vertices,edges):
    '''tests if the graph is connected, which reduces to knowing from from vertex 0 we can reach every 
    other vertex'''
    
    x=DFScount(0,vertices,edges)
    return x==len(vertices)

#Now, if we have an eulerian or semi-eulerian graph, let's create an eulerian path

def is_valid_nextEdge(u,v,vertices,edges):
    '''edge u-v is valid in the eulerian path iff it is not a bridge (case 2) or it is the unique possible edge 
    from u (case 1)'''
    neighbors=neighbor(vertices,edges)
    
    #case 1
    if len(neighbors[u])==1: return True

    #case 2
    else: #Checking that it is not a bridge
        
        visited={v:False for v in range(len(vertices))}

        count1 = DFScount(u,vertices,edges)
        
        #Remove edge (u, v) and after removing the edge, count vertices reachable from u
        rmvEdge(u, v,neighbors,edges)
        visited={v:False for v in range(len(vertices))}

        count2 = DFScount(u,vertices,edges)
 
        #Add the edge back to the graph
        addEdge(u,v,neighbors,edges)
 
        #If count1 is greater, then edge (u, v) is a bridge
        return False if count1 > count2 else True

def eulerian_path(v0,vertices,edges,neighbors):
    if len(neighbors[v0])==0:
        return []
    L=[]
    for v in neighbors[v0]:
        if is_valid_nextEdge(v0,v,vertices,edges):
            L.append(v)
            rmvEdge(v0,v,neighbors,edges)
            return L+eulerian_path(v,vertices,edges,neighbors)


#Now, if we have a graph, which is not eulerian, let's modify it to make it eulerian

def extract_min_dist(frontier,dist):
    # in a frontier list, this function return the element with the closest distance 
    min_vertex = frontier[0]
    for vertex in frontier:
        if dist[vertex] < dist[min_vertex]:
            min_vertex = vertex
    frontier.remove(min_vertex)
    return min_vertex

def shortest_path (s,vertices,edges):
    # implementing djikstra to get to know the shortest distance from s to any other related vertex
    neighbors=neighbor_w(vertices,edges)
    frontier = [s]
    parent = {s : None}
    dist = { s : 0}
    while len( frontier ) >0:
        x = extract_min_dist(frontier,dist)
        for y in neighbors[x]:
            if y[0] not in parent :
                frontier.append(y[0])
            # update
            new_dist = dist[x]+ y[1]
            if y[0] not in dist or dist[y[0]] > new_dist :
                dist [y[0]] = new_dist
                parent [y[0]] = x
    return parent,dist

def odd_vertices(neighbours):
    #extracts the vertices with odd degree in the graph
    odd_v=[]
    for v in neighbours:
        if len(neighbours[v])%2==1:
            odd_v.append(v)
    return odd_v

def compute_dist_odd(odd_v,vertices,edges):
    # computes the shortest distance between every 2 vertices with odd degree 
    distances={}
    for i in range(len(odd_v)-1):
        L=shortest_path(odd_v[i],vertices,edges)[1]
        for j in range(i+1,len(odd_v)):
            distances[(min(odd_v[i],odd_v[j]),max((odd_v[i],odd_v[j])))]=L[odd_v[j]]
    return distances

def find_best_pairing(odd_v,distances):
    '''finds the pairing of odd vertices with the least total cost, it runs over every permutation
    of the vertices and starts computing for each permutation the cost of its pairing, and does a branch
    and bound to not complete computing if the distance is not the best'''
    partitions=list(permutations(odd_v))
    partition=partitions[0]
    best_dist=0
    best_partition=0
    for i in range(len(partition)-1):
        if i%2==0:
            best_dist+=distances[(min(partition[i],partition[i+1]),max(partition[i],partition[i+1]))]
    i=1
    while i<len(partitions):
        distance=0
        partition=partitions[i]
        idx_current=0
        
        while idx_current< len(partition)-1:
            if idx_current%2==0:
                distance+=distances[(min(partition[idx_current],partition[idx_current+1]),max(partition[idx_current],partition[idx_current+1]))]
            if distance>best_dist:
                idx_current=len(partition)
                i+=1
            idx_current+=1
        if distance<best_dist:
            best_dist=distance
            best_partition=i
        i+=1
    return partitions[best_partition]


def add_best_edges(best_pairing,distances,edges,neighbors):
    '''after we found the best pairing , we are going to add its edges to our graph and make it 
    semi-eulerian, we need to find 2 vertices to leave out, and the others to link'''
    
    #let's identify the vertices to leave
    distance=0
    biggest_dist=0
    to_leave=0

    for i in range(len(best_pairing)-1):
        if i%2==0:
            distance=distances[(min(best_pairing[i],best_pairing[i+1]),max(best_pairing[i],best_pairing[i+1]))]
            if distance>biggest_dist:
                biggest_dist=distance
                to_leave=i

    for i in range(len(best_pairing)-1):
        if i%2==0:
            if i!=to_leave:
                addEdge(best_pairing[i],best_pairing[i+1],neighbors,edges)
    return best_pairing[to_leave]

def djikstra_path(u,v,dic):
    path=[v]
    parent=v
    while parent!=u:
        parent=dic[parent]
        path=[parent]+path
    return path

def augment_path(euler_path,odd_v,vertices,edges):
    '''takes an euler path on the augmented graph and the djikstra dicts for every odd degree vertex,
    and returns a semi-eulerian path of the original graph'''
    path=[]
    for i in range(len(euler_path)-1):
        if euler_path[i] in odd_v and euler_path[i+1] in odd_v:
            path+=djikstra_path(euler_path[i],euler_path[i+1],shortest_path(euler_path[i],vertices,edges)[0])[:-1]
        else: 
            path+=[euler_path[i],euler_path[i+1]][:-1]
    return path+[euler_path[-1]]

def main():
    
    in_file, plot_graph = parse_cmd_line()
    vertices, edges = parse_file(in_file)
    edges0=edges
    print(f"#E={len(edges)}, #V={len(vertices)}")

    start_time = time.time()
    test=test_connexe(vertices,edges)
    if not test:
        print('Graph is not connexe, a semi eulerian path doesn t exist')
    
    else:
        print('Graph is connexe')
        euler_test=test_eulerian(vertices,edges)
        if euler_test[0]==1:
            print('Graph is eulerian')
            # if the graph is eulerian, return eulerian path starting from 0
            edges1=E(edges)
            neighbors=neighbor(vertices,edges1)
            print('An eulerian path is: ',[0]+eulerian_path(0,vertices,edges1,neighbors))

        if euler_test[0]==2:
            print('Graph is semi eulerian')
            # if graph semi eulerian, return eulerian path starting from an odd degree vertex
            edges1=E(edges)
            neighbors=neighbor(vertices,edges1)
            v0=euler_test[1]
            print('A semi eulerian path is: ',[v0]+eulerian_path(v0,vertices,edges1,neighbors))
        elif euler_test[0]==0:
            print('Graph is non eulerian, nor semi-eulerian')
            #else
            edges=E1(edges)
            neighbors=neighbor(vertices,edges)
            #find all odd degree vertices
            odd_v=odd_vertices(neighbors)
            #compute pairwise distances between each of them
            distances=compute_dist_odd(odd_v,vertices,edges)
            #find the best pairing
            
            best_pairing=find_best_pairing(odd_v,distances)
            print('best pairing: ', best_pairing)
            #construct the new augmented semi-eulerian graph
            edges1=E(edges)
            new_edges,new_neighbors=edges1,neighbors
            v0=add_best_edges(best_pairing,distances,new_edges,new_neighbors)
            #find the eulerien path on the augmented graph
            euler_path_g=[v0]+eulerian_path(v0,vertices,new_edges,new_neighbors)
            # print(euler_path_g)
            semi_eulerian_path=augment_path(euler_path_g,odd_v,vertices,edges)
            print('A semi-eulerian path is: ', semi_eulerian_path)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution in:", execution_time, "sec")
    graph = Graph(vertices, edges0)
    if plot_graph:
        graph.plot()


if __name__ == "__main__":
    main()