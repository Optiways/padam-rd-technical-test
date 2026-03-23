import math

from dijkstra import compute_dijkstra

from graph import Graph


def vertices_to_path(g: Graph, vertices):
    edges = []
    for i in range(len(vertices) - 1):
        # TODO complexity is linear when it should be constant because the data structures don't work well with each other
        for edge in g.real_edges:
            if edge is None:
                continue
            # TODO create an explicit method for this
            if (edge[0] == vertices[i] and edge[1] == vertices[i + 1]) or (
                edge[0] == vertices[i + 1] and edge[1] == vertices[i]
            ):
                edges.append(edge)
                break
    return edges


# TODO : refacto separate recursive and global method
def compute_path(g: Graph, i: int, j: int, predecessors, vertices=[]):
    vertices.append(j)
    if i == j:
        return vertices_to_path(g, vertices)
    previous = predecessors[i][j]
    if previous < 0:
        return None
    return compute_path(g, i, previous, predecessors, vertices)


# simplest way to make graph eulerian : pair each odd vertex with another one
def naive_matching(g: Graph):
    odds = g.odd_vertices()
    print("odd vertices computed")
    if len(odds) % 2 != 0:
        raise Exception("Something is wrong")
    [dist_matrix, predecessors] = compute_dijkstra(g)
    print("Dijkstra computed")
    for k in range(len(odds) // 2):
        [i, j] = odds[2 * k : 2 * k + 2]
        weight = math.floor(dist_matrix[i][j])
        path = compute_path(g, i, j, predecessors)
        g.add_virtual_edge(i, j, weight, path)
    print(
        f"added {len(g.edges) - len(g.real_edges)} to a graph with {len(odds)} odd vertices",
        flush=True,
    )
    return g
