# Arc is an edge
class Arc:
    def __init__(self, capacity):
        self.capacity = capacity
        self.flow = 0

    def remaining(self):
        return self.capacity - self.flow

    def is_full(self) -> bool:
        return self.remaining == 0


class FlowGraph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, id: int):
        self.graph[id] = {}

    # Checks whether a node is a source O(V + E)
    def is_source(self, id: int) -> bool:
        return True
