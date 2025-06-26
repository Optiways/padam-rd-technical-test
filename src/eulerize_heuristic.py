from collections import Counter
from itertools import combinations

from .dijkstra import dijkstra
from .graph import Graph


def manhattan(graph: Graph, start: int, end: int) -> float:
    """Return manhattan distance between start and end"""
    return abs(graph.vertices[start][0] - graph.vertices[end][0]) + abs(
        graph.vertices[start][1] - graph.vertices[end][1]
    )


def greedy_pairing(graph: Graph, dists: list) -> list:
    """Pair nodes by distance greedily, dists must be sorted
    The last (largest) pair of nodes is skipped"""
    paths = []
    closed: set[int] = set()
    for it in dists:
        pair = it[1]
        if pair[0] in closed or pair[1] in closed:
            continue
        paths.extend(dijkstra(graph, *pair)[1])
        closed.add(pair[0])
        closed.add(pair[1])
    return paths


def eulerize_heuristic(graph: Graph, odd: list) -> None:
    """Adds edges inplace to graph to make it semi-eulerian using manhattan heuristic greedy paring.
    After solving selected paths are added to graph
    If after paring an edge would appears more than twice in graph, it can be removed twice from the edge"""
    dists = list((manhattan(graph, *c), c) for c in combinations(odd, 2))
    dists.sort()
    paths = greedy_pairing(graph, dists)
    to_add = []
    max_edge = paths[0]
    for edge, count in Counter(paths).items():
        to_add.extend([edge] * (count % 2))
        if count % 2 and max_edge[2] < edge[2]:
            max_edge = edge
    to_add.remove(max_edge)
    graph.edges.extend(to_add)
    graph.build_adjacency_list()
