import json,os
FILENAME = ".graph_data.json"

class Graph:
    def __init__(self, nodes: list[str] | dict[str, dict[str, list[str]]] = {}) -> None:
        self.adj_list: dict[str, dict[str, list[str]]] = {}
        self.num_nodes: int = 1
        for node in nodes:
            self.adj_list[node] = {"neighbours": []}
            self.num_nodes += 1

    def add_node(self, new_node: str, neighbours: list[str] = []) -> None:
        self.adj_list[new_node] = {"neighbours": neighbours}
        self.num_nodes += 1
        for neighbour in neighbours:
            if new_node not in self.adj_list[neighbour]["neighbours"]:
                self.adj_list[neighbour]["neighbours"].append(new_node)

    def remove_node(self, target_node: str) -> None:
        for node in self.adj_list:
            if target_node in self.adj_list[node]["neighbours"]:
                self.adj_list[node]["neighbours"].remove(target_node)
        presence: bool | dict[str, list[str]] = self.adj_list.pop(target_node, False)
        if not presence:
            print(f'Node {target_node} not found.')
        else:
            self.num_nodes -= 1

    def check_edge(self, start: str, end: str) -> int:
        # -1 if start doesn't exist, -2 if end doesn't exist, 1 elsewhere (even when an edge doesn't exist)
        if start not in self.adj_list:
            return -1
        if end not in self.adj_list:
            return -2
        return 1

    def add_edge(self, start: str, end: str) -> None | int:
        # direction might be needed in the future, so the naming convention of start and end
        edge_presence: int = self.check_edge(start, end)
        if edge_presence != 1:
            return edge_presence
        if start not in self.adj_list[end]["neighbours"]:
            self.adj_list[end]["neighbours"].append(start)
        if end not in self.adj_list[start]["neighbours"]:
            self.adj_list[start]["neighbours"].append(end)

    def del_edge(self, start: str, end: str) -> None | int:
        edge_presence: int = self.check_edge(start, end)
        if edge_presence != 1:
            return edge_presence
        if start in self.adj_list[end]["neighbours"]:
            self.adj_list[end]["neighbours"].remove(start)
        if end in self.adj_list[start]["neighbours"]:
            self.adj_list[start]["neighbours"].remove(end)

    def display_node(self, node: str) -> None:
        print(f'{node} -> ', end='')
        neighbours: list[str] = self.adj_list[node]["neighbours"]
        first: bool = True
        for neighbour in neighbours:
            print(f' {neighbour}', end="") if first else print(f' , {neighbour}', end="")
            first = False
        print()

    def display_graph(self) -> None:
        for node in self.adj_list:
            self.display_node(node)

    def bfs(self, start: str, target: str) -> str | list[str]:
        fringe: list[str] = list(start)
        explored: list[str] = []
        while len(fringe) != 0:
            print(f'Fringe: {fringe}\nExplored: {explored}')
            curr_node: str = fringe.pop(0)
            if curr_node not in explored:
                explored.append(curr_node)
            if curr_node == target:
                return " -> ".join(explored)
            for node in self.adj_list[curr_node]["neighbours"]:
                if node not in fringe and node not in explored:
                    fringe.append(node)
        return []

    def dfs_helper(self, curr_node: str, explored: list[str], target: str) -> bool:
        if curr_node == target:
            return True
        for node in self.adj_list[curr_node]["neighbours"]:
            if node not in explored:
                explored.append(node)
                if self.dfs_helper(node, explored, target):
                    return True
        return False

    def dfs(self, start: str, target: str) -> str:
        explored: list[str] = [start]
        if self.dfs_helper(start, explored, target):
            return " -> ".join(explored)
        else:
            return ""
        
    def to_dict(self) -> dict[str, dict[str, dict[str]]]:
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
    graph: Graph = Graph(["a", "b", "c", "d", "e", "f", "g"])
    graph.add_edge("a", "b")
    graph.add_edge("a", "c")
    graph.add_edge("b", "d")
    graph.add_edge("b", "e")
    graph.add_edge("c", "f")
    graph.add_edge("c", "g")
    graph.display_graph()
    bfs_path: str | list[str] = graph.bfs("a", "g")
    if bfs_path != []:
        print(bfs_path)
    else:
        print(f'Target node not found')
    dfs_path: str = graph.dfs('a', 'd')
    if dfs_path != "":
        print(dfs_path)
    else:
        print('Target node not found')
