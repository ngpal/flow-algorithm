class Road:
    def __init__(self, capacity, residual=None):
        self.capacity = capacity
        self.residual = residual
        self.flow = 0

    def is_residual(self):
        return self.capacity == 0

    def remaining(self):
        return self.capacity - self.flow

    def is_full(self):
        return self.remaining() == 0

    def augment(self, flow):
        self.flow += flow
        self.residual.flow -= flow


class TrafficNetwork:
    def __init__(self):
        self.network = {}
        self.housings = set()
        self.workplaces = set()

    def add_road(self, u, v, capacity):
        if u not in self.network:
            self.network[u] = {}
        if v not in self.network:
            self.network[v] = {}

        # Create residual road
        backward = Road(0)
        forward = Road(capacity, backward)
        backward.residual = forward

        self.network[u][v] = forward
        self.network[v][u] = backward

    def add_roads(self, *roads):
        for road in roads:
            self.add_road(*road)

    def add_housing(self, node):
        self.housings.add(node)

    def add_workplace(self, node):
        self.workplaces.add(node)

    def print_status(self):
        print("Housings:", self.housings)
        print("Workplaces:", self.workplaces)
        for u, edges in self.network.items():
            for v, road in edges.items():
                if not road.is_residual():
                    print(f"{u} -> {v} | {road.flow}/{road.capacity}")


def compute_max_traffic_flow(city: TrafficNetwork):
    from collections import deque

    super_source = -1
    super_sink = -2

    city.network[super_source] = {}
    city.network[super_sink] = {}

    for housing in city.housings:
        city.add_road(super_source, housing, float('inf'))

    for workplace in city.workplaces:
        city.add_road(workplace, super_sink, float('inf'))

    level = {}

    def bfs():
        nonlocal level
        level = {v: -1 for v in city.network}
        level[super_source] = 0
        queue = deque([super_source])
        while queue:
            u = queue.popleft()
            for v, road in city.network[u].items():
                if level[v] == -1 and road.remaining() > 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        return level[super_sink] != -1

    def dfs(u, flow):
        if u == super_sink:
            return flow
        for v, road in city.network[u].items():
            if level.get(v, -1) == level[u] + 1 and road.remaining() > 0:
                pushed = dfs(v, min(flow, road.remaining()))
                if pushed > 0:
                    road.augment(pushed)
                    return pushed
        return 0

    max_flow = 0
    while bfs():
        while True:
            pushed = dfs(super_source, float('inf'))
            if pushed == 0:
                break
            max_flow += pushed
    return max_flow


if __name__ == "__main__":
    city = TrafficNetwork()

    # register 3 housings (nodes 0, 1, 2)
    city.add_housing(0)
    city.add_housing(1)
    city.add_housing(2)

    # register 2 workplaces (nodes 6, 7)
    city.add_workplace(6)
    city.add_workplace(7)

    city.add_roads(
        (0, 3, 3),
        (1, 3, 2),
        (2, 4, 4),
        (3, 4, 3),
        (3, 5, 2),
        (4, 5, 3),
        (5, 6, 3),
        (5, 7, 2),
    )

    max_traffic = compute_max_traffic_flow(city)
    print("Maximum traffic flow from all housings to all workplaces:", max_traffic)
    city.print_status()
