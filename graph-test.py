from graph import Graph
from input import parse_file


# Refacto : have a fixture file
def read_graph(in_file: str) -> Graph:
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    return Graph(vertices, edges)


triangle = read_graph("instances/triangle.txt")
line = read_graph("instances/line.txt")
paris = read_graph("instances/paris_map.txt")

## End refacto needed


def odd():
    assert triangle.is_eulerian()
    assert not line.is_eulerian()
    assert triangle.odd_vertices() == []
    assert line.odd_vertices() == [0, 2]
    assert not paris.is_eulerian()


def next():
    assert triangle.next(0, 1) == [1, 2]
    assert triangle.next(1, 2) == [2, 0]  # Next
    assert triangle.next(0, 0) == [2, 2]  # Reverse
    assert line.next(1, 2) == [-1, None]  # End of the line


def tests():
    odd()
    next()
