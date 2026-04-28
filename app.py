from flask import Flask, request, jsonify
from flask_cors import CORS
import heapq, time, random, math

app = Flask(__name__)
CORS(app)

# VEHICLE
def assign_vehicle(weight):
    if weight < 25:
        return {"type": "2-Wheeler", "icon": "🛵"}
    elif weight <= 45:
        return {"type": "4-Wheeler Small", "icon": "🚗"}
    else:
        return {"type": "4-Wheeler Big", "icon": "🚛"}

# MERGE SORT
def merge_sort(arr, key):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            res.append(left[i]); i+=1
        else:
            res.append(right[j]); j+=1
    res.extend(left[i:]); res.extend(right[j:])
    return res

# SORT API (UPDATED WITH SMART SCORE)
@app.route('/api/sort', methods=['POST'])
def sort_packages():
    data = request.json
    packages = data.get('packages', [])
    sort_key = data.get('key', 'deadline')

    for p in packages:
        p['vehicle'] = assign_vehicle(p.get('weight', 0))
        # NEW LOGIC
        p['score'] = (
            p.get('priority',0)*2 +
            (100 - p.get('deadline',0)) -
            p.get('distance',0)
        )

    t0 = time.perf_counter()

    if sort_key == 'score':
        sorted_pkgs = merge_sort(packages, 'score')
        complexity = "Smart Score O(n log n)"
    else:
        sorted_pkgs = merge_sort(packages, sort_key)
        complexity = "O(n log n)"

    elapsed = round((time.perf_counter()-t0)*1000,4)

    return jsonify({
        "sorted": sorted_pkgs,
        "complexity": complexity,
        "time_ms": elapsed
    })

# GENERATE DATA
@app.route('/api/generate')
def gen():
    packages=[]
    for i in range(8):
        w = round(random.uniform(1,80),1)
        packages.append({
            "id": f"PKG-{i+1}",
            "weight": w,
            "deadline": random.randint(1,24),
            "priority": random.randint(1,10),
            "value": random.randint(50,500),
            "distance": random.randint(1,50)
        })
    return jsonify({"packages":packages})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
