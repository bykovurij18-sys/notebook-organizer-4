from directed_graph import DirectedGraph
from undirected_graph import UndirectedGraph
from weighted_graph import WeightedGraph

class GraphFactory:
    @staticmethod
    def create_graph(graph_type):
        if graph_type == "directed":
            return DirectedGraph()
        elif graph_type == "undirected":
            return UndirectedGraph()
        elif graph_type == "weighted":
            return WeightedGraph()
        else:
            raise ValueError(f"Unknown graph type: {graph_type}")

    @staticmethod
    def create_from_json(filename="data/graph.json"):
        import json
        import os

        if not os.path.exists(filename):
            return None

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        graph_type = data.get("type", "UndirectedGraph")
        if graph_type == "DirectedGraph":
            graph = GraphFactory.create_graph("directed")
        elif graph_type == "WeightedGraph":
            graph = GraphFactory.create_graph("weighted")
        else:
            graph = GraphFactory.create_graph("undirected")

        graph.load_from_json(filename)
        return graph