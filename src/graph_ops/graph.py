import json,os
from tabulate import tabulate
import networkx as nx
from asciinet import graph_to_ascii
FILENAME = ".graph_data.json"

class Graph:
    def __init__(self, nodes: list[str] | dict[str, dict[str, list[str]]] | None = None) -> None:
        if nodes is None:
            nodes = {}
        self.adj_list: dict[str, dict[str, list[str]]] = {}
        self.num_nodes: int = 0
        for node in nodes:
            self.adj_list[node] = {"neighbours": []}
            self.num_nodes += 1

    def add_node(self, new_node: str, neighbours: list[str] | None = None) -> str | None:
        if neighbours is None:
            neighbours = []
        if(new_node in self.adj_list.keys()):
            return f"{new_node} already exists"
        self.adj_list[new_node] = {"neighbours": neighbours}
        self.num_nodes += 1
        for neighbour in neighbours:
            if new_node not in self.adj_list[neighbour]["neighbours"]:
                self.adj_list[neighbour]["neighbours"].append(new_node)
        return f"{new_node} added to the graph."

    def remove_node(self, target_node: str) -> str:
        for node in self.adj_list:
            if target_node in self.adj_list[node]["neighbours"]:
                self.adj_list[node]["neighbours"].remove(target_node)
        presence: bool | dict[str, list[str]] = self.adj_list.pop(target_node, False)
        if not presence:
            return(f'Node {target_node} not found.')
        self.num_nodes -= 1
        return f"{target_node} removed from the graph"

    def check_edge(self, start: str, end: str) -> str:
        # -1 if start doesn't exist, -2 if end doesn't exist, 1 elsewhere (even when an edge doesn't exist)
        if(start == end):
            return f"Start node is same as end node: {start}"
        if start not in self.adj_list:
            return f"{start} doesn't exist"
        if end not in self.adj_list:
            return f"{end} doesn't exist"
        return ""

    def add_edge(self, start: str, end: str) -> str:
        # direction might be needed in the future, so the naming convention of start and end
        edge_presence: str = self.check_edge(start, end)
        if edge_presence != "":
            return edge_presence
        edge_exists : bool = True
        if start not in self.adj_list[end]["neighbours"]:
            self.adj_list[end]["neighbours"].append(start)
            edge_exists = False
        if end not in self.adj_list[start]["neighbours"]:
            self.adj_list[start]["neighbours"].append(end)
            edge_exists = False
        if edge_exists:
            return f"Edge already exists between {start} and {end}"
        return f"Edge added between {start} and {end}"

    def remove_edge(self, start: str, end: str) -> str:
        edge_presence: str = self.check_edge(start, end)
        if edge_presence != "":
            return edge_presence
        if start in self.adj_list[end]["neighbours"]:
            self.adj_list[end]["neighbours"].remove(start)
        if end in self.adj_list[start]["neighbours"]:
            self.adj_list[start]["neighbours"].remove(end)
        return f"Edge between {start} and {end} removed."

    def display_node(self, node: str) -> str:
        if node not in self.adj_list.keys():
            return f"{node} deesn't exist"
        if not self.adj_list[node]["neighbours"]:
            return f"{node} doesn't have any neighbours"
        path: str = f'{node} '
        neighbours: list[str] = self.adj_list[node]["neighbours"]
        first: bool = True
        for neighbour in neighbours:
            path += f' -> {neighbour }' if first else f' , {neighbour}'
            first = False
        return path + '\n'

    def display_graph(self) -> str | None:
        if len(self.adj_list) == 0:
            return "No nodes to display"
        edges: set = set()
        for node,info in self.adj_list.items():
            for neighbour in info["neighbours"]:
                edge = tuple(sorted((node,neighbour)))
                edges.add(edge)
        G = nx.Graph(list(edges))
        for node in self.adj_list:
            if not self.adj_list[node]["neighbours"]:
                G.add_node(node)
        print(graph_to_ascii(G))

    def bfs(self, start: str, target: str) -> str:
        fringe: list[str] = [start]
        explored: list[str] = []
        trace: list[list[str]] = []
        print(f"BFS for target {target}")
        while len(fringe) != 0:
            trace.append([str(fringe), str(explored)])
            curr_node: str = fringe.pop(0)
            if curr_node not in explored:
                explored.append(curr_node)
            if curr_node == target:
                print(tabulate(trace,headers=["Fringe","Explored"],tablefmt="fancy_grid"))
                return " -> ".join(explored)
            for node in self.adj_list[curr_node]["neighbours"]:
                if node not in fringe and node not in explored:
                    fringe.append(node)
        print(tabulate(trace,headers=["Fringe","Explored"],tablefmt="fancy_grid"))
        return f"{target} doesn't exist"

    def dfs_helper(self, curr_node: str, explored: list[str], target: str,path: list[str] | None = None, trace: list[list[str]] = []) -> bool:
        if path is None:
            path = []
        path.append(curr_node)
        trace.append([str(path), str(explored)])
        if curr_node == target:
            return True
        for node in self.adj_list[curr_node]["neighbours"]:
            if node not in explored:
                explored.append(node)
                if self.dfs_helper(node, explored, target,path,trace):
                    return True
        path.pop()
        return False

    def dfs(self, start: str, target: str) -> str:
        explored: list[str] = [start]
        trace:list[list[str]] = []
        path: list[str] = []
        if self.dfs_helper(start, explored, target,path,trace):
            print(tabulate(trace,headers=["Fringe","Explored"],tablefmt="fancy_grid"))
            return " -> ".join(explored)
        else:
            print(tabulate(trace,headers=["Fringe","Explored"],tablefmt="fancy_grid"))
            return f"{target} is unreachable"
        
    def to_dict(self) -> list[str] | dict[str, dict[str, list[str]]]:
        return self.adj_list

    def from_dict(self, data: dict[str, dict[str, list[str]]]) -> None:
        self.adj_list = data
        self.num_nodes = len(data)
        
    def save(self):
        with(open(FILENAME, "w")) as f:
            json.dump(self.to_dict(),f)
    
    def load(self):
        if(os.path.exists(FILENAME)):
            with(open(FILENAME,"r")) as f:
                self.from_dict(json.load(f))

if __name__ == "__main__":
    graph: Graph = Graph()
    graph.add_node("a")
    graph.add_node("a")
    graph.add_node("b")
    graph.add_node("c")
    graph.add_node("d")
    graph.add_node("e")
    graph.add_node("f")
    graph.add_node("g")
    graph.add_edge("a", "b")
    graph.add_edge("b", "d")
    graph.add_edge("b", "e")
    graph.add_edge("c", "f")
    graph.add_edge("c", "g")
    graph.add_edge("a", "c")
    # bfs_path: str | list[str] = graph.bfs("a", "g")
    # if bfs_path != []:
    #     print(bfs_path)
    # else:
    #     print(f'Target node not found')
    # dfs_path: str = graph.dfs('a', 'd')
    # if dfs_path != "":
    #     print(dfs_path)
    # else:
    #     print('Target node not found')
    # graph.remove_node("b")
    graph.display_graph()
    print("-----------------------------------------")
    graph.remove_edge("a","b")
    graph.display_graph()