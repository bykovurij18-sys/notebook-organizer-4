from graph import Graph
from collections import deque

class UndirectedGraph(Graph):
    def _add_edge_impl(self, from_name, to_name, weight=1):
        self.nodes[from_name].add_connection(to_name, weight)
        self.nodes[to_name].add_connection(from_name, weight)

    def remove_edge(self, from_name, to_name):
        if from_name in self.nodes and to_name in self.nodes:
            self.nodes[from_name].remove_connection(to_name)
            self.nodes[to_name].remove_connection(from_name)
            return True
        return False

    def shortest_path(self, start_name, target_name):
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