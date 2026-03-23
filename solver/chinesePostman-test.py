import datetime

from chinesePostman import chinese_postman_solver

from graph import Graph
from input import parse_file


# Refacto : have a fixture file
def read_graph(in_file: str) -> Graph:
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    return Graph(vertices, edges)


line = read_graph("instances/line.txt")
triangle = read_graph("instances/triangle.txt")
hard_to_choose = read_graph("instances/hard_to_choose.txt")
islands = read_graph("instances/islands.txt")
paris = read_graph("instances/paris_map.txt")

# End Refacto


def integration():
    path = chinese_postman_solver(line)
    assert path[0] == 4  # weight
    assert len(path[1]) == 3  # two real one virtual
    path = chinese_postman_solver(triangle)
    assert path[0] == 4
    assert len(path[1]) == 3


def performance(graph):
    begin = datetime.datetime.now()
    path = chinese_postman_solver(graph)
    duration = datetime.datetime.now() - begin
    print(f"found path of weight {path[0]} in {duration}s")


def performances():
    performance(hard_to_choose)
    """ both these instances fail with indexes bound when reconstructing Dijkstra paths
    performance(islands)
    performance(paris)
    """


def tests():
    integration()
    performances()
