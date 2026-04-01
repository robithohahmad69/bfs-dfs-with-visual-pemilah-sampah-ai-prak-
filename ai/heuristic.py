import heapq

# ============================================================
# HEURISTIK: estimasi jumlah langkah minimum menuju T
# Semakin kecil nilainya = semakin dekat ke tujuan T
# Node buntu (G, I, J) diberi 99 agar tidak diprioritaskan
# ============================================================
heuristic = {
    "M": 6,   # M → A → C → E → T = 2+1+2+1=6
    "A": 4,   # A → C → E → T = 1+2+1=4
    "B": 4,   # B → C → E → T = 1+2+1=4
    "C": 3,   # C → E → T = 2+1=3
    "D": 4,   # D → C → E → T = 1+2+1=4
    "E": 1,   # E → T = 1
    "F": 99,  # F → G → buntu
    "H": 1,   # H → T = 1
    "T": 0,   # tujuan
    "G": 99,  # buntu
    "I": 99,  # buntu
    "J": 99,  # buntu
}


# ============================================================
# GREEDY BEST-FIRST SEARCH
# Prioritas hanya berdasarkan h(n) = heuristik saja
# Pilih node yang estimasinya paling dekat ke T
# Cepat tapi tidak selalu menemukan jalur paling optimal
# ============================================================
def greedy_bfs(graph, start):
    visited = set()
    # heap isi: (h(node), path)
    heap = [(heuristic.get(start, 99), [start])]

    while heap:
        h, path = heapq.heappop(heap)
        node = path[-1]

        if node in visited:
            continue

        print(f"Greedy Kunjungi: {node} | h={h}")
        visited.add(node)

        if node == "T" or node == "G" or node == "J":
            print("Greedy selesai di:", node, "| Jalur:", " -> ".join(path))
            return path

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(heap, (
                    heuristic.get(neighbor, 99),
                    path + [neighbor]
                ))

    return None


# ============================================================
# A* SEARCH
# Prioritas berdasarkan f(n) = g(n) + h(n)
# g(n) = jumlah langkah nyata dari start ke node ini
# h(n) = estimasi langkah ke T (heuristik)
# Lebih optimal dari Greedy karena pertimbangkan biaya nyata
# ============================================================
def astar(graph, start):
    visited = set()
    # heap isi: (f(n), g(n), path)
    heap = [(heuristic.get(start, 99), 0, [start])]

    while heap:
        f, g, path = heapq.heappop(heap)
        node = path[-1]

        if node in visited:
            continue

        print(f"A* Kunjungi: {node} | g={g}, h={heuristic.get(node,99)}, f={f}")
        visited.add(node)

        if node == "T" or node == "G" or node == "J":
            print("A* selesai di:", node, "| Jalur:", " -> ".join(path))
            return path

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                new_g = g + 1
                new_f = new_g + heuristic.get(neighbor, 99)
                heapq.heappush(heap, (new_f, new_g, path + [neighbor]))

    return None