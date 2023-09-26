from collections import defaultdict

class Graph_dict:
    def __init__(self):
        self.graph = defaultdict(list)
    
    def size(self):
        return len(self.graph)

    def display(self):
         for key, value in self.graph.items():
            print(f'{key}: {value}')

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def add_edge_sub(self, u, v):
        self.graph[u] = v
    
    #Gives all vertices' degree for a sub_graph
    def sub_graph_degrees(self):
        vertices_degree = {}
        for key,value in self.graph.items():
            vertices_degree[key] = len(value)
        return vertices_degree

    def create_graph(self, filename):
        with open(f"{filename}", "r") as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                continue
            splitted_line = line.strip("\n\r").split(" ")
            if len(splitted_line) == 2:
                continue
            elif len(splitted_line) == 3:
                vertex_1, vertex_2 = int(splitted_line[0]), int(splitted_line[1])
                self.add_edge(vertex_1,vertex_2)

            
    def dfs(self, v, visited, visited_path):
        visited[v] = True
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                visited_path.append((v,neighbor))
                self.dfs(neighbor, visited, visited_path)

    #alternative DFS code when a graph is not connected
    def dfs_not_connected(self, v, visited, visited_path, vertices):
        visited[v] = True
        vertices.add(v)
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                visited_path.append((v,neighbor))
                self.dfs_not_connected(neighbor, visited, visited_path, vertices)
    

    def is_connected(self):
        # Choose first starting vertex
        start_vertex = next(iter(self.graph))
        # Initialize visited vertices
        visited = {v: False for v in self.graph}
        visited_path = []
        self.dfs(start_vertex, visited, visited_path)
        # Check if all vertices are visited
        return all(visited.values()), visited_path
    
    def add_sub_graph(self,list_sub_graph,inf_limit, sup_limit):
        #Create a sub-graph 
        sub_graph = Graph_dict()
        #Store every key and their neighors with key's value between 2 index
        for key,value in self.graph.items():
            if inf_limit<=key<=sup_limit:
                sub_graph.add_edge_sub(key, value)
        #Add each sub-graph to a list of sub-graph
        list_sub_graph.append(sub_graph)

    def not_connected(self, vertices_id): #Todo: optimize some lines to shorten the code
        visited_vertices = set()
        start_vertex = next(iter(self.graph))
        visited_vertices.add(start_vertex)
        visited_path = []
        visited = {v: False for v in self.graph}
        list_sub_graph =[]
        
        #vertices_id stores every vertices from initial graph
        #visited_vertices stores every new unique vertex we meet
        while vertices_id != visited_vertices:
            next_vertex = next(iter(visited))
            self.dfs_not_connected(next_vertex, visited, visited_path, visited_vertices)
            #extraction of every vertices that are connected, i.e. every vertices with True value in visited
            true_keys = [key for key, value in visited.items() if value == True]
            #update of visited to get rid of already processed vertices
            visited = {key: value for key, value in visited.items() if not value}
            self.add_sub_graph(list_sub_graph,true_keys[0], true_keys[-1])
        return list_sub_graph
    


