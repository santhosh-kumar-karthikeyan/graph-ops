class Graph:
    def __init__(self, nodes = []):
        self.adj_list = []
        self.num_nodes = 1
        for node in nodes:
            self.adj_list[self.num_nodes - 1] = { "name" : node,
                                                 "neighbours": []}
            self.num_nodes += 1
    def add_node(self, parents, new_node):
        self.adj_list[self.num_nodes - 1] = {"name" : new_node,
                                             "neighbours" : []}
        self.num_nodes += 1
        