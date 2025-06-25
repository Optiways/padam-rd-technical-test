from copy import deepcopy

from .eulerize_blossom import eulerize_blossom
from .eulerize_heuristic import eulerize_heuristic
from .graph import Graph, Edge


SOLVERS = {"blossom": eulerize_blossom, "heuristic": eulerize_heuristic}


def process_graph(graph: Graph, plot_graph: bool, solver: str) -> None:
    try:
        print(f"{'Vertices:':<15}{len(graph.vertices)}")
        print(f"{'Edges:':<15}{len(graph.edges)}")
        path, start = solution(graph, solver)
        check_solution(graph, path, start)
        edge_sum = sum(edge[2] for edge in graph.edges)
        print(f"{'Edge Weight:':<15}{edge_sum}")
        path_weigth = sum(edge[2] for edge in path)
        print(
            f"{'Path Weight:':<15}{path_weigth:<5} ({path_weigth / edge_sum:.0%})"
        )
        print(
            f"{'Path Length:':<15}{len(path):<5} ({len(path) / len(graph.edges):.0%})"
        )
        if plot_graph:
            graph.plot()
            graph.display_path(path=path)
    except RuntimeError as error:
        print(type(error).__name__ + ":", error)


def solution(graph: Graph, solver: str) -> tuple[list[Edge], int]:
    """Implement a not so naive solution to find a path in the graph which travels all edges."""
    assert graph.is_connected(), "graph must be connected"
    if len(graph.edges) < 3:
        return deepcopy(graph.edges), graph.edges[0][0]
    graph = deepcopy(graph)
    odd_vertices = graph.get_odd_vertices()
    print(f"{'Odd Nodes:':<15}{len(odd_vertices)}")
    if len(odd_vertices) == 0:
        return eulerian_path(graph, [0, 0])
    if len(odd_vertices) == 2:
        return eulerian_path(graph, odd_vertices)
    SOLVERS[solver](graph, odd_vertices)
    odd_vertices = graph.get_odd_vertices()
    assert len(odd_vertices) == 2, "graph is not semi-eulerian"
    return eulerian_path(graph, odd_vertices)


def eulerian_path(graph: Graph, odd: list[int]) -> tuple[list[Edge], int]:
    """Return eulerian path in graph starting at start using Hierholzer's algorithm"""
    stack = [(odd[0], -1)]
    path, ret = [], []
    adj = deepcopy(graph.adj_list)
    while stack:
        curr, _ = stack[-1]
        if adj[curr]:
            v, id = adj[curr].pop()
            adj[v].remove((curr, id))
            stack.append((v, id))
        else:
            path.append(stack.pop())
    for (u, id), (v, _) in zip(path[:-1], path[1:]):
        ret.append(graph.edge_map[(u, v, id)])
    return ret, odd[1]


def check_solution(graph: Graph, path: list[Edge], start: int) -> None:
    """Raise an expection if the path in not semi-eulerian in graph"""
    for e in path:
        assert start in e[:2], "path is disconnected"
        start = e[1] if start == e[0] else e[0]
    assert set(graph.edges) - set(path) == set(), "not all edges are covered"
