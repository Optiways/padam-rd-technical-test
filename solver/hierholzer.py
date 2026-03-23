from typing import Union

from graph import Graph


# TODO : refacto to make it simpler
def cycle(g: Graph, initial_vertex: int, initial_edge_index: int):
    i = initial_edge_index
    edge = g.edges[i]
    if edge is None:
        return [0, []]
    vertex = initial_vertex
    weight = 0
    path = []
    # tour until either dead end or coming back to starting point
    while (
        vertex is not None
        and edge is not None
        and (vertex != initial_vertex or len(path) <= 0)
    ):
        weight += edge[2]
        path.append(edge)
        g.remove_edge(i)
        [j, next_vertex] = g.next(i, vertex)
        i = j
        edge = g.edges[i]
        vertex = next_vertex
    return [weight, path]


# TODO : linear complexity, find a way to have constant complexity if too much time spent here
def insert(host: list, to_add: list):
    if len(to_add) == 0:
        return host
    if len(host) == 0:
        return to_add
    vertex = to_add[0][0]
    for [i, edge] in enumerate(host):
        if edge[1] == vertex:
            return host[:i] + to_add + host[i:]
    # found no place to insert
    lisible_to_add = [edge[:2] for edge in to_add]
    lisible_host = [edge[:2] for edge in host]
    raise Exception(f"Impossible to insert {lisible_to_add} into {lisible_host}")


# TODO improve the complexity with better data structure
def next_start(g: Graph, path=[]):
    if len(path) == 0:
        if len(g.edges) < 1 or g.edges[0] is None:
            raise Exception("Impossible to compute Eulerian cycle")
        return [0, 0]
    for p in path:
        vertex = p[1]
        if g.is_hub(vertex):
            for [i, edge] in enumerate(g.edges):
                if edge is None:
                    continue
                if edge[0] == vertex:
                    return [vertex, i]
    raise Exception("Impossible to compute Eulerian cycle")


# TODO : if majority of time spent on this part of code
# improve data structure to have constant time for each operation
def hierholzer(input_graph: Graph) -> Union[list, None]:
    g = input_graph.clone()
    if len(g.edges) < 1 or g.edges[0] is None:
        raise Exception("Impossible to compute Eulerian cycle")
    [vertex, edge] = next_start(g)
    [weight, path] = cycle(g, vertex, edge)
    nb_tours = 1
    while g.has_unvisited_edges() and nb_tours < len(g.edges):  # safety to break
        [vertex, edge] = next_start(g, path)
        current_tour = cycle(g, vertex, edge)
        nb_tours += 1
        path = insert(path, current_tour[1])
        weight += current_tour[0]
    print(f"{nb_tours} tours", flush=True)
    return [weight, path]
