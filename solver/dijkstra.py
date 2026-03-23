from scipy.sparse.csgraph import dijkstra

from graph import Graph


# TODO make it a class so it can be a service called by every method used for perfect-matching
def compute_dijkstra(g: Graph):
    graph = g.matrix()
    dist_matrix, predecessors = dijkstra(
        csgraph=graph,
        directed=False,
        return_predecessors=True,
        indices=g.odd_vertices(),
    )
    return [dist_matrix, predecessors]
