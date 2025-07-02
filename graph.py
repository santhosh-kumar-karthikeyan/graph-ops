class Graph:
    def __init__(self, nodes = {}):
        self.adj_list = {}
        self.num_nodes = 1
        for node in nodes:
            self.adj_list[node] = list()
            self.num_nodes += 1
            
    def add_node(self, new_node, neighbours = list()):
        self.adj_list[new_node] = neighbours
        self.num_nodes += 1
        for neighbour in neighbours:
            if(new_node not in self.adj_list[neighbour]):
                self.adj_list[neighbour].append(new_node)
        
    def remove_node(self,target_node):
        for node in self.adj_list:
            if(target_node in self.adj_list[node]):
                self.adj_list[node].remove(target_node)
        presence = self.adj_list.pop(target_node,False)
        if not presence:
            print(f'Node {target_node} not found.')
        else:
            self.num_nodes -= 1
            
    def check_edge(self,start,end):
        # -1 if start doesn't exist, -2 if end doesn't exist, 1 elsewhere (even when an edge doesn't exist)
        if(start not in self.adj_list):
            return -1
        if end not in self.adj_list:
            return -2
        return 1
    
    def add_edge(self,start, end):
        #direction might be needed in the future, so the naming convention of start and end
        edge_presence = self.check_edge(start,end)
        if edge_presence != 1:
            return edge_presence
        if(start not in self.adj_list[end]):
            self.adj_list[end].append(start)
        if(end not in self.adj_list[start]):
            self.adj_list[start].append(end)
        
    def del_edge(self,start,end):
        edge_presence = self.check_edge(start,end)
        if edge_presence != 1:
            return edge_presence
        if(start in self.adj_list[end]):
            self.adj_list[end].remove(start)
        if(end in self.adj_list[start]):
            self.adj_list[start].remove(end)
        
    def display_node(self,node):
        print(f'{node} -> ',end='')
        first = True
        for neighbour in self.adj_list[node]:
            print(f' {neighbour}', end="") if first else print(f' , {neighbour}',end="")
            first = False
        print()
        
    def display_graph(self):
        for node in self.adj_list:
            self.display_node(node)
    
    def bfs(self,start,target):
        fringe = list(start)
        explored = list()
        while len(fringe) != 0:
            print(f'Fringe: {fringe}\nExplored: {explored}')
            curr_node = fringe.pop(0)
            if curr_node not in explored:
                explored.append(curr_node)
            if curr_node == target:
                return " -> ".join(explored)
            for node in self.adj_list[curr_node]:
                if node not in fringe:
                    fringe.append(node)
        return []
        
    def dfs_helper(self,curr_node,explored, target):
        if curr_node == target:
            return True
        for node in self.adj_list[curr_node]:
            if node not in explored:
                explored.append(node)
                if self.dfs_helper(node,explored,target):
                    return True
        return False
    
    def dfs(self,start,target):
        explored = [start]
        if self.dfs_helper(start,explored,target):
            return (" -> ".join(explored))
        else:
            return ""

if __name__ == "__main__":
    graph = Graph(["a", "b","c","d","e","f","g"]);
    graph.add_edge("a","b")
    graph.add_edge("a","c")
    graph.add_edge("b","d")
    graph.add_edge("b", "e")
    graph.add_edge("c","f")
    graph.add_edge("c", "g")
    graph.display_graph()
    bfs_path = graph.bfs("a","g")
    if bfs_path != []:
        print(bfs_path)
    else:
        print(f'Target node not found')
    dfs_path = graph.dfs('a','d')
    if dfs_path != "":
        print(dfs_path)
    else:
        print('Target node not found')
