import unittest
import tempfile
import os
import json
from src.graph_ops.graph import Graph


class TestGraph(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.graph = Graph()
        
    def test_init(self):
        """Test graph initialization."""
        self.assertEqual(self.graph.adj_list, {})
        self.assertEqual(self.graph.num_nodes, 0)
    
    def test_add_node_basic(self):
        """Test adding a basic node."""
        result = self.graph.add_node("A")
        self.assertEqual(result, "A added to the graph.")
        self.assertIn("A", self.graph.adj_list)
        self.assertEqual(self.graph.num_nodes, 1)
        self.assertEqual(self.graph.adj_list["A"], {})
    
    def test_add_node_duplicate(self):
        """Test adding a duplicate node."""
        self.graph.add_node("A")
        result = self.graph.add_node("A")
        self.assertEqual(result, "A already exists")
        self.assertEqual(self.graph.num_nodes, 1)
    
    def test_add_node_with_neighbours(self):
        """Test adding a node with initial neighbours."""
        self.graph.add_node("A")
        result = self.graph.add_node("B", {"A": 5})
        self.assertEqual(result, "B added to the graph.")
        self.assertEqual(self.graph.adj_list["B"]["A"], 5)
        self.assertEqual(self.graph.adj_list["A"]["B"], 5)
        self.assertEqual(self.graph.num_nodes, 2)
    
    def test_remove_node_basic(self):
        """Test removing a basic node."""
        self.graph.add_node("A")
        result = self.graph.remove_node("A")
        self.assertEqual(result, "A removed from the graph")
        self.assertNotIn("A", self.graph.adj_list)
        self.assertEqual(self.graph.num_nodes, 0)
    
    def test_remove_node_nonexistent(self):
        """Test removing a non-existent node."""
        result = self.graph.remove_node("Z")
        self.assertEqual(result, "Node Z not found.")
        self.assertEqual(self.graph.num_nodes, 0)
    
    def test_remove_node_with_edges(self):
        """Test removing a node that has edges."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_edge("A", "B", 3)
        self.graph.add_edge("B", "C", 2)
        
        result = self.graph.remove_node("B")
        self.assertEqual(result, "B removed from the graph")
        self.assertNotIn("B", self.graph.adj_list)
        self.assertNotIn("B", self.graph.adj_list["A"])
        self.assertNotIn("B", self.graph.adj_list["C"])
        self.assertEqual(self.graph.num_nodes, 2)
    
    def test_check_edge_valid(self):
        """Test check_edge with valid nodes."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        result = self.graph.check_edge("A", "B")
        self.assertEqual(result, "")
    
    def test_check_edge_same_node(self):
        """Test check_edge with same start and end node."""
        self.graph.add_node("A")
        result = self.graph.check_edge("A", "A")
        self.assertEqual(result, "Start node is same as end node: A")
    
    def test_check_edge_nonexistent_start(self):
        """Test check_edge with non-existent start node."""
        self.graph.add_node("B")
        result = self.graph.check_edge("X", "B")
        self.assertEqual(result, "X doesn't exist")
    
    def test_check_edge_nonexistent_end(self):
        """Test check_edge with non-existent end node."""
        self.graph.add_node("A")
        result = self.graph.check_edge("A", "Y")
        self.assertEqual(result, "Y doesn't exist")
    
    def test_add_edge_basic(self):
        """Test adding a basic edge."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        result = self.graph.add_edge("A", "B", 5)
        self.assertEqual(result, "Edge added between A and B with cost 5")
        self.assertEqual(self.graph.adj_list["A"]["B"], 5)
        self.assertEqual(self.graph.adj_list["B"]["A"], 5)
    
    def test_add_edge_default_cost(self):
        """Test adding an edge with default cost."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        result = self.graph.add_edge("A", "B")
        self.assertEqual(result, "Edge added between A and B with cost 0")
        self.assertEqual(self.graph.adj_list["A"]["B"], 0)
    
    def test_add_edge_update_existing(self):
        """Test updating an existing edge."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B", 3)
        result = self.graph.add_edge("A", "B", 7)
        self.assertEqual(result, "Edge between A and B updated with cost 7")
        self.assertEqual(self.graph.adj_list["A"]["B"], 7)
        self.assertEqual(self.graph.adj_list["B"]["A"], 7)
    
    def test_add_edge_invalid_nodes(self):
        """Test adding edge with invalid nodes."""
        self.graph.add_node("A")
        result = self.graph.add_edge("A", "Z", 5)
        self.assertEqual(result, "Z doesn't exist")
    
    def test_remove_edge_basic(self):
        """Test removing a basic edge."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B", 5)
        result = self.graph.remove_edge("A", "B")
        self.assertEqual(result, "Edge between A and B removed.")
        self.assertNotIn("B", self.graph.adj_list["A"])
        self.assertNotIn("A", self.graph.adj_list["B"])
    
    def test_remove_edge_nonexistent(self):
        """Test removing a non-existent edge."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        result = self.graph.remove_edge("A", "B")
        self.assertEqual(result, "Edge between A and B removed.")
    
    def test_display_node_basic(self):
        """Test displaying a node with neighbours."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_edge("A", "B", 3)
        self.graph.add_edge("A", "C", 5)
        result = self.graph.display_node("A")
        self.assertIn("A", result)
        self.assertIn("B(3)", result)
        self.assertIn("C(5)", result)
    
    def test_display_node_no_neighbours(self):
        """Test displaying a node with no neighbours."""
        self.graph.add_node("A")
        result = self.graph.display_node("A")
        self.assertEqual(result, "A doesn't have any neighbours")
    
    def test_display_node_nonexistent(self):
        """Test displaying a non-existent node."""
        result = self.graph.display_node("Z")
        self.assertEqual(result, "Z doesn't exist")
    
    def test_display_graph_empty(self):
        """Test displaying an empty graph."""
        result = self.graph.display_graph()
        self.assertEqual(result, "No nodes to display")
    
    def test_to_dict_and_from_dict(self):
        """Test graph serialization and deserialization."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B", 5)
        
        data = self.graph.to_dict()
        expected = {"A": {"B": 5}, "B": {"A": 5}}
        self.assertEqual(data, expected)
        
        new_graph = Graph()
        new_graph.from_dict(data)
        self.assertEqual(new_graph.adj_list, self.graph.adj_list)
        self.assertEqual(new_graph.num_nodes, self.graph.num_nodes)
    
    def test_save_and_load(self):
        """Test saving and loading graph to/from file."""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name
        
        # Monkey patch the filename for this test
        import src.graph_ops.graph as graph_module
        original_filename = graph_module.FILENAME
        
        try:
            graph_module.FILENAME = temp_filename
            
            # Create and save graph
            self.graph.add_node("A")
            self.graph.add_node("B")
            self.graph.add_edge("A", "B", 10)
            self.graph.save()
            
            # Load into new graph
            new_graph = Graph()
            new_graph.load()
            
            self.assertEqual(new_graph.adj_list, self.graph.adj_list)
            self.assertEqual(new_graph.num_nodes, self.graph.num_nodes)
            
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            # Restore original filename
            graph_module.FILENAME = original_filename


class TestGraphSearchAlgorithms(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.graph = Graph()
        # Create a test graph
        #     A --- 1 --- B
        #     |           |
        #     4           2
        #     |           |
        #     C --- 1 --- D
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        self.graph.add_edge("A", "B", 1)
        self.graph.add_edge("A", "C", 4)
        self.graph.add_edge("B", "D", 2)
        self.graph.add_edge("C", "D", 1)
    
    def test_bfs_found_path(self):
        """Test BFS finding a path."""
        result = self.graph.bfs("A", "D")
        # BFS should find A -> B -> D (ignores weights)
        self.assertIn("A", result)
        self.assertIn("D", result)
        self.assertNotEqual(result, "D can't be reached")
    
    def test_bfs_unreachable(self):
        """Test BFS with unreachable target."""
        self.graph.add_node("E")  # Isolated node
        result = self.graph.bfs("A", "E")
        self.assertEqual(result, "E can't be reached")
    
    def test_dfs_found_path(self):
        """Test DFS finding a path."""
        result = self.graph.dfs("A", "D")
        self.assertIn("A", result)
        self.assertIn("D", result)
        self.assertNotEqual(result, "D is unreachable")
    
    def test_dfs_unreachable(self):
        """Test DFS with unreachable target."""
        self.graph.add_node("E")  # Isolated node
        result = self.graph.dfs("A", "E")
        self.assertEqual(result, "E is unreachable")
    
    def test_ucs_found_optimal_path(self):
        """Test UCS finding optimal path."""
        result = self.graph.ucs("A", "D")
        # UCS should find A -> B -> D (cost 3) over A -> C -> D (cost 5)
        self.assertIn("Path: A -> B -> D", result)
        self.assertIn("Total cost: 3", result)
    
    def test_ucs_unreachable(self):
        """Test UCS with unreachable target."""
        self.graph.add_node("E")  # Isolated node
        result = self.graph.ucs("A", "E")
        self.assertEqual(result, "E is unreachable")
    
    def test_ucs_nonexistent_start(self):
        """Test UCS with non-existent start node."""
        result = self.graph.ucs("Z", "A")
        self.assertEqual(result, "Start node Z doesn't exist")
    
    def test_ucs_nonexistent_target(self):
        """Test UCS with non-existent target node."""
        result = self.graph.ucs("A", "Z")
        self.assertEqual(result, "Target node Z doesn't exist")
    
    def test_ucs_same_start_target(self):
        """Test UCS with same start and target."""
        result = self.graph.ucs("A", "A")
        self.assertIn("Path: A", result)
        self.assertIn("Total cost: 0", result)


class TestGraphComplexScenarios(unittest.TestCase):
    
    def test_large_graph_operations(self):
        """Test operations on a larger graph."""
        graph = Graph()
        
        # Create nodes A through J
        nodes = [chr(ord('A') + i) for i in range(10)]
        for node in nodes:
            graph.add_node(node)
        
        # Add some edges
        edges = [
            ("A", "B", 2), ("B", "C", 3), ("C", "D", 1),
            ("D", "E", 4), ("E", "F", 2), ("F", "G", 3),
            ("G", "H", 1), ("H", "I", 2), ("I", "J", 1),
            ("A", "J", 20)  # Expensive direct path
        ]
        
        for start, end, cost in edges:
            graph.add_edge(start, end, cost)
        
        self.assertEqual(graph.num_nodes, 10)
        
        # Test UCS finds optimal path from A to J
        result = graph.ucs("A", "J")
        # Should find path through the chain rather than direct expensive edge
        self.assertIn("Total cost:", result)
        cost_part = result.split("Total cost: ")[1]
        cost = int(cost_part)
        self.assertLess(cost, 20)  # Should be less than direct path
    
    def test_disconnected_graph(self):
        """Test operations on disconnected graph components."""
        graph = Graph()
        
        # Component 1: A - B - C
        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C")
        graph.add_edge("A", "B", 1)
        graph.add_edge("B", "C", 1)
        
        # Component 2: X - Y - Z
        graph.add_node("X")
        graph.add_node("Y")
        graph.add_node("Z")
        graph.add_edge("X", "Y", 2)
        graph.add_edge("Y", "Z", 2)
        
        # Test search within component
        result = graph.ucs("A", "C")
        self.assertIn("Path: A -> B -> C", result)
        
        # Test search across components (should fail)
        result = graph.ucs("A", "Z")
        self.assertEqual(result, "Z is unreachable")
    
    def test_zero_weight_edges(self):
        """Test graph with zero-weight edges."""
        graph = Graph()
        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C")
        
        graph.add_edge("A", "B", 0)
        graph.add_edge("B", "C", 0)
        
        result = graph.ucs("A", "C")
        self.assertIn("Total cost: 0", result)
    
    def test_negative_and_high_weight_edges(self):
        """Test graph with various edge weights."""
        graph = Graph()
        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C")
        
        # Test with high cost
        graph.add_edge("A", "B", 1000)
        graph.add_edge("A", "C", 1)
        graph.add_edge("C", "B", 1)
        
        result = graph.ucs("A", "B")
        self.assertIn("Path: A -> C -> B", result)
        self.assertIn("Total cost: 2", result)
    
    def test_multiple_optimal_paths(self):
        """Test graph with multiple optimal paths."""
        graph = Graph()
        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C")
        graph.add_node("D")
        
        # Two paths with same cost: A-B-D and A-C-D
        graph.add_edge("A", "B", 2)
        graph.add_edge("A", "C", 2)
        graph.add_edge("B", "D", 1)
        graph.add_edge("C", "D", 1)
        
        result = graph.ucs("A", "D")
        self.assertIn("Total cost: 3", result)
        # Should find one of the optimal paths
        self.assertTrue("A -> B -> D" in result or "A -> C -> D" in result)


class TestGraphEdgeCases(unittest.TestCase):
    
    def test_single_node_graph(self):
        """Test operations on single node graph."""
        graph = Graph()
        graph.add_node("A")
        
        # Test search on single node
        result = graph.ucs("A", "A")
        self.assertIn("Path: A", result)
        self.assertIn("Total cost: 0", result)
    
    def test_empty_graph_operations(self):
        """Test operations on empty graph."""
        graph = Graph()
        
        result = graph.ucs("A", "B")
        self.assertEqual(result, "Start node A doesn't exist")
        
        result = graph.bfs("A", "B")
        self.assertEqual(result, "B can't be reached")
    
    def test_graph_after_node_removal(self):
        """Test graph consistency after node removal."""
        graph = Graph()
        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C")
        graph.add_edge("A", "B", 1)
        graph.add_edge("B", "C", 1)
        
        # Remove middle node
        graph.remove_node("B")
        
        # A and C should now be disconnected
        result = graph.ucs("A", "C")
        self.assertEqual(result, "C is unreachable")
    
    def test_graph_with_self_loops_prevention(self):
        """Test that self-loops are prevented."""
        graph = Graph()
        graph.add_node("A")
        
        result = graph.add_edge("A", "A", 5)
        self.assertEqual(result, "Start node is same as end node: A")


if __name__ == '__main__':
    unittest.main()
