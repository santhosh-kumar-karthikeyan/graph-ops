import unittest
from src.graph_ops.graph import Graph


class TestUCSBinarySearch(unittest.TestCase):
    """Detailed tests for UCS algorithm's binary search priority queue implementation."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.graph = Graph()
    
    def test_insert_sorted_empty_queue(self):
        """Test inserting into empty priority queue."""
        queue = []
        item = (5, "A", ["A"])
        self.graph._insert_sorted(queue, item)
        self.assertEqual(queue, [item]
    
    def test_insert_sorted_single_item(self):
        """Test inserting into queue with single item."""
        queue = [(3, "A", ["A"])]
        
        # Insert item with lower cost
        item1 = (1, "B", ["B"])
        self.graph._insert_sorted(queue, item1)
        self.assertEqual(queue[0], item1)
        
        # Insert item with higher cost
        item2 = (7, "C", ["C"])
        self.graph._insert_sorted(queue, item2)
        self.assertEqual(queue[-1], item2)
    
    def test_insert_sorted_multiple_items(self):
        """Test inserting into queue with multiple items."""
        queue = [(1, "A", ["A"]), (3, "B", ["B"]), (7, "C", ["C"])]
        
        # Insert in middle
        item = (5, "D", ["D"])
        self.graph._insert_sorted(queue, item)
        
        # Verify sorted order
        costs = [item[0] for item in queue]
        self.assertEqual(costs, [1, 3, 5, 7])
    
    def test_insert_sorted_duplicate_costs(self):
        """Test inserting items with duplicate costs."""
        queue = [(2, "A", ["A"]), (4, "B", ["B"])]
        
        # Insert item with same cost as existing
        item = (2, "C", ["C"])
        self.graph._insert_sorted(queue, item)
        
        # Should maintain relative order for same costs
        costs = [item[0] for item in queue]
        self.assertEqual(costs, [2, 2, 4])
    
    def test_ucs_priority_queue_ordering(self):
        """Test that UCS processes nodes in correct cost order."""
        # Create graph where order matters
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        
        # A connects to B(cost=5) and C(cost=2)
        # B connects to D(cost=1), C connects to D(cost=10)
        # Optimal path should be A -> C -> B -> D (cost=8) vs A -> B -> D (cost=6)
        self.graph.add_edge("A", "B", 5)
        self.graph.add_edge("A", "C", 2)
        self.graph.add_edge("B", "D", 1)
        self.graph.add_edge("C", "B", 1)
        
        result = self.graph.ucs("A", "D")
        self.assertIn("Path: A -> B -> D", result)
        self.assertIn("Total cost: 6", result)
    
    def test_ucs_with_many_nodes(self):
        """Test UCS with larger graph to stress-test binary search."""
        # Create a larger graph
        nodes = [chr(ord('A') + i) for i in range(8)]  # A through H
        for node in nodes:
            self.graph.add_node(node)
        
        # Create edges with varying costs
        edges = [
            ("A", "B", 3), ("A", "C", 8), ("A", "D", 2),
            ("B", "E", 4), ("C", "F", 1), ("D", "G", 6),
            ("E", "H", 2), ("F", "H", 3), ("G", "H", 1)
        ]
        
        for start, end, cost in edges:
            self.graph.add_edge(start, end, cost)
        
        result = self.graph.ucs("A", "H")
        self.assertIn("Total cost:", result)
        
        # Verify it's a valid path
        self.assertIn("Path:", result)
        self.assertIn("A", result)
        self.assertIn("H", result)
    
    def test_ucs_binary_search_correctness(self):
        """Test that binary search maintains correct order under various scenarios."""
        # Create a graph that will generate many queue insertions
        self.graph.add_node("START")
        for i in range(10):
            node = f"N{i}"
            self.graph.add_node(node)
            # Connect START to each node with different costs
            self.graph.add_edge("START", node, 10 - i)  # Costs 10, 9, 8, ..., 1
        
        self.graph.add_node("END")
        for i in range(10):
            node = f"N{i}"
            # Connect each node to END with cost 1
            self.graph.add_edge(node, "END", 1)
        
        result = self.graph.ucs("START", "END")
        # Should find path through N9 (cost 1 + 1 = 2)
        self.assertIn("N9", result)
        self.assertIn("Total cost: 2", result)


class TestUCSEdgeCases(unittest.TestCase):
    """Test edge cases for UCS algorithm."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.graph = Graph()
    
    def test_ucs_single_node(self):
        """Test UCS on single node (start = target)."""
        self.graph.add_node("A")
        result = self.graph.ucs("A", "A")
        self.assertIn("Path: A", result)
        self.assertIn("Total cost: 0", result)
    
    def test_ucs_no_path(self):
        """Test UCS when no path exists."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        # No edges between A and B
        result = self.graph.ucs("A", "B")
        self.assertEqual(result, "B is unreachable")
    
    def test_ucs_zero_cost_edges(self):
        """Test UCS with zero-cost edges."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        
        self.graph.add_edge("A", "B", 0)
        self.graph.add_edge("B", "C", 0)
        
        result = self.graph.ucs("A", "C")
        self.assertIn("Total cost: 0", result)
        self.assertIn("Path: A -> B -> C", result)
    
    def test_ucs_high_cost_edges(self):
        """Test UCS with very high cost edges."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        
        self.graph.add_edge("A", "B", 1000000)
        self.graph.add_edge("A", "C", 1)
        self.graph.add_edge("C", "B", 1)
        
        result = self.graph.ucs("A", "B")
        self.assertIn("Path: A -> C -> B", result)
        self.assertIn("Total cost: 2", result)
    
    def test_ucs_complex_path_selection(self):
        """Test UCS choosing optimal path in complex scenario."""
        # Create a diamond-shaped graph with different path costs
        self.graph.add_node("START")
        self.graph.add_node("TOP")
        self.graph.add_node("BOTTOM")
        self.graph.add_node("END")
        
        # Two paths: START -> TOP -> END (cost 100) vs START -> BOTTOM -> END (cost 3)
        self.graph.add_edge("START", "TOP", 50)
        self.graph.add_edge("START", "BOTTOM", 2)
        self.graph.add_edge("TOP", "END", 50)
        self.graph.add_edge("BOTTOM", "END", 1)
        
        result = self.graph.ucs("START", "END")
        self.assertIn("Path: START -> BOTTOM -> END", result)
        self.assertIn("Total cost: 3", result)
    
    def test_ucs_revisiting_nodes(self):
        """Test that UCS correctly handles revisiting nodes with higher costs."""
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        
        # Create scenario where we might reach D via multiple paths
        self.graph.add_edge("A", "B", 1)
        self.graph.add_edge("A", "C", 10)
        self.graph.add_edge("B", "D", 1)
        self.graph.add_edge("C", "D", 1)
        
        result = self.graph.ucs("A", "D")
        self.assertIn("Path: A -> B -> D", result)
        self.assertIn("Total cost: 2", result)


class TestSearchAlgorithmComparison(unittest.TestCase):
    """Test comparing different search algorithms on same graphs."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.graph = Graph()
        
        # Create a test graph where BFS and UCS will find different paths
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        
        # BFS will find A -> D (direct), UCS will find A -> B -> C -> D (cheaper)
        self.graph.add_edge("A", "D", 100)  # Expensive direct path
        self.graph.add_edge("A", "B", 1)
        self.graph.add_edge("B", "C", 1)
        self.graph.add_edge("C", "D", 1)
    
    def test_bfs_vs_ucs_different_results(self):
        """Test that BFS and UCS can find different paths."""
        bfs_result = self.graph.bfs("A", "D")
        ucs_result = self.graph.ucs("A", "D")
        
        # BFS should find direct path (ignores weights)
        self.assertIn("A", bfs_result)
        self.assertIn("D", bfs_result)
        
        # UCS should find optimal path
        self.assertIn("Path: A -> B -> C -> D", ucs_result)
        self.assertIn("Total cost: 3", ucs_result)
    
    def test_dfs_vs_ucs_different_results(self):
        """Test that DFS and UCS can find different paths."""
        dfs_result = self.graph.dfs("A", "D")
        ucs_result = self.graph.ucs("A", "D")
        
        # Both should find a path, but likely different ones
        self.assertIn("A", dfs_result)
        self.assertIn("D", dfs_result)
        
        # UCS should find optimal path
        self.assertIn("Total cost: 3", ucs_result)
    
    def test_all_algorithms_unreachable(self):
        """Test all algorithms handle unreachable targets consistently."""
        self.graph.add_node("ISOLATED")
        
        bfs_result = self.graph.bfs("A", "ISOLATED")
        dfs_result = self.graph.dfs("A", "ISOLATED")
        ucs_result = self.graph.ucs("A", "ISOLATED")
        
        self.assertIn("can't be reached", bfs_result)
        self.assertIn("unreachable", dfs_result)
        self.assertIn("unreachable", ucs_result)


if __name__ == '__main__':
    unittest.main()
