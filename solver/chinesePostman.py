from hierholzer import hierholzer
from naiveMatching import naive_matching

from graph import Graph


def chinese_postman_solver_generic(g: Graph, eulerian_cycle, matching):
    if not g.is_eulerian():
        print("no Eulerian cycle in the graph ; adding missing edges", flush=True)
        g = matching(g)
        print("computing Eulerian cycle on enriched graph", flush=True)
    else:
        print("Graph is Eulerian, computing cycle directly")
    cycle = eulerian_cycle(g)
    return cycle_to_path(cycle)


def cycle_to_path(cycle):
    # TODO
    # if there are virtual edges, remove the one of maximum weight
    # present the path in a readable way
    return cycle


def chinese_postman_solver(g: Graph):
    # TODO
    # Refacto to inject smallest path strategy as well (here choice to use Dijkstra is hidden)
    # Implement and use Edmond's blossom algorithm instead of naive matching : will increase computation time but will give optimal solution
    return chinese_postman_solver_generic(g, hierholzer, naive_matching)
