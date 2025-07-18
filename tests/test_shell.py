import unittest
import io
import sys
from unittest.mock import patch, MagicMock
from src.graph_ops.shell import GraphShell
from src.graph_ops.graph import Graph


class TestGraphShell(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.shell = GraphShell()
        # Clear any existing graph data
        self.shell.graph = Graph()
    
    def capture_output(self, method, *args):
        """Helper method to capture print output from shell commands."""
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            method(*args)
            output = buffer.getvalue()
        finally:
            sys.stdout = old_stdout
        return output
    
    def test_do_add_node(self):
        """Test add_node shell command."""
        output = self.capture_output(self.shell.do_add_node, "TestNode")
        self.assertIn("TestNode added to the graph", output)
        self.assertIn("TestNode", self.shell.graph.adj_list)
    
    def test_do_add_node_empty_arg(self):
        """Test add_node shell command with empty argument."""
        output = self.capture_output(self.shell.do_add_node, "")
        self.assertIn("Usage: add_node NODE", output)
    
    def test_do_add_node_duplicate(self):
        """Test add_node shell command with duplicate node."""
        self.shell.do_add_node("TestNode")
        output = self.capture_output(self.shell.do_add_node, "TestNode")
        self.assertIn("TestNode already exists", output)
    
    def test_do_remove_node(self):
        """Test remove_node shell command."""
        self.shell.do_add_node("TestNode")
        output = self.capture_output(self.shell.do_remove_node, "TestNode")
        self.assertIn("TestNode removed from the graph", output)
        self.assertNotIn("TestNode", self.shell.graph.adj_list)
    
    def test_do_remove_node_empty_arg(self):
        """Test remove_node shell command with empty argument."""
        output = self.capture_output(self.shell.do_remove_node, "")
        self.assertIn("Usage: remove_node NODE", output)
    
    def test_do_remove_node_nonexistent(self):
        """Test remove_node shell command with non-existent node."""
        output = self.capture_output(self.shell.do_remove_node, "NonExistent")
        self.assertIn("Node NonExistent not found", output)
    
    def test_do_add_edge_basic(self):
        """Test add_edge shell command."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        output = self.capture_output(self.shell.do_add_edge, "A B")
        self.assertIn("Edge added between A and B with cost 0", output)
        self.assertEqual(self.shell.graph.adj_list["A"]["B"], 0)
    
    def test_do_add_edge_with_cost(self):
        """Test add_edge shell command with cost."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        output = self.capture_output(self.shell.do_add_edge, "A B 5")
        self.assertIn("Edge added between A and B with cost 5", output)
        self.assertEqual(self.shell.graph.adj_list["A"]["B"], 5)
    
    def test_do_add_edge_invalid_cost(self):
        """Test add_edge shell command with invalid cost."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        output = self.capture_output(self.shell.do_add_edge, "A B invalid")
        self.assertIn("Cost must be an integer", output)
    
    def test_do_add_edge_invalid_args(self):
        """Test add_edge shell command with invalid arguments."""
        output = self.capture_output(self.shell.do_add_edge, "A")
        self.assertIn("Usage: add_edge NODE1 NODE2 [COST]", output)
        
        output = self.capture_output(self.shell.do_add_edge, "A B C D")
        self.assertIn("Usage: add_edge NODE1 NODE2 [COST]", output)
    
    def test_do_remove_edge(self):
        """Test remove_edge shell command."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        self.shell.do_add_edge("A B 5")
        output = self.capture_output(self.shell.do_remove_edge, "A B")
        self.assertIn("Edge between A and B removed", output)
        self.assertNotIn("B", self.shell.graph.adj_list["A"])
    
    def test_do_remove_edge_invalid_args(self):
        """Test remove_edge shell command with invalid arguments."""
        output = self.capture_output(self.shell.do_remove_edge, "A")
        self.assertIn("Usage: remove_edge NODE1 NODE2", output)
    
    def test_do_display_graph(self):
        """Test display shell command for entire graph."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        self.shell.do_add_edge("A B 3")
        
        # Test displaying entire graph
        output = self.capture_output(self.shell.do_display, "")
        self.assertIn("Graph structure", output)
        self.assertIn("Edge weights", output)
    
    def test_do_display_node(self):
        """Test display shell command for specific node."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        self.shell.do_add_edge("A B 3")
        
        # Test displaying specific node
        output = self.capture_output(self.shell.do_display, "A")
        self.assertIn("A", output)
        self.assertIn("B(3)", output)
    
    def test_do_display_empty_graph(self):
        """Test display shell command on empty graph."""
        output = self.capture_output(self.shell.do_display, "")
        self.assertIn("No nodes to display", output)
    
    def test_do_bfs(self):
        """Test BFS shell command."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        self.shell.do_add_node("C")
        self.shell.do_add_edge("A B")
        self.shell.do_add_edge("B C")
        
        output = self.capture_output(self.shell.do_bfs, "A C")
        self.assertIn("BFS for target C", output)
        self.assertIn("A -> B -> C", output)
    
    def test_do_bfs_invalid_args(self):
        """Test BFS shell command with invalid arguments."""
        output = self.capture_output(self.shell.do_bfs, "A")
        self.assertIn("Usage: bfs start target", output)
    
    def test_do_dfs(self):
        """Test DFS shell command."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        self.shell.do_add_node("C")
        self.shell.do_add_edge("A B")
        self.shell.do_add_edge("B C")
        
        output = self.capture_output(self.shell.do_dfs, "A C")
        self.assertIn("A", output)
        self.assertIn("C", output)
    
    def test_do_dfs_invalid_args(self):
        """Test DFS shell command with invalid arguments."""
        output = self.capture_output(self.shell.do_dfs, "A")
        self.assertIn("Usage: dfs start target", output)
    
    def test_do_ucs(self):
        """Test UCS shell command."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        self.shell.do_add_node("C")
        self.shell.do_add_edge("A B 1")
        self.shell.do_add_edge("B C 1")
        self.shell.do_add_edge("A C 5")
        
        output = self.capture_output(self.shell.do_ucs, "A C")
        self.assertIn("UCS for target C", output)
        self.assertIn("Path: A -> B -> C", output)
        self.assertIn("Total cost: 2", output)
    
    def test_do_ucs_invalid_args(self):
        """Test UCS shell command with invalid arguments."""
        output = self.capture_output(self.shell.do_ucs, "A")
        self.assertIn("Usage: ucs start target", output)
    
    @patch('src.graph_ops.graph.Graph.save')
    def test_do_save(self, mock_save):
        """Test save shell command."""
        output = self.capture_output(self.shell.do_save, "")
        self.assertIn("Graph saved", output)
        mock_save.assert_called_once()
    
    @patch('src.graph_ops.graph.Graph.load')
    def test_do_load(self, mock_load):
        """Test load shell command."""
        output = self.capture_output(self.shell.do_load, "")
        self.assertIn("Graph loaded", output)
        mock_load.assert_called_once()
    
    @patch('src.graph_ops.graph.Graph.save')
    def test_do_exit(self, mock_save):
        """Test exit shell command."""
        result = self.shell.do_exit("")
        self.assertTrue(result)  # Should return True to exit
        mock_save.assert_called_once()


class TestGraphShellIntegration(unittest.TestCase):
    """Integration tests for shell functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.shell = GraphShell()
        self.shell.graph = Graph()
    
    def capture_output(self, method, *args):
        """Helper method to capture print output from shell commands."""
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            method(*args)
            output = buffer.getvalue()
        finally:
            sys.stdout = old_stdout
        return output
    
    def test_complex_graph_operations(self):
        """Test complex sequence of graph operations."""
        # Build a graph through shell commands
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        self.shell.do_add_node("C")
        self.shell.do_add_node("D")
        
        self.shell.do_add_edge("A B 2")
        self.shell.do_add_edge("A C 5")
        self.shell.do_add_edge("B C 1")
        self.shell.do_add_edge("B D 3")
        self.shell.do_add_edge("C D 1")
        
        # Test that UCS finds optimal path
        output = self.capture_output(self.shell.do_ucs, "A D")
        self.assertIn("Path: A -> B -> C -> D", output)
        self.assertIn("Total cost: 4", output)
        
        # Remove a node and test connectivity
        self.shell.do_remove_node("B")
        output = self.capture_output(self.shell.do_ucs, "A D")
        self.assertIn("Path: A -> C -> D", output)
        self.assertIn("Total cost: 6", output)
    
    def test_search_algorithm_comparison(self):
        """Test different search algorithms on same graph."""
        # Create a graph where algorithms might differ
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        self.shell.do_add_node("C")
        self.shell.do_add_edge("A B 10")  # Expensive direct path
        self.shell.do_add_edge("A C 1")   # Cheap intermediate
        self.shell.do_add_edge("C B 1")   # Cheap intermediate
        
        # BFS (ignores weights) vs UCS (considers weights)
        bfs_output = self.capture_output(self.shell.do_bfs, "A B")
        ucs_output = self.capture_output(self.shell.do_ucs, "A B")
        
        # BFS should find direct path A -> B
        self.assertIn("A -> B", bfs_output)
        
        # UCS should find optimal path A -> C -> B
        self.assertIn("A -> C -> B", ucs_output)
        self.assertIn("Total cost: 2", ucs_output)
    
    def test_isolated_nodes_handling(self):
        """Test handling of isolated nodes."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        self.shell.do_add_node("Isolated")
        self.shell.do_add_edge("A B 1")
        
        # Display should show isolated nodes separately
        output = self.capture_output(self.shell.do_display, "")
        self.assertIn("Isolated nodes", output)
        self.assertIn("Isolated", output)
        
        # Search to isolated node should fail
        output = self.capture_output(self.shell.do_ucs, "A Isolated")
        self.assertIn("unreachable", output)
    
    def test_edge_weight_updates(self):
        """Test updating edge weights through shell."""
        self.shell.do_add_node("A")
        self.shell.do_add_node("B")
        
        # Add edge with cost 5
        output = self.capture_output(self.shell.do_add_edge, "A B 5")
        self.assertIn("added", output)
        
        # Update edge with cost 10
        output = self.capture_output(self.shell.do_add_edge, "A B 10")
        self.assertIn("updated", output)
        
        # Verify the cost was updated
        self.assertEqual(self.shell.graph.adj_list["A"]["B"], 10)
    
    def test_error_handling_sequences(self):
        """Test various error conditions in sequence."""
        # Operations on non-existent nodes
        output = self.capture_output(self.shell.do_remove_node, "NonExistent")
        self.assertIn("not found", output)
        
        output = self.capture_output(self.shell.do_add_edge, "A B")
        self.assertIn("doesn't exist", output)
        
        # Search on empty graph
        output = self.capture_output(self.shell.do_bfs, "A B")
        self.assertIn("can't be reached", output)
        
        # Invalid command arguments
        output = self.capture_output(self.shell.do_add_edge, "A B C D E")
        self.assertIn("Usage:", output)


if __name__ == '__main__':
    unittest.main()
