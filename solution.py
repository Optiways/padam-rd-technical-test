from collections import defaultdict, deque
import itertools
from graph import Graph, Edge
import random
import heapq


def find_minimal_path(graph: Graph) -> list:
    # 1) Trouver les sommets de degré impair
    degree = defaultdict(int)
    for u, v, *_ in graph.edges:
        degree[u] += 1
        degree[v] += 1

    odd_vertices = [v for v in degree if degree[v] % 2 != 0]

    if not odd_vertices:
        return find_eulerian_path(graph)
    print(f"Nombre de sommets de degré impairs : {len(odd_vertices)}")
    # 2) Appariement aléatoire des sommets impairs,
    # il faudrait les apparier par proximité mais quand il y en a beaucoup le temps de calcul explose
    # On pourrait se fixer un nombre de pairs à parcourir fixe tiré aléatoirement et on prend la meilleure paire
    random.shuffle(odd_vertices)
    matching = list(zip(odd_vertices[::2], odd_vertices[1::2]))

    # 3) Rajouter les arêtes pour relier les sommets de degré impairs (seulement entre chaque pairs identiféess)
    augmented_edges = graph.edges.copy()
    for u, v in matching:
        path = find_shortest_path(graph, u, v)
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            edge = next(
                e
                for e in graph.edges
                if (e[0] == a and e[1] == b) or (e[0] == b and e[1] == a)
            )
            augmented_edges.append(edge)

    # 4) Trouver un chemin eulérien dans le graphe modifié devenu eulérien
    return find_eulerian_path(Graph(graph.vertices, augmented_edges))


def find_shortest_path(graph: Graph, start: int, end: int) -> list:
    """
    Algorithme de Dijkstra
    """

    neighbors = defaultdict(list)
    for u, v, weight, *_ in graph.edges:
        neighbors[u].append((v, weight))
        neighbors[v].append((u, weight))

    distances = {node: float("inf") for node in range(len(graph.vertices))}
    distances[start] = 0
    previous_nodes = {node: None for node in range(len(graph.vertices))}
    queued = [(0, start)]

    while queued:
        current_distance, current_node = heapq.heappop(queued)
        # print(current_distance)
        if current_node == end:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in neighbors[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queued, (distance, neighbor))

    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()

    if path[0] == start:
        return path
    else:
        return []


def find_eulerian_path(graph: Graph) -> list:
    if not graph.edges:
        return []

    adj = defaultdict(deque)
    edge_count = defaultdict(int)
    edge_indices = {}

    for idx, edge in enumerate(graph.edges):
        u, v, weight, coord1, coord2 = edge
        adj[u].append(idx)
        adj[v].append(idx)
        edge_indices[idx] = edge
        edge_count[(u, v)] += 1
        edge_count[(v, u)] += 1

    start_vertex = graph.edges[0][0]

    degree = defaultdict(int)
    for u, v, *_ in graph.edges:
        degree[u] += 1
        degree[v] += 1

    odd_vertices = [v for v in degree if degree[v] % 2 != 0]

    if odd_vertices:
        start_vertex = odd_vertices[0]

    stack = [start_vertex]
    path = []
    used_edges = set()

    while stack:
        current_vertex = stack[-1]

        while adj[current_vertex]:
            edge_idx = adj[current_vertex].popleft()
            if edge_idx in used_edges:
                continue
            # print(edge_idx)
            # print(used_edges)
            edge = edge_indices[edge_idx]
            u, v, weight, coord1, coord2 = edge

            if u == current_vertex:
                next_vertex = v
            else:
                next_vertex = u

            used_edges.add(edge_idx)

            stack.append(next_vertex)
            current_vertex = stack[-1]
            break
        else:

            if stack:
                path.append(stack.pop())

    edge_path = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]

        found = False
        for edge in graph.edges:
            if (edge[0] == u and edge[1] == v) or (edge[0] == v and edge[1] == u):
                edge_path.append(edge)
                found = True
                break

        if not found:

            for edge in graph.edges:
                if (
                    (edge[0] == u and edge[1] == v) or (edge[0] == v and edge[1] == u)
                ) and edge not in edge_path:
                    edge_path.append(edge)
                    break

    return edge_path
