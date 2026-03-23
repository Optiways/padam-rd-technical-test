from hierholzer import cycle, hierholzer

from graph import Graph
from input import parse_file


# Refacto : have a fixture file
def read_graph(in_file: str) -> Graph:
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    return Graph(vertices, edges)


triangle = read_graph("instances/triangle.txt")
line = read_graph("instances/line.txt")
farfalle = read_graph("instances/farfalle.txt")

# End todo refacto


def cycle_tests():
    assert cycle(triangle.clone(), 0, 0) == [
        4,
        [triangle.edges[0], triangle.edges[2], triangle.edges[1]],
    ]


def hierholzer_tests():
    assert hierholzer(triangle.clone()) == [
        4,
        [triangle.edges[0], triangle.edges[2], triangle.edges[1]],
    ]
    assert hierholzer(farfalle.clone()) == [
        7,
        [
            farfalle.edges[0],
            farfalle.edges[2],
            farfalle.edges[3],
            farfalle.edges[5],
            farfalle.edges[4],
            farfalle.edges[1],
        ],
    ]


def tests():
    cycle_tests()
    hierholzer_tests()
