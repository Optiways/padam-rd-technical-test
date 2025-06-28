import heapq
from collections import deque
import sys

sys.setrecursionlimit(1000000)

def blossom_min_weight_matching(edges):
    """Algorithme de Blossom pour le couplage parfait de poids minimal."""
    if not edges:
        return []
    
    # Création d'un graphe complet pour l'algorithme
    nodes = set()
    for u, v, w in edges:
        nodes.add(u)
        nodes.add(v)
    nodes = sorted(nodes)
    n = len(nodes)
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    idx_to_node = {i: node for i, node in enumerate(nodes)}
    
    # Matrice des poids avec initialisation à -infini
    weights = [[-10**18] * n for _ in range(n)]
    for u, v, w in edges:
        i, j = node_to_idx[u], node_to_idx[v]
        weights[i][j] = weights[j][i] = -w  # Négatif pour poids minimal
    
    # Initialisation des structures de données pour Blossom
    match = [-1] * n
    label = [-1] * n
    parent = [-1] * n
    in_blossom = list(range(n))
    queue = deque()
    
    # Fonction pour trouver la base d'une fleur
    def find_base(v, w):
        path = set()
        while v != -1 or w != -1:
            if v != -1:
                if v in path:
                    return v
                path.add(v)
                v = parent[v] if parent[v] != -1 else -1
            v, w = w, v
        return -1

    # Algorithme principal de couplage
    for i in range(n):
        if match[i] == -1:
            label = [-1] * n
            parent = [-1] * n
            label[i] = 0
            queue.clear()
            queue.append(i)
            
            found = False
            while queue and not found:
                u = queue.popleft()
                for v in range(n):
                    if weights[u][v] != -10**18 and u != v:
                        if label[v] == -1:
                            label[v] = 1
                            parent[v] = u
                            if match[v] == -1:
                                # Chemin augmentant trouvé
                                x = u
                                y = v
                                while x != -1:
                                    temp = match[x]
                                    match[x] = y
                                    match[y] = x
                                    y = temp
                                    if y == -1:
                                        x = -1
                                    else:
                                        x = parent[y]
                                found = True
                                break
                            else:
                                label[match[v]] = 0
                                queue.append(match[v])
                        elif label[v] == 0:
                            base = find_base(u, v)
                            if base != -1:
                                # Contraction de la fleur
                                path_u = []
                                cur = u
                                while cur != base:
                                    path_u.append(cur)
                                    cur = parent[cur]
                                path_v = []
                                cur = v
                                while cur != base:
                                    path_v.append(cur)
                                    cur = parent[cur]
                                
                                for node in set(path_u + path_v):
                                    if label[node] != 0:
                                        label[node] = 0
                                        queue.append(node)
                                parent[u] = v
                                parent[v] = u

    # Construction des résultats
    matching = []
    for i in range(n):
        if i < match[i]:
            u = idx_to_node[i]
            v = idx_to_node[match[i]]
            w = -weights[i][match[i]]  # Rétablir le poids original
            matching.append((u, v, w))
    return matching

