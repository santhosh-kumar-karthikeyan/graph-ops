import json,os
from tabulate import tabulate
import networkx as nx
from asciinet import graph_to_ascii
from typing import TypedDict
FILENAME = ".graph_data.json"

class Graph:
    def __init__(self) -> None:
        self.adj_list: dict[str, dict[str, int]] = {}
        self.num_nodes: int = 0

    def add_node(self, new_node: str, neighbours: dict[str, int] | None = None) -> str | None:
        if neighbours is None:
            neighbours = {}
        if(new_node in self.adj_list.keys()):
            return f"{new_node} already exists"
        self.adj_list[new_node] = neighbours.copy()
        self.num_nodes += 1
        for neighbour, cost in neighbours.items():
            if neighbour not in self.adj_list:
                self.adj_list[neighbour] = {}
            if new_node not in self.adj_list[neighbour]:
                self.adj_list[neighbour][new_node] = cost
        return f"{new_node} added to the graph."

    def remove_node(self, target_node: str) -> str:
        for node in self.adj_list:
            if target_node in self.adj_list[node]:
                del self.adj_list[node][target_node]
        presence: dict[str, int] | bool = self.adj_list.pop(target_node, False)
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

    def add_edge(self, start: str, end: str, cost = 0) -> str:
        edge_presence: str = self.check_edge(start, end)
        if edge_presence != "":
            return edge_presence
        
        edge_exists = end in self.adj_list[start] or start in self.adj_list[end]
        
        self.adj_list[end][start] = cost
        self.adj_list[start][end] = cost
        
        if edge_exists:
            return f"Edge between {start} and {end} updated with cost {cost}"
        else:
            return f"Edge added between {start} and {end} with cost {cost}"

    def remove_edge(self, start: str, end: str) -> str:
        edge_presence: str = self.check_edge(start, end)
        if edge_presence != "":
            return edge_presence
        if start in self.adj_list[end]:
            del self.adj_list[end][start]
        if end in self.adj_list[start]:
            del self.adj_list[start][end]
        return f"Edge between {start} and {end} removed."

    def display_node(self, node: str) -> str:
        if node not in self.adj_list.keys():
            return f"{node} doesn't exist"
        if not self.adj_list[node]:
            return f"{node} doesn't have any neighbours"
        path: str = f'{node} '
        neighbours: list[str] = list(self.adj_list[node].keys())
        first: bool = True
        for neighbour in neighbours:
            cost = self.adj_list[node][neighbour]
            path += f' -> {neighbour}({cost})' if first else f' , {neighbour}({cost})'
            first = False
        return path + '\n'

    def display_graph(self) -> str | None:
        if len(self.adj_list) == 0:
            return "No nodes to display"
        
        weighted_edges: list[tuple] = []
        isolated_nodes: list[str] = []
        
        for node, neighbours in self.adj_list.items():
            if not neighbours:
                isolated_nodes.append(node)
            else:
                for neighbour, cost in neighbours.items():
                    edge = tuple(sorted((node, neighbour)))
                    edge_with_weight = (edge[0], edge[1], cost)
                    if edge_with_weight not in weighted_edges:
                        weighted_edges.append(edge_with_weight)
        
        if weighted_edges:
            G = nx.Graph()
            for node1, node2, weight in weighted_edges:
                G.add_edge(node1, node2)
            
            print("Graph structure:")
            print(graph_to_ascii(G))
            
            print("\nEdge weights:")
            for edge in weighted_edges:
                node1, node2, weight = edge
                print(f"  {node1} ←--({weight})--→ {node2}")
        
        if isolated_nodes:
            if weighted_edges:
                print("\nIsolated nodes:")
            else:
                print("Isolated nodes:")
            for node in isolated_nodes:
                name_width = max(len(node), 3) 
                border = "─" * name_width
                print(f"┌─{border}─┐")
                print(f"│ {node:^{name_width}} │")
                print(f"└─{border}─┘")
                print()

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
            for node in self.adj_list[curr_node].keys():
                if node not in fringe and node not in explored:
                    fringe.append(node)
        return f"{target} can't be reached"

    def dfs_helper(self, curr_node: str, explored: list[str], target: str,path: list[str] | None = None, trace: list[list[str]] = []) -> bool:
        if path is None:
            path = []
        path.append(curr_node)
        trace.append([str(path), str(explored)])
        if curr_node == target:
            return True
        for node in self.adj_list[curr_node].keys():
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
    
    def ucs(self, start: str, target: str) -> str:
        if start not in self.adj_list:
            return f"Start node {start} doesn't exist"
        if target not in self.adj_list:
            return f"Target node {target} doesn't exist"
        priority_queue: list[tuple[int, str, list[str]]] = [(0, start, [start])]
        explored: set[str] = set()
        trace: list[list[str]] = []
        
        print(f"UCS for target {target}")
        
        while priority_queue:
            current_cost, current_node, path = priority_queue.pop(0)
            queue_display = [f"{node}({cost})" for cost, node, _ in priority_queue]
            trace.append([str(queue_display), str(list(explored))])
            if current_node in explored:
                continue
            explored.add(current_node)
            if current_node == target:
                print(tabulate(trace, headers=["Priority Queue", "Explored"], tablefmt="fancy_grid"))
                return f"Path: {' -> '.join(path)}, Total cost: {current_cost}"
            for neighbor, edge_cost in self.adj_list[current_node].items():
                if neighbor not in explored:
                    new_cost = current_cost + edge_cost
                    new_path = path + [neighbor]
                    new_entry = (new_cost, neighbor, new_path)
                    self._insert_sorted(priority_queue, new_entry)
        
        print(tabulate(trace, headers=["Priority Queue", "Explored"], tablefmt="fancy_grid"))
        return f"{target} is unreachable"
    
    def _insert_sorted(self, queue: list[tuple[int, str, list[str]]], item: tuple[int, str, list[str]]) -> None:
        if not queue:
            queue.append(item)
            return
        left, right = 0, len(queue)
        target_cost = item[0]
        while left < right:
            mid = (left + right) // 2
            if queue[mid][0] <= target_cost:
                left = mid + 1
            else:
                right = mid
        queue.insert(left, item)
        
    def to_dict(self) -> dict[str, dict[str, int]]:
        return self.adj_list

    def from_dict(self, data: dict[str, dict[str, int]]) -> None:
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