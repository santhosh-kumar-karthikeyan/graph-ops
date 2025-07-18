import unittest
import time
import random
from src.graph_ops.graph import Graph


class TestGraphPerformance(unittest.TestCase):
    """Performance tests for graph operations."""
    
    def test_large_graph_creation(self):
        """Test creating a large graph."""
        start_time = time.time()
        
        graph = Graph()
        num_nodes = 1000
        
        # Add nodes
        for i in range(num_nodes):
            graph.add_node(f"N{i}")
        
        # Add edges (sparse graph)
        for i in range(num_nodes - 1):
            graph.add_edge(f"N{i}", f"N{i+1}", random.randint(1, 10))
        
        creation_time = time.time() - start_time
        self.assertEqual(graph.num_nodes, num_nodes)
        self.assertLess(creation_time, 5.0)  # Should complete within 5 seconds
    
    def test_ucs_performance_large_graph(self):
        """Test UCS performance on larger graph."""
        graph = Graph()
        
        # Create a grid-like graph
        size = 20  # 20x20 grid = 400 nodes
        
        # Add nodes
        for i in range(size):
            for j in range(size):
                graph.add_node(f"{i},{j}")
        
        # Add edges (connect adjacent nodes)
        for i in range(size):
            for j in range(size):
                current = f"{i},{j}"
                # Connect to right neighbor
                if j < size - 1:
                    right = f"{i},{j+1}"
                    graph.add_edge(current, right, 1)
                # Connect to bottom neighbor
                if i < size - 1:
                    bottom = f"{i+1},{j}"
                    graph.add_edge(current, bottom, 1)
        
        # Test UCS from corner to corner
        start_time = time.time()
        result = graph.ucs("0,0", f"{size-1},{size-1}")
        ucs_time = time.time() - start_time
        
        self.assertIn("Path:", result)
        self.assertIn(f"Total cost: {2 * (size - 1)}", result)  # Manhattan distance
        self.assertLess(ucs_time, 10.0)  # Should complete within 10 seconds
    
    def test_binary_search_insertion_performance(self):
        """Test performance of binary search insertion in priority queue."""
        graph = Graph()
        
        # Create a large priority queue scenario
        queue = []
        
        start_time = time.time()
        
        # Insert many items (worst case: reverse sorted)
        for i in range(1000, 0, -1):
            item = (i, f"N{i}", [f"N{i}"])
            graph._insert_sorted(queue, item)
        
        insertion_time = time.time() - start_time
        
        # Verify queue is sorted
        costs = [item[0] for item in queue]
        self.assertEqual(costs, sorted(costs))
        self.assertLess(insertion_time, 1.0)  # Should complete within 1 second
    
    def test_memory_usage_large_graph(self):
        """Test memory efficiency with large graphs."""
        import sys
        
        graph = Graph()
        
        # Measure memory before
        initial_size = sys.getsizeof(graph.adj_list)
        
        # Add many nodes and edges
        num_nodes = 500
        for i in range(num_nodes):
            graph.add_node(f"N{i}")
        
        # Add edges in a ring
        for i in range(num_nodes):
            next_node = (i + 1) % num_nodes
            graph.add_edge(f"N{i}", f"N{next_node}", 1)
        
        final_size = sys.getsizeof(graph.adj_list)
        
        # Memory should scale reasonably
        self.assertLess(final_size, initial_size + num_nodes * 1000)  # Rough bound
        self.assertEqual(graph.num_nodes, num_nodes)