def sol(graph):
    vertices = graph.vertices
    edges = graph.edges
    n = len(vertices)
    m = len(edges)
    
    # Calcul des degrés et identification des sommets de degré impair
    degree = [0] * n
    for edge in edges:
        u, v, w, _, _ = edge
        degree[u] += 1
        degree[v] += 1
        
    T = [i for i in range(n) if degree[i] % 2 == 1]
    k = len(T)
    
    # Cas particulier: graphe déjà eulérien
    if k == 0:
        matching_pairs = []
        start_vertex = 0
    else:
        # Construction du graphe pour Dijkstra
        adj = [[] for _ in range(n)]
        for idx, edge in enumerate(edges):
            u, v, w, _, _ = edge
            adj[u].append((v, w, idx))
            adj[v].append((u, w, idx))
        
        # Calcul des plus courts chemins entre sommets impairs
        dist_T = [[10**18] * k for _ in range(k)]
        paths_T = [[[] for _ in range(k)] for _ in range(k)]
        
        for i in range(k):
            src = T[i]
            dist = [10**18] * n
            prev_vertex = [-1] * n
            prev_edge_index = [-1] * n
            dist[src] = 0
            heap = [(0, src)]
            
            while heap:
                d, u = heapq.heappop(heap)
                if d != dist[u]:
                    continue
                for v, w, idx in adj[u]:
                    nd = d + w
                    if nd < dist[v]:
                        dist[v] = nd
                        prev_vertex[v] = u
                        prev_edge_index[v] = idx
                        heapq.heappush(heap, (nd, v))
            
            for j in range(k):
                t_j = T[j]
                if i == j:
                    dist_T[i][j] = 0
                elif dist[t_j] < 10**18:
                    dist_T[i][j] = dist[t_j]
                    # Reconstruction du chemin
                    cur = t_j
                    path_edges = []
                    while cur != src:
                        idx_e = prev_edge_index[cur]
                        path_edges.append(idx_e)
                        cur = prev_vertex[cur]
                    path_edges.reverse()
                    paths_T[i][j] = path_edges
        
        # Option 1: Fermeture (couplage complet)
        closed_edges = []
        for i in range(k):
            for j in range(i + 1, k):
                if dist_T[i][j] < 10**18:
                    closed_edges.append((i, j, dist_T[i][j]))
        
        closed_matching = blossom_min_weight_matching(closed_edges) if closed_edges else []
        M0 = sum(edge[2] for edge in closed_matching) if closed_matching else 10**18
        
        # Option 2: Chemin ouvert (avec deux sommets libres)
        open_edges = closed_edges[:]  # Copie des arêtes fermées
        d1, d2 = k, k + 1  # Nœuds fictifs
        for i in range(k):
            open_edges.append((i, d1, 0))
            open_edges.append((i, d2, 0))
        
        open_matching = blossom_min_weight_matching(open_edges) if open_edges else []
        M_open = sum(edge[2] for edge in open_matching if edge[0] < k and edge[1] < k)
        
        # Identification des extrémités
        endpoints = []
        for edge in open_matching:
            if edge[0] < k and edge[1] >= k:
                endpoints.append(edge[0])
            elif edge[1] < k and edge[0] >= k:
                endpoints.append(edge[1])
        
        # Choix de la meilleure option
        if M0 <= M_open or len(endpoints) != 2:
            matching_pairs = [(edge[0], edge[1]) for edge in closed_matching]
            start_vertex = 0
        else:
            matching_pairs = [(edge[0], edge[1]) for edge in open_matching 
                             if edge[0] < k and edge[1] < k]
            start_vertex = T[endpoints[0]]
    
        # Duplication des arêtes sur les chemins de couplage
        multiplicity = [1] * m
        for i, j in matching_pairs:
            path_edges = paths_T[i][j]
            for e_idx in path_edges:
                multiplicity[e_idx] += 1
        
        # Construction du multigraphe
        adj_multigraph = [[] for _ in range(n)]
        for idx, edge in enumerate(edges):
            u, v, w, _, _ = edge
            for _ in range(multiplicity[idx]):
                adj_multigraph[u].append((v, idx))
                adj_multigraph[v].append((u, idx))
        
        # Algorithme de Hierholzer amélioré pour le chemin eulérien
        ptr = [0] * n
        stack = [start_vertex]
        path_edge_indices = []
        used = [0] * m  # Compteur d'utilisation par arête
        
        # Nouvel algorithme: parcours DFS récursif
        def dfs(u):
            while ptr[u] < len(adj_multigraph[u]):
                v, e_idx = adj_multigraph[u][ptr[u]]
                ptr[u] += 1
                if used[e_idx] < multiplicity[e_idx]:
                    used[e_idx] += 1
                    dfs(v)
                    path_edge_indices.append(e_idx)
        
        dfs(start_vertex)
        
        # Ajout des arêtes manquantes en cas de besoin
        for idx in range(m):
            remaining = multiplicity[idx] - used[idx]
            for _ in range(remaining):
                path_edge_indices.append(idx)
        
        result_edges = [edges[idx] for idx in path_edge_indices]
        return result_edges
    
    # Cas eulérien: parcours direct
    adj_multigraph = [[] for _ in range(n)]
    for idx, edge in enumerate(edges):
        u, v, w, _, _ = edge
        adj_multigraph[u].append((v, idx))
        adj_multigraph[v].append((u, idx))
    
    ptr = [0] * n
    stack = [0]
    path_edge_indices = []
    
    # Algorithme DFS récursif pour cas eulérien
    def dfs(u):
        while ptr[u] < len(adj_multigraph[u]):
            v, e_idx = adj_multigraph[u][ptr[u]]
            ptr[u] += 1
            dfs(v)
            path_edge_indices.append(e_idx)
    
    dfs(0)
    
    result_edges = [edges[idx] for idx in path_edge_indices]
    return result_edges