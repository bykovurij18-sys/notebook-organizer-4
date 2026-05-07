from graph import Graph
import heapq

class WeightedGraph(Graph):
    def _add_edge_impl(self, from_name, to_name, weight=1):
        if weight <= 0:
            raise ValueError("Weight must be positive")
        self.nodes[from_name].add_connection(to_name, weight)

    def add_edge(self, from_name, to_name, weight=1):
        if weight <= 0:
            raise ValueError("Weight must be positive")
        super().add_edge(from_name, to_name, weight)

    def shortest_path(self, start_name, target_name):
        if start_name not in self.nodes or target_name not in self.nodes:
            return None

        distances = {node: float('inf') for node in self.nodes}
        distances[start_name] = 0
        previous = {node: None for node in self.nodes}
        pq = [(0, start_name)]

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current == target_name:
                path = []
                while current is not None:
                    path.append(current)
                    current = previous[current]
                return path[::-1]

            if current_dist > distances[current]:
                continue

            for neighbor, weight in self.nodes[current].get_connections().items():
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))

        return None

    def dijkstra(self, start_name, target_name):
        return self.shortest_path(start_name, target_name)