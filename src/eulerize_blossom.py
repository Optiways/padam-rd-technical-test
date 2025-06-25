from pymatching import Matching

from .graph import Graph


def eulerize_blossom(graph: Graph, odd: list) -> None:
    """Adds edges inplace to graph to make it semi-eulerian using PyMatching for MWPM.
    Every edge of the graph are added to the solver, syndrome contains the odd vertices.
    After solving selected paths are added to graph """
    m = Matching()
    for idx, (u, v, w, _, _) in enumerate(graph.edges):
        m.add_edge(u, v, fault_ids=idx, weight=w)
    syndrome = [1 if i in odd else 0 for i in range(len(graph.vertices))]
    corr = m.decode(syndrome)
    matched_edges = [graph.edges[i] for i, bit in enumerate(corr) if bit]
    max_edge = max(matched_edges, key=lambda e: e[2])
    matched_edges.remove(max_edge)
    graph.edges.extend(matched_edges)
    graph.build_adjacency_list()
