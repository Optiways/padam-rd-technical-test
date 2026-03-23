import datetime

from dijkstra import compute_dijkstra

from graph import Graph
from input import parse_file


# Refacto : have a fixture file
def read_graph(in_file: str) -> Graph:
    vertices, edges = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    return Graph(vertices, edges)


paris = read_graph("instances/paris_map.txt")

# End Refacto


def perf():
    begin = datetime.datetime.now()
    compute_dijkstra(paris)
    duration = datetime.datetime.now() - begin
    print(f"computed dijkstra in {duration}")


def tests():
    perf()
