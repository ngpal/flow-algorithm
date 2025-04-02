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

    def add_node(self, id: int):
        ...

    def add_nodes(self, *ids):
        map(self.add_node, ids)

    def add_arc(self, a_id: int, b_id: int, capacity: int):
        ...

    # Checks whether a node is a source O(V + E)
    def is_source(self, id: int) -> bool:
        return True

    # Checks whether a node is a sink O(1)
    def is_sink(self, id: int) -> bool:
        return True

