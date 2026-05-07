import unittest
import os
import tempfile
from graph_factory import GraphFactory
from directed_graph import DirectedGraph
from undirected_graph import UndirectedGraph
from weighted_graph import WeightedGraph

class TestGraphNavigator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.original_dir)
        self.temp_dir.cleanup()

    def test_add_node(self):
        graph = UndirectedGraph()
        self.assertTrue(graph.add_node("A"))
        self.assertFalse(graph.add_node("A"))
        self.assertEqual(graph.get_nodes(), ["A"])

    def test_remove_node(self):
        graph = UndirectedGraph()
        graph.add_node("A")
        graph.add_node("B")
        graph.add_edge("A", "B")
        self.assertTrue(graph.remove_node("A"))
        self.assertEqual(graph.get_nodes(), ["B"])

    def test_add_edge_undirected(self):
        graph = UndirectedGraph()
        graph.add_edge("A", "B")
        self.assertEqual(len(graph.get_edges()), 1)

    def test_add_edge_directed(self):
        graph = DirectedGraph()
        graph.add_edge("A", "B")
        edges = graph.get_edges()
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0], ("A", "B"))

    def test_add_edge_weighted(self):
        graph = WeightedGraph()
        graph.add_edge("A", "B", 5)
        edges_with_weight = graph.get_edges_with_weights()
        self.assertEqual(edges_with_weight[0][2], 5)

    def test_bfs_path_exists(self):
        graph = UndirectedGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        path = graph.bfs("A", "C")
        self.assertEqual(path, ["A", "B", "C"])

    def test_bfs_path_not_exists(self):
        graph = UndirectedGraph()
        graph.add_node("A")
        graph.add_node("B")
        path = graph.bfs("A", "B")
        self.assertIsNone(path)

    def test_dfs_path_exists(self):
        graph = UndirectedGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        path = graph.dfs("A", "C")
        self.assertIsNotNone(path)

    def test_shortest_path_unweighted(self):
        graph = UndirectedGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("A", "C")
        path = graph.shortest_path("A", "C")
        self.assertEqual(len(path), 2)

    def test_shortest_path_weighted_dijkstra(self):
        graph = WeightedGraph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("B", "C", 1)
        graph.add_edge("A", "C", 5)
        path = graph.shortest_path("A", "C")
        self.assertEqual(path, ["A", "B", "C"])

    def test_factory_create_directed(self):
        graph = GraphFactory.create_graph("directed")
        self.assertIsInstance(graph, DirectedGraph)

    def test_factory_create_undirected(self):
        graph = GraphFactory.create_graph("undirected")
        self.assertIsInstance(graph, UndirectedGraph)

    def test_factory_create_weighted(self):
        graph = GraphFactory.create_graph("weighted")
        self.assertIsInstance(graph, WeightedGraph)

    def test_factory_invalid_type(self):
        with self.assertRaises(ValueError):
            GraphFactory.create_graph("invalid")

    def test_save_and_load_json(self):
        graph = WeightedGraph()
        graph.add_edge("A", "B", 5)
        graph.save_to_json("test.json")
        new_graph = GraphFactory.create_from_json("test.json")
        self.assertEqual(new_graph.get_nodes(), ["A", "B"])
        edges = new_graph.get_edges_with_weights()
        self.assertEqual(edges[0][2], 5)

    def test_remove_edge_undirected(self):
        graph = UndirectedGraph()
        graph.add_edge("A", "B")
        self.assertTrue(graph.remove_edge("A", "B"))
        self.assertEqual(len(graph.get_edges()), 0)

    def test_add_duplicate_node(self):
        graph = DirectedGraph()
        self.assertTrue(graph.add_node("A"))
        self.assertFalse(graph.add_node("A"))

    def test_invalid_weight(self):
        graph = WeightedGraph()
        with self.assertRaises(ValueError):
            graph.add_edge("A", "B", -5)

if __name__ == "__main__":
    unittest.main()