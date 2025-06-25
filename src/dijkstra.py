from collections import defaultdict
import heapq
import math

from .graph import Graph


def dijkstra(graph: Graph, start: int, target: int) -> tuple[int, list[int]]:
    """Return the shortest path between start and target in graph using Dijkstra's algorithm"""
    if start == target:
        return dijkstra_path((0, start, -1))

    # open: list[tuple[cost, vertex, prev_edge_idx, this]]
    open: list[tuple[int, int, int, tuple]] = [(0, start, -1, tuple())]
    closed: set[int] = set()
    distances = defaultdict(lambda: math.inf)

    while open:
        cost, u, prev_idx, prev = heapq.heappop(open)
        if u in closed:
            continue
        closed.add(u)
        if u == target:
            return dijkstra_path((cost, u, prev_idx, prev))
        for v, edge_idx in graph.adj_list[u]:
            w = graph.edge_map[(u, v, edge_idx)][2]
            new_cost = cost + w
            if new_cost < distances[v]:
                distances[v] = new_cost
                heapq.heappush(
                    open, (new_cost, v, edge_idx, (cost, u, prev_idx, prev))
                )

    return dijkstra_path((0, None, -1))


def dijkstra_path(last: tuple) -> tuple[int, list[int]]:
    """Rebuild the path from dijkstra search"""
    path = []
    cost = last[0]
    while last[2] != -1:
        path.append((last[1], last[3][1], last[2]))
        last = last[3]
    path.reverse()
    return cost, path