class TestGraphStressTests(unittest.TestCase):
    """Stress tests for edge cases and robustness."""
    
    def test_many_isolated_nodes(self):
        """Test graph with many isolated nodes."""
        graph = Graph()
        
        num_isolated = 1000
        for i in range(num_isolated):
            graph.add_node(f"ISOLATED_{i}")
        
        self.assertEqual(graph.num_nodes, num_isolated)
        
        # Display should handle this gracefully
        result = graph.display_graph()
        # Should not crash or hang
        self.assertIsNone(result)  # display_graph prints, returns None
    
    def test_deeply_connected_graph(self):
        """Test graph where every node connects to every other node."""
        graph = Graph()
        
        num_nodes = 50  # Keep reasonable for test speed
        nodes = [f"N{i}" for i in range(num_nodes)]
        
        # Add all nodes
        for node in nodes:
            graph.add_node(node)
        
        # Connect every node to every other node
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if i < j:  # Avoid duplicates and self-loops
                    graph.add_edge(node1, node2, random.randint(1, 100))
        
        # Test UCS on fully connected graph
        result = graph.ucs("N0", f"N{num_nodes-1}")
        self.assertIn("Path:", result)
        self.assertIn("Total cost:", result)
    
    def test_linear_chain_graph(self):
        """Test very long linear chain of nodes."""
        graph = Graph()
        
        chain_length = 500
        
        # Create linear chain: N0 -> N1 -> N2 -> ... -> N499
        for i in range(chain_length):
            graph.add_node(f"N{i}")
        
        for i in range(chain_length - 1):
            graph.add_edge(f"N{i}", f"N{i+1}", 1)
        
        # Test UCS from start to end
        result = graph.ucs("N0", f"N{chain_length-1}")
        self.assertIn(f"Total cost: {chain_length-1}", result)
    
    def test_random_graph_operations(self):
        """Test random sequence of graph operations."""
        graph = Graph()
        
        # Perform random operations
        for _ in range(1000):
            operation = random.choice(['add_node', 'add_edge', 'remove_node', 'remove_edge'])
            
            try:
                if operation == 'add_node':
                    node_id = f"N{random.randint(0, 100)}"
                    graph.add_node(node_id)
                
                elif operation == 'add_edge' and graph.num_nodes >= 2:
                    nodes = list(graph.adj_list.keys())
                    if len(nodes) >= 2:
                        node1, node2 = random.sample(nodes, 2)
                        cost = random.randint(1, 10)
                        graph.add_edge(node1, node2, cost)
                
                elif operation == 'remove_node' and graph.num_nodes > 0:
                    nodes = list(graph.adj_list.keys())
                    node = random.choice(nodes)
                    graph.remove_node(node)
                
                elif operation == 'remove_edge' and graph.num_nodes >= 2:
                    nodes = list(graph.adj_list.keys())
                    if len(nodes) >= 2:
                        node1, node2 = random.sample(nodes, 2)
                        graph.remove_edge(node1, node2)
                
            except Exception as e:
                # Should not crash on valid operations
                self.fail(f"Operation {operation} caused exception: {e}")
        
        # Graph should remain in valid state
        self.assertGreaterEqual(graph.num_nodes, 0)
        self.assertEqual(len(graph.adj_list), graph.num_nodes)


class TestGraphDataIntegrity(unittest.TestCase):
    """Tests for data integrity and consistency."""
    
    def test_bidirectional_edge_consistency(self):
        """Test that edges remain bidirectional after operations."""
        graph = Graph()
        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C")
        
        # Add edges
        graph.add_edge("A", "B", 5)
        graph.add_edge("B", "C", 3)
        
        # Check bidirectionality
        self.assertEqual(graph.adj_list["A"]["B"], graph.adj_list["B"]["A"])
        self.assertEqual(graph.adj_list["B"]["C"], graph.adj_list["C"]["B"])
        
        # Update edge and check consistency
        graph.add_edge("A", "B", 7)
        self.assertEqual(graph.adj_list["A"]["B"], 7)
        self.assertEqual(graph.adj_list["B"]["A"], 7)
        
        # Remove edge and check consistency
        graph.remove_edge("A", "B")
        self.assertNotIn("B", graph.adj_list["A"])
        self.assertNotIn("A", graph.adj_list["B"])
    
    def test_node_removal_edge_cleanup(self):
        """Test that removing nodes properly cleans up edges."""
        graph = Graph()
        
        # Create a star graph: center connected to all others
        graph.add_node("CENTER")
        for i in range(5):
            node = f"OUTER_{i}"
            graph.add_node(node)
            graph.add_edge("CENTER", node, i + 1)
        
        # Remove center node
        graph.remove_node("CENTER")
        
        # Check that all outer nodes have no edges to CENTER
        for i in range(5):
            node = f"OUTER_{i}"
            self.assertNotIn("CENTER", graph.adj_list[node])
            self.assertEqual(len(graph.adj_list[node]), 0)
    
    def test_serialization_roundtrip_integrity(self):
        """Test that save/load preserves graph structure exactly."""
        import tempfile
        import os
        
        graph = Graph()
        
        # Create complex graph
        nodes = ["A", "B", "C", "D", "E"]
        for node in nodes:
            graph.add_node(node)
        
        edges = [("A", "B", 3), ("B", "C", 5), ("C", "D", 2), ("D", "E", 4), ("E", "A", 1)]
        for start, end, cost in edges:
            graph.add_edge(start, end, cost)
        
        # Save original state
        original_adj_list = graph.adj_list.copy()
        original_num_nodes = graph.num_nodes
        
        # Save and load
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name
        
        import src.graph_ops.graph as graph_module
        original_filename = graph_module.FILENAME
        
        try:
            graph_module.FILENAME = temp_filename
            
            graph.save()
            
            new_graph = Graph()
            new_graph.load()
            
            # Check integrity
            self.assertEqual(new_graph.adj_list, original_adj_list)
            self.assertEqual(new_graph.num_nodes, original_num_nodes)
            
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            graph_module.FILENAME = original_filename


if __name__ == '__main__':
    unittest.main()
