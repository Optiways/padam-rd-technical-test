from input import parse_cmd_line, parse_file
from graph import Graph
from connection_check import Graph_dict

def check_eulerian_path(degrees_table):
    eulerian = True
    nb_odd = 0
    for vertex in degrees_table:
        if degrees_table[vertex]%2 != 0:
            eulerian = False
            nb_odd +=1
    return eulerian, nb_odd

def main():
    in_file, plot_graph = parse_cmd_line()
    vertices, edges, vertices_degree = parse_file(in_file)
    print(f"#E={len(edges)}, #V={len(vertices)}")
    graph = Graph(vertices, edges)

    print(vertices_degree)

    
    g = Graph_dict()
    g.create_graph(in_file)


    # Check if graph is connected
    connect, path = g.is_connected()
    print("Is the graph connected?", connect)
    if connect:
        #Check if graph is eulerian or not
        is_eulerian_path, nb_odd_degrees = check_eulerian_path(vertices_degree)
        if is_eulerian_path and nb_odd_degrees == 0:
            print("It's an Eulerian cycle")
            print("Shortest path is :", path)
            print("Total distance =", sum([edge[2] for edge in edges]))
        elif is_eulerian_path and 0<nb_odd_degrees <=2 :
            print("It's an Eulerian path")
            print("Shortest path is :", path) #Todo: modify path code to start from one of the vertices with odd degree
            print("Total distance =", sum([edge[2] for edge in edges]))
    else:
        vertices_id = set()
        for i in range(len(vertices)):
            vertices_id.add(i)
        M = g.not_connected(vertices_id)
        for i in range(len(M)): #Todo: shorten the connectivity checking by transforming it into a function or method (redundant lines)
            connect_sub, sub_path = M[i].is_connected()
            print("Is the subgraph connected?", connect_sub)
            M[i].display()
            vertices_degree = M[i].sub_graph_degrees()
            print(vertices_degree)
            is_eulerian_path, nb_odd_degrees = check_eulerian_path(vertices_degree)
            if is_eulerian_path and nb_odd_degrees == 0:
                print("It's an Eulerian cycle")
                print("Shortest path is :", path)
                print("Total distance =", sum([edge[2] for edge in edges]))
            elif is_eulerian_path and 0<nb_odd_degrees <=2 :
                print("It's an Eulerian path")
                print("Shortest path is :", path)
                print("Total distance =", sum([edge[2] for edge in edges]))


    # if plot_graph:
    #     graph.plot()

    #Todo: add case of no Eulerian path or cycle

if __name__ == "__main__":
    main()
