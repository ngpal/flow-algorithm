# Arc is an edge
class Arc:
    def __init__(self, capacity, residual=None):
        self.capacity = capacity
        self.residual = residual
        self.flow = 0

    def is_residual(self):
        return self.capacity == 0

    def remaining(self):
        return self.capacity - self.flow

    def is_full(self) -> bool:
        return self.remaining() == 0

    def augment(self, flow: int):
        self.flow += flow
        self.residual.flow -= flow


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
        elif b_id in self.sources:
            self.sources.remove(b_id)

        self.graph[b_id][a_id] = Arc(0)
        self.graph[a_id][b_id] = Arc(capacity, self.graph[b_id][a_id])

    def add_arcs(self, *arcs):
        for arc in arcs:
            self.add_arc(*arc)

    # O(1) lookup
    def is_source(self, id: int) -> bool:
        return id in self.sources

    # O(1) lookup
    def is_sink(self, id: int) -> bool:
        return id in self.sinks

    def print(self):
        print("sources:", self.sources)
        print("sinks:", self.sinks)
        for a, neighbours in self.graph.items():
            for b, e in neighbours.items():
                if not e.is_residual():
                    print(f"{a} -> {b} | {e.flow}/{e.capacity}")


def dinics(g: FlowGraph):
    from collections import deque

    source = next(iter(g.sources))
    sink = next(iter(g.sinks))

    level = {}

    # Step 1: Build level graph using BFS
    def bfs():
        nonlocal level
        level = {v: -1 for v in g.graph}
        queue = deque([source])
        level[source] = 0
        while queue:
            u = queue.popleft()
            for v, arc in g.graph[u].items():
                if level[v] == -1 and arc.remaining() > 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        return level[sink] != -1

    # Step 2: DFS to send flow through level-respecting paths
    def dfs(u, flow):
        if u == sink:
            return flow
        for v, arc in g.graph[u].items():
            if level.get(v, -1) == level[u] + 1 and arc.remaining() > 0:
                pushed = dfs(v, min(flow, arc.remaining()))
                if pushed > 0:
                    arc.augment(pushed)
                    return pushed
        return 0

    # Main loop
    max_flow = 0
    while bfs():  # while we can build level graph
        while True:
            pushed = dfs(source, float('inf'))
            if pushed == 0:
                break
            max_flow += pushed
    return max_flow

if __name__ == "__main__":
    g = FlowGraph()

    g.add_arcs(
        (0, 1, 3),
        (0, 2, 7),
        (2, 1, 5),
        (1, 3, 3),
        (1, 4, 4),
        (2, 4, 3),
        (3, 4, 3),
        (3, 5, 2),
        (4, 5, 6),
    )

    max_flow = dinics(g)
    print("Max flow attained:", max_flow)
    g.print()
