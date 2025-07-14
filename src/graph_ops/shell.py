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
        'Add an edge: add_edge NODE1 NODE2'
        try:
            node1, node2 = arg.split()
            print(self.graph.add_edge(node1, node2))
        except ValueError:
            print("Usage: add_edge NODE1 NODE2")

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

    def do_exit(self, arg: str) -> bool:
        'Exit the shell'
        self.graph.save()
        print("Graph saved.")
        return True

    def do_EOF(self, arg: str) -> bool:
        'Exit with Ctrl-D'
        return self.do_exit(arg)


def shell():
    GraphShell().cmdloop()

if __name__ == "__main__":
    shell()