
import time
import random
import heapq

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        
        if isinstance(other, Node):
            return (self.x, self.y) < (other.x, other.y) 
        return False

    def __str__(self):
        return f"Node({self.x}, {self.y})" 

def zero_heuristic(a, b):
    # A non-informative heuristic that always returns zero
    return 0
def inadmissible_heuristic(a, b):
    # Manhattan distance overestimated by multiplying by a constant factor (e.g., 2)
    return 2 * (abs(a.x - b.x) + abs(a.y - b.y))


def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def generate_graph(num_nodes, density=0.2):
   
    nodes = [Node(x, y) for x in range(num_nodes) for y in range(num_nodes)]
    
   
    graph = {node: {} for node in nodes}

    
    for node in nodes:
        for neighbor in nodes:
            if random.random() < density and node != neighbor:
                graph[node][neighbor] = random.randint(1, 10)

    return graph, nodes[0], nodes[-1]  

def generate_graph_with_barriers(num_nodes, density=0.2, blocked_percentage=0.2):
    nodes = [Node(x, y) for x in range(num_nodes) for y in range(num_nodes)]
    
    total_nodes = len(nodes)
    num_blocked = int(total_nodes * blocked_percentage)
    
    blocked_nodes = set(random.sample(nodes, num_blocked))
    
 
    start = nodes[0]
    goal = nodes[-1]
    
   
    blocked_nodes.discard(start)
    blocked_nodes.discard(goal)
    
   
    graph = {node: {} for node in nodes}
    
   
    for node in nodes:
        if node in blocked_nodes:
            continue  
        
        for neighbor in nodes:
            if node != neighbor and random.random() < density and neighbor not in blocked_nodes:
                graph[node][neighbor] = random.randint(1, 10)  
    return graph, start, goal, len(nodes), blocked_nodes 

def run_performance_test(num_nodes, density, blocked_percentage):

    graph, start, goal, total_nodes, blocked_nodes = generate_graph_with_barriers(num_nodes, density, blocked_percentage)
    start_time = time.time()
    gbfs_visited = greedy_best_first(graph, start, goal, heuristic, blocked_nodes)
    gbfs_time = time.time() - start_time
    start_time = time.time()
    astar_visited = a_star(graph, start, goal, heuristic, blocked_nodes)
    astar_time = time.time() - start_time
    start_time = time.time()
    astar_visited_zeroh = a_star(graph, start, goal, zero_heuristic, blocked_nodes)  # Use zero heuristic
    astar_time_zeroh = time.time() - start_time
    start_time = time.time()
    astar_visited_inadmit = a_star(graph, start, goal, inadmissible_heuristic, blocked_nodes)  # Use inadmissable heuristic
    astar_time_inadmit = time.time() - start_time
    start_time = time.time()
    dijkstra_visited = dijkstra(graph, start, goal, blocked_nodes)
    dijkstra_time = time.time() - start_time
    
    print(f"Graph size: {num_nodes}x{num_nodes} | Density: {density} | Blocked Percentage: {blocked_percentage * 100}%")
    print(f"Greedy Best-First Search: {gbfs_visited} nodes visited out of {total_nodes}, Time: {gbfs_time:.4f}s")
    print(f"A* Algorithm: {astar_visited} nodes visited out of {total_nodes}, Time: {astar_time:.4f}s")
    print(f"A* Algorithm (Zero heuristic): {astar_visited_zeroh} nodes visited out of {total_nodes}, Time: {astar_time_zeroh:.4f}s")
    print(f"A* Algorithm (Inadmissable heuristic): {astar_visited_inadmit} nodes visited out of {total_nodes}, Time: {astar_time_inadmit:.4f}s")
    print(f"Dijkstra: {dijkstra_visited} nodes visited out of {total_nodes}, Time: {dijkstra_time:.4f}s")
    print("--------------------------------------------------------")

def dijkstra(graph, start, goal, blocked_nodes):
    open_list = [(0, start)]  # (distance, node)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    came_from = {}
    
    nodes_visited = 0
    visited_nodes = set()  # Track visited nodes
    
    while open_list:
        current_distance, current_node = heapq.heappop(open_list)
        
        # Skip blocked nodes and already visited nodes
        if current_node in blocked_nodes or current_node in visited_nodes:
            continue
        
        visited_nodes.add(current_node)
        nodes_visited += 1
        
        if current_node == goal:
            return nodes_visited
        
        for neighbor, weight in graph[current_node].items():
            if neighbor in blocked_nodes or neighbor in visited_nodes:
                continue
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                came_from[neighbor] = current_node
                heapq.heappush(open_list, (distance, neighbor))
    
    return nodes_visited



def greedy_best_first(graph, start, goal, heuristic, blocked_nodes):
    open_list = [(start, heuristic(start, goal))]
    g_cost = {start: 0}
    f_cost = {start: heuristic(start, goal)}
    came_from = {}
    
    nodes_visited = 0
    visited_nodes = set()  # Track visited nodes
    
    while open_list:
        current_node, _ = heapq.heappop(open_list)
        
        # Skip blocked nodes and already visited nodes
        if current_node in blocked_nodes or current_node in visited_nodes:
            continue
        
        visited_nodes.add(current_node)
        nodes_visited += 1
        
        if current_node == goal:
            return nodes_visited
        
        for neighbor, weight in graph[current_node].items():
            if neighbor in blocked_nodes or neighbor in visited_nodes:
                continue
            tentative_g = g_cost[current_node] + weight
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                came_from[neighbor] = current_node
                g_cost[neighbor] = tentative_g
                f_cost[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (neighbor, f_cost[neighbor]))
    
    return nodes_visited



def a_star(graph, start, goal, heuristic, blocked_nodes):
    open_list = [(start, heuristic(start, goal))]
    g_cost = {start: 0}
    f_cost = {start: heuristic(start, goal)}
    came_from = {}
    
    nodes_visited = 0
    visited_nodes = set()  # Track visited nodes
    
    while open_list:
        current_node, _ = heapq.heappop(open_list)
        
        # Skip blocked nodes and already visited nodes
        if current_node in blocked_nodes or current_node in visited_nodes:
            continue
        
        visited_nodes.add(current_node)
        nodes_visited += 1
        
        if current_node == goal:
            return nodes_visited
        
        for neighbor, weight in graph[current_node].items():
            if neighbor in blocked_nodes or neighbor in visited_nodes:
                continue
            tentative_g = g_cost[current_node] + weight
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                came_from[neighbor] = current_node
                g_cost[neighbor] = tentative_g
                f_cost[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (neighbor, f_cost[neighbor]))
    
    return nodes_visited


print("Running test: Small Graph, Sparse Connections, Low Blockage")
run_performance_test(5, 0.2, 0.2)  # Small graph, 20% blocked nodes
run_performance_test(5, 0.2, 0.4)  # Small graph, 40% blocked nodes
run_performance_test(5, 0.2, 0.6)  # Small graph, 60% blocked nodes

# Medium Graph, Sparse Connections
print("\nRunning test: Medium Graph, Sparse Connections")
run_performance_test(10, 0.2, 0.1)  # Medium graph, 10% blocked nodes
run_performance_test(10, 0.2, 0.3)  # Medium graph, 30% blocked nodes
run_performance_test(10, 0.2, 0.5)  # Medium graph, 50% blocked nodes

# Small Graph, Dense Connections
print("\nRunning test: Small Graph, Dense Connections")
run_performance_test(5, 0.8, 0.1)  # Small graph, dense connections, 10% blocked nodes
run_performance_test(5, 0.8, 0.3)  # Small graph, dense connections, 30% blocked nodes
run_performance_test(5, 0.8, 0.5)  # Small graph, dense connections, 50% blocked nodes

# Larger Graph, Dense Connections
print("\nRunning test: Larger Graph, Dense Connections")
run_performance_test(10, 0.8, 0.1)  # Larger graph, dense connections, 10% blocked nodes
run_performance_test(10, 0.8, 0.3)  # Larger graph, dense connections, 30% blocked nodes
run_performance_test(10, 0.8, 0.5)  # Larger graph, dense connections, 50% blocked nodes

# Large Graph, Sparse Connections
print("\nRunning test: Large Graph, Sparse Connections")
run_performance_test(20, 0.2, 0.1)  # Larger graph, sparse connections, 10% blocked nodes
run_performance_test(20, 0.2, 0.2)  # Larger graph, sparse connections, 20% blocked nodes
run_performance_test(20, 0.2, 0.5)  # Larger graph, sparse connections, 50% blocked nodes

# Extreme Blockage Case
print("\nRunning test: Extreme Blockage")
run_performance_test(10, 0.4, 0.7)  # Large graph, 70% blocked nodes
run_performance_test(10, 0.4, 0.9)  # Large graph, 90% blocked nodes