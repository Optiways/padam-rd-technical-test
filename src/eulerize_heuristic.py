from itertools import combinations

from .dijkstra import dijkstra
from .graph import Graph


def manhattan(graph: Graph, start: int, end: int) -> float:
    """Return manhattan distance between start and end"""
    return abs(graph.vertices[start][0] - graph.vertices[end][0]) + abs(
        graph.vertices[start][1] - graph.vertices[end][1]
    )


def greedy_pairing(graph: Graph, dists: list, odd: list[int]) -> list:
    """Pair nodes by distance greedily, dists must be sorted
    The last (largest) pair of nodes is skipped"""
    paths = []
    closed: set[int] = set()
    for it in dists:
        if len(paths) == len(odd) // 2 - 1:
            return paths
        pair = it[1]
        if pair[0] in closed or pair[1] in closed:
            continue
        paths.append(dijkstra(graph, *pair)[1])
        closed.add(pair[0])
        closed.add(pair[1])
    return paths


def eulerize_heuristic(graph: Graph, odd: list) -> None:
    """Adds edges inplace to graph to make it semi-eulerian using manhattan heuristic greedy paring.
    After solving selected paths are added to graph"""
    dists = list((manhattan(graph, *c), c) for c in combinations(odd, 2))
    dists.sort()
    paths = greedy_pairing(graph, dists, odd)
    graph.add_paths(paths)
