import datetime

from naiveMatching import naive_matching, vertices_to_path

from graph import Graph
from input import parse_file


# Refacto : have a fixture file
def read_graph(in_file: str) -> Graph:
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    return Graph(vertices, edges)


line = read_graph("instances/line.txt")
hard_to_choose = read_graph("instances/hard_to_choose.txt")
paris = read_graph("instances/paris_map.txt")


def to_path():
    assert vertices_to_path(line, [0, 1, 2]) == [line.edges[0], line.edges[1]]
    assert vertices_to_path(line, [2, 1, 0]) == [line.edges[1], line.edges[0]]
    assert vertices_to_path(line, [0, 2]) == []


def naive():
    naive_matching(line)
    assert line.is_eulerian()
    # we only test the added edge
    assert len(line.edges) == 3
    expected_edge = (
        0,
        2,
        2,
        (0.5, 0),
        (0.5, 2),
        [line.edges[1], line.edges[0]],
    )
    assert line.edges[2] == expected_edge


def perf(graph):
    begin = datetime.datetime.now()
    naive_matching(graph)
    duration = datetime.datetime.now() - begin
    print(f"found matching in {duration}")


def tests():
    to_path()
    naive()
    perf(hard_to_choose)
