from flask import Flask, request, jsonify
from flask_cors import CORS
import heapq
import time
import random
import math

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────
#  VEHICLE TYPE ASSIGNMENT
# ─────────────────────────────────────────────
def assign_vehicle(weight):
    if weight < 25:
        return {"type": "2-Wheeler", "icon": "🛵", "capacity": "< 25 kg", "color": "#ff6b00"}
    elif 25 <= weight <= 45:
        return {"type": "4-Wheeler Small", "icon": "🚗", "capacity": "25–45 kg", "color": "#ff9500"}
    else:
        return {"type": "4-Wheeler Big", "icon": "🚛", "capacity": "> 45 kg", "color": "#ffb800"}

# ─────────────────────────────────────────────
#  MODULE 1: SORTING ALGORITHMS
# ─────────────────────────────────────────────
def merge_sort(packages, key):
    if len(packages) <= 1:
        return packages
    mid = len(packages) // 2
    left = merge_sort(packages[:mid], key)
    right = merge_sort(packages[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(packages, key, low=None, high=None):
    packages = packages[:]
    if low is None: low = 0
    if high is None: high = len(packages) - 1
    def partition(arr, l, h):
        pivot = arr[h][key]
        i = l - 1
        for j in range(l, h):
            if arr[j][key] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[h] = arr[h], arr[i+1]
        return i + 1
    def _quick(arr, l, h):
        if l < h:
            pi = partition(arr, l, h)
            _quick(arr, l, pi - 1)
            _quick(arr, pi + 1, h)
    _quick(packages, low, high)
    return packages

def heap_sort(packages, key):
    packages = packages[:]
    n = len(packages)
    def heapify(arr, n, i):
        largest = i
        l, r = 2*i+1, 2*i+2
        if l < n and arr[l][key] > arr[largest][key]: largest = l
        if r < n and arr[r][key] > arr[largest][key]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    for i in range(n//2 - 1, -1, -1):
        heapify(packages, n, i)
    for i in range(n-1, 0, -1):
        packages[0], packages[i] = packages[i], packages[0]
        heapify(packages, i, 0)
    return packages

@app.route('/api/sort', methods=['POST'])
def sort_packages():
    data = request.json
    packages = data.get('packages', [])
    algorithm = data.get('algorithm', 'merge')
    sort_key = data.get('key', 'deadline')

    # Add vehicle assignment to each package
    for p in packages:
        p['vehicle'] = assign_vehicle(p.get('weight', 0))

    t0 = time.perf_counter()
    if algorithm == 'merge':
        sorted_pkgs = merge_sort(packages, sort_key)
        complexity = "O(n log n) — Stable"
    elif algorithm == 'quick':
        sorted_pkgs = quick_sort(packages, sort_key)
        complexity = "O(n log n) avg — Not Stable"
    elif algorithm == 'heap':
        sorted_pkgs = heap_sort(packages, sort_key)
        complexity = "O(n log n) — Not Stable"
    else:
        sorted_pkgs = packages
        complexity = "N/A"
    elapsed = round((time.perf_counter() - t0) * 1000, 4)

    return jsonify({
        "sorted": sorted_pkgs,
        "algorithm": algorithm.title() + " Sort",
        "complexity": complexity,
        "time_ms": elapsed,
        "count": len(sorted_pkgs)
    })

# ─────────────────────────────────────────────
#  MODULE 2: GRAPH — DIJKSTRA & BELLMAN-FORD
# ─────────────────────────────────────────────
def dijkstra(graph, start, end, nodes):
    dist = {n: float('inf') for n in nodes}
    prev = {n: None for n in nodes}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in graph.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    # Reconstruct path
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return dist[end], path if path[0] == start else []

def bellman_ford(edges, start, end, nodes):
    dist = {n: float('inf') for n in nodes}
    prev = {n: None for n in nodes}
    dist[start] = 0
    for _ in range(len(nodes) - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return dist[end], path if path[0] == start else []

@app.route('/api/route', methods=['POST'])
def find_route():
    data = request.json
    nodes = data.get('nodes', [])
    edges_raw = data.get('edges', [])  # [{from, to, weight}]
    start = data.get('start')
    end = data.get('end')
    algorithm = data.get('algorithm', 'dijkstra')

    graph = {}
    edges = []
    for e in edges_raw:
        u, v, w = e['from'], e['to'], e['weight']
        graph.setdefault(u, []).append((v, w))
        graph.setdefault(v, []).append((u, w))
        edges.append((u, v, w))
        edges.append((v, u, w))

    t0 = time.perf_counter()
    if algorithm == 'dijkstra':
        cost, path = dijkstra(graph, start, end, nodes)
        complexity = "O((V + E) log V)"
    else:
        cost, path = bellman_ford(edges, start, end, nodes)
        complexity = "O(V × E)"
    elapsed = round((time.perf_counter() - t0) * 1000, 4)

    return jsonify({
        "path": path,
        "cost": cost if cost != float('inf') else -1,
        "algorithm": algorithm.title().replace('-', '-'),
        "complexity": complexity,
        "time_ms": elapsed
    })

# ─────────────────────────────────────────────
#  MODULE 3: GREEDY — FRACTIONAL KNAPSACK
# ─────────────────────────────────────────────
@app.route('/api/greedy', methods=['POST'])
def greedy_assign():
    data = request.json
    packages = data.get('packages', [])
    capacity = data.get('capacity', 100)

    items = [(p['value'] / p['weight'], p['weight'], p['value'], p['id'], p) for p in packages if p['weight'] > 0]
    items.sort(reverse=True)

    t0 = time.perf_counter()
    remaining = capacity
    selected = []
    total_value = 0

    for ratio, w, v, pid, pkg in items:
        if remaining <= 0: break
        vehicle = assign_vehicle(w)
        if w <= remaining:
            selected.append({**pkg, "fraction": 1.0, "taken_weight": w, "vehicle": vehicle})
            total_value += v
            remaining -= w
        else:
            frac = remaining / w
            selected.append({**pkg, "fraction": round(frac, 3), "taken_weight": round(remaining, 2), "vehicle": vehicle})
            total_value += v * frac
            remaining = 0

    elapsed = round((time.perf_counter() - t0) * 1000, 4)
    return jsonify({
        "selected": selected,
        "total_value": round(total_value, 2),
        "used_capacity": round(capacity - remaining, 2),
        "capacity": capacity,
        "complexity": "O(n log n)",
        "time_ms": elapsed
    })

# ─────────────────────────────────────────────
#  MODULE 4: DP — 0/1 KNAPSACK
# ─────────────────────────────────────────────
@app.route('/api/dp', methods=['POST'])
def dp_knapsack():
    data = request.json
    packages = data.get('packages', [])
    capacity = int(data.get('capacity', 50))

    weights = [int(p['weight']) for p in packages]
    values = [int(p['value']) for p in packages]
    n = len(packages)

    t0 = time.perf_counter()
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])

    # Backtrack
    selected_ids = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_ids.append(packages[i-1]['id'])
            w -= weights[i-1]

    selected = []
    for p in packages:
        if p['id'] in selected_ids:
            selected.append({**p, "vehicle": assign_vehicle(p['weight'])})

    elapsed = round((time.perf_counter() - t0) * 1000, 4)
    return jsonify({
        "selected": selected,
        "max_value": dp[n][capacity],
        "capacity": capacity,
        "dp_table_size": f"{n+1} × {capacity+1}",
        "complexity": "O(n × W)",
        "time_ms": elapsed
    })

# ─────────────────────────────────────────────
#  MODULE 5: DIVIDE & CONQUER — CLOSEST PAIR
# ─────────────────────────────────────────────
def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def closest_pair(points):
    def brute(pts):
        min_d = float('inf')
        pair = (pts[0], pts[1])
        for i in range(len(pts)):
            for j in range(i+1, len(pts)):
                d = dist(pts[i], pts[j])
                if d < min_d:
                    min_d = d
                    pair = (pts[i], pts[j])
        return min_d, pair

    def strip_closest(strip, d):
        min_d = d
        pair = None
        strip.sort(key=lambda p: p[1])
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j][1] - strip[i][1]) < min_d:
                dd = dist(strip[i], strip[j])
                if dd < min_d:
                    min_d = dd
                    pair = (strip[i], strip[j])
                j += 1
        return min_d, pair

    def rec(pts):
        n = len(pts)
        if n <= 3:
            return brute(pts)
        mid = n // 2
        mid_point = pts[mid]
        dl, pl = rec(pts[:mid])
        dr, pr = rec(pts[mid:])
        if dl < dr:
            d, best_pair = dl, pl
        else:
            d, best_pair = dr, pr
        strip = [p for p in pts if abs(p[0] - mid_point[0]) < d]
        ds, ps = strip_closest(strip, d)
        if ps and ds < d:
            return ds, ps
        return d, best_pair

    sorted_pts = sorted(points, key=lambda p: p[0])
    return rec(sorted_pts)

