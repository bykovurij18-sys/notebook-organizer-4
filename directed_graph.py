from graph import Graph
from collections import deque
import heapq

class DirectedGraph(Graph):
    def _add_edge_impl(self, from_name, to_name, weight=1):
        self.nodes[from_name].add_connection(to_name, weight)

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