# Road represents a directed edge (road segment) with capacity (vehicle throughput)
class Road:
    def __init__(self, capacity, residual=None):
        self.capacity = capacity  # Max number of vehicles per time unit
        self.residual = residual  # Backward road for residual capacity
        self.flow = 0             # Current traffic on this road

    def is_residual(self):
        return self.capacity == 0

    def remaining(self):
        return self.capacity - self.flow  # Remaining capacity

    def is_full(self) -> bool:
        return self.remaining() == 0

    def augment(self, flow: int):
        # Push traffic forward and update the backward road
        self.flow += flow
        self.residual.flow -= flow


# TrafficNetwork models the road network from housing to workplaces
class TrafficNetwork:
    def __init__(self):
        self.network = {}  # Adjacency list: {intersection: {neighbour: Road}}
        self.housings = set()
        self.workplaces = set()

    def add_road(self, from_intersection: int, to_intersection: int, capacity: int):
        # Register nodes and their roles (housing or workplace)
        if from_intersection not in self.network:
            self.network[from_intersection] = {}
            self.housings.add(from_intersection)
        elif from_intersection in self.workplaces:
            self.workplaces.remove(from_intersection)

        if to_intersection not in self.network:
            self.network[to_intersection] = {}
            self.workplaces.add(to_intersection)
        elif to_intersection in self.housings:
            self.housings.remove(to_intersection)

        # Add forward and backward (residual) roads
        self.network[to_intersection][from_intersection] = Road(0)
        self.network[from_intersection][to_intersection] = Road(
            capacity, self.network[to_intersection][from_intersection]
        )

    def add_roads(self, *roads):
        for road in roads:
            self.add_road(*road)

    def is_housing(self, id: int) -> bool:
        return id in self.housings

    def is_workplace(self, id: int) -> bool:
        return id in self.workplaces

    def print_status(self):
        print("Housings:", self.housings)
        print("Workplaces:", self.workplaces)
        for a, neighbours in self.network.items():
            for b, road in neighbours.items():
                if not road.is_residual():
                    print(f"{a} -> {b} | {road.flow}/{road.capacity}")


# Dinic's algorithm to compute max traffic flow from housings to workplaces
def compute_max_traffic_flow(city: TrafficNetwork):
    from collections import deque

    source = next(iter(city.housings))
    sink = next(iter(city.workplaces))

    level = {}

    # Step 1: Build level graph using BFS
    def bfs():
        nonlocal level
        level = {v: -1 for v in city.network}
        queue = deque([source])
        level[source] = 0
        while queue:
            u = queue.popleft()
            for v, road in city.network[u].items():
                if level[v] == -1 and road.remaining() > 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        return level[sink] != -1

    # Step 2: DFS to push traffic through shortest valid routes
    def dfs(u, flow):
        if u == sink:
            return flow
        for v, road in city.network[u].items():
            if level.get(v, -1) == level[u] + 1 and road.remaining() > 0:
                pushed = dfs(v, min(flow, road.remaining()))
                if pushed > 0:
                    road.augment(pushed)
                    return pushed
        return 0

    # Main loop
    max_flow = 0
    while bfs():
        while True:
            pushed = dfs(source, float('inf'))
            if pushed == 0:
                break
            max_flow += pushed
    return max_flow


if __name__ == "__main__":
    city = TrafficNetwork()

    # (from_intersection, to_intersection, capacity)
    city.add_roads(
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

    max_traffic = compute_max_traffic_flow(city)
    print("Maximum traffic flow from housing to workplace:", max_traffic)
    city.print_status()