@app.route('/api/divide', methods=['POST'])
def divide_conquer():
    data = request.json
    warehouses = data.get('warehouses', [])  # [{id, x, y, name}]

    points = [(w['x'], w['y'], w['name']) for w in warehouses]
    pts_xy = [(p[0], p[1]) for p in points]

    t0 = time.perf_counter()
    if len(pts_xy) >= 2:
        min_dist, pair = closest_pair(pts_xy)
        p1_name = points[pts_xy.index(pair[0])][2]
        p2_name = points[pts_xy.index(pair[1])][2]
    else:
        min_dist = 0
        p1_name = p2_name = ""
    elapsed = round((time.perf_counter() - t0) * 1000, 4)

    return jsonify({
        "closest_pair": [p1_name, p2_name],
        "min_distance": round(min_dist, 4),
        "complexity": "O(n log n)",
        "recurrence": "T(n) = 2T(n/2) + O(n)",
        "time_ms": elapsed
    })

# ─────────────────────────────────────────────
#  GENERATE RANDOM SAMPLE DATA
# ─────────────────────────────────────────────
@app.route('/api/generate', methods=['GET'])
def generate_data():
    n = int(request.args.get('n', 8))
    packages = []
    for i in range(n):
        w = round(random.uniform(1, 80), 1)
        packages.append({
            "id": f"PKG-{i+1:03d}",
            "weight": w,
            "deadline": random.randint(1, 24),
            "priority": random.randint(1, 10),
            "value": round(random.uniform(50, 500), 2),
            "distance": round(random.uniform(1, 50), 1),
            "vehicle": assign_vehicle(w)
        })
    cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Jaipur"]
    nodes = cities[:min(n, len(cities))]
    edges = []
    for i in range(len(nodes)-1):
        edges.append({"from": nodes[i], "to": nodes[i+1], "weight": random.randint(10, 200)})
    if len(nodes) > 2:
        edges.append({"from": nodes[0], "to": nodes[2], "weight": random.randint(50, 300)})
        edges.append({"from": nodes[1], "to": nodes[3 % len(nodes)], "weight": random.randint(30, 150)})

    warehouses = [{"id": i, "name": f"WH-{chr(65+i)}", "x": random.randint(0, 100), "y": random.randint(0, 100)} for i in range(6)]

    return jsonify({"packages": packages, "nodes": nodes, "edges": edges, "warehouses": warehouses})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
