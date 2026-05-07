from graph_node import GraphNode
from collections import deque
import heapq
import json
import os

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = GraphNode(name)
            return True
        return False

    def remove_node(self, name):
        if name in self.nodes:
            del self.nodes[name]
            for node in self.nodes.values():
                node.remove_connection(name)
            return True
        return False

    def add_edge(self, from_name, to_name, weight=1):
        if from_name not in self.nodes:
            self.add_node(from_name)
        if to_name not in self.nodes:
            self.add_node(to_name)
        self._add_edge_impl(from_name, to_name, weight)

    def _add_edge_impl(self, from_name, to_name, weight):
        raise NotImplementedError

    def remove_edge(self, from_name, to_name):
        if from_name in self.nodes and to_name in self.nodes:
            self.nodes[from_name].remove_connection(to_name)
            return True
        return False

    def get_nodes(self):
        return list(self.nodes.keys())

    def get_edges(self):
        edges = []
        for from_name, node in self.nodes.items():
            for to_name in node.get_connections():
                edges.append((from_name, to_name))
        return edges

    def bfs(self, start_name, target_name):
        if start_name not in self.nodes or target_name not in self.nodes:
            return None

        visited = set()
        queue = deque([(start_name, [start_name])])

        while queue:
            current, path = queue.popleft()
            if current == target_name:
                return path

            if current in visited:
                continue

            visited.add(current)
            for neighbor in self._get_neighbors(current):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return None

    def dfs(self, start_name, target_name):
        if start_name not in self.nodes or target_name not in self.nodes:
            return None

        visited = set()
        stack = [(start_name, [start_name])]

        while stack:
            current, path = stack.pop()
            if current == target_name:
                return path

            if current in visited:
                continue

            visited.add(current)
            for neighbor in self._get_neighbors(current):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

        return None

    def shortest_path(self, start_name, target_name):
        raise NotImplementedError

    def _get_neighbors(self, node_name):
        if node_name in self.nodes:
            return list(self.nodes[node_name].get_connections().keys())
        return []

    def save_to_json(self, filename="data/graph.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        data = {
            "type": self.__class__.__name__,
            "nodes": list(self.nodes.keys()),
            "edges": self.get_edges_with_weights()
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_from_json(self, filename="data/graph.json"):
        if not os.path.exists(filename):
            return False
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.nodes = {}
            for node_name in data["nodes"]:
                self.add_node(node_name)

            for edge in data["edges"]:
                if len(edge) == 3:
                    from_name, to_name, weight = edge
                    self._add_edge_impl(from_name, to_name, weight)
                else:
                    from_name, to_name = edge
                    self._add_edge_impl(from_name, to_name, 1)
            return True
        except Exception:
            return False

    def get_edges_with_weights(self):
        edges = []
        for from_name, node in self.nodes.items():
            for to_name, weight in node.get_connections().items():
                edges.append((from_name, to_name, weight))
        return edges

    def __str__(self):
        result = f"{self.__class__.__name__}:\n"
        result += f"Nodes: {', '.join(self.get_nodes())}\n"
        result += "Edges:\n"
        for from_name, to_name, weight in self.get_edges_with_weights():
            result += f"  {from_name} --({weight})--> {to_name}\n"
        return result