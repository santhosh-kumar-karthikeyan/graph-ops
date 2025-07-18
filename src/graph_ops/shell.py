import cmd
from .graph import Graph

class GraphShell(cmd.Cmd):
    intro = "Welcome to the Graph shell. Type help or ? to list commands."
    prompt = "(graph)>>"

    def __init__(self) -> None:
        super().__init__()
        self.graph = Graph()
        self.graph.load()

    def do_add_node(self, arg: str) -> None:
        'Add a node: add_node NODE'
        node = arg.strip()
        if node:
            print(self.graph.add_node(node))
        else:
            print("Usage: add_node NODE")

    def do_remove_node(self, arg: str) -> None:
        'Remove a node: remove_node NODE'
        node = arg.strip()
        if node:
            print(self.graph.remove_node(node))
        else:
            print("Usage: remove_node NODE")

    def do_add_edge(self, arg: str) -> None:
        'Add an edge with optional cost: add_edge NODE1 NODE2 [COST] (default cost: 0)'
        parts = arg.split()
        if len(parts) == 2:
            node1, node2 = parts
            print(self.graph.add_edge(node1, node2, 0))
        elif len(parts) == 3:
            node1, node2, cost_str = parts
            try:
                cost = int(cost_str)
                print(self.graph.add_edge(node1, node2, cost))
            except ValueError:
                print("Cost must be an integer")
        else:
            print("Usage: add_edge NODE1 NODE2 [COST] (default cost: 0)")

    def do_remove_edge(self, arg: str) -> None:
        'Remove an edge: remove_edge NODE1 NODE2'
        try:
            node1, node2 = arg.split()
            print(self.graph.remove_edge(node1, node2))
        except ValueError:
            print("Usage: remove_edge NODE1 NODE2")

    def do_display(self, arg: str | None = None) -> None:
        'Display the graph or a node. Usage: display | display node_name'
        if arg is None:
            arg = ""
        if len(arg.split()) == 0:
            result: str | None = self.graph.display_graph()
            if result is not None:
                print(result)
        else:
            node = arg.split()
            print(self.graph.display_node(node[0]))

    def do_save(self, arg: str) -> None:
        'Save the current graph to disk'
        self.graph.save()
        print("Graph saved.")

    def do_load(self, arg: str) -> None:
        'Load the graph from disk'
        self.graph.load()
        print("Graph loaded.")
    def do_bfs(self,arg: str) -> None:
        'Search for target node in Breadth first fashion: bfs start target'
        try:
            start,target = arg.split()
            print(self.graph.bfs(start,target))
        except ValueError:
            print("Usage: bfs start target")
    def do_dfs(self,arg: str) -> None:
        'Search for a target node in Depth first manner: dfs start target'
        try:
            start,target = arg.split()
            print(self.graph.dfs(start,target))
        except ValueError:
            print("Usage: dfs start target")
    
    def do_ucs(self, arg: str) -> None:
        'Search for target node using Uniform Cost Search: ucs start target'
        try:
            start, target = arg.split()
            print(self.graph.ucs(start, target))
        except ValueError:
            print("Usage: ucs start target")
            
    def do_exit(self, arg: str) -> bool:
        'Exit the shell'
        self.graph.save()
        print("Graph saved.")
        return True


def shell():
    GraphShell().cmdloop()

if __name__ == "__main__":
    shell()