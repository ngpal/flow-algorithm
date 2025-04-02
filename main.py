# Arc is an edge
class Arc:
    def __init__(self, capacity):
        self.capacity = capacity
        self.flow = 0

    def is_recidual(self):
        return self.capacity == 0

    def remaining(self):
        return self.capacity - self.flow

    def is_full(self) -> bool:
        return self.remaining == 0


class FlowGraph:
    def __init__(self):
        self.graph = {}
        self.sources = set()
        self.sinks = set()

    def add_arc(self, a_id: int, b_id: int, capacity: int):
        if a_id not in self.graph:
            self.graph[a_id] = {}
            self.sources.add(a_id)
        elif a_id in self.sinks:
            self.sinks.remove(a_id)

        if b_id not in self.graph:
            self.graph[b_id] = {}
            self.sinks.add(b_id)
        elif b_id in self.sinks:
            self.sources.remove(b_id)

        self.graph[a_id][b_id] = Arc(capacity)
        self.graph[b_id][a_id] = Arc(0)

    # O(1) lookup
    def is_source(self, id: int) -> bool:
        return id in self.sources

    # O(1) lookup
    def is_sink(self, id: int) -> bool:
        return id in self.sinks

