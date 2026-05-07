class GraphNode:
    def __init__(self, name):
        self.name = str(name)
        self.connections = {}

    def add_connection(self, target, weight=1):
        self.connections[target] = weight

    def remove_connection(self, target):
        if target in self.connections:
            del self.connections[target]

    def get_connections(self):
        return self.connections

    def get_name(self):
        return self.name

    def __repr__(self):
        return f"GraphNode({self.name})"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name if isinstance(other, GraphNode) else self.name == other