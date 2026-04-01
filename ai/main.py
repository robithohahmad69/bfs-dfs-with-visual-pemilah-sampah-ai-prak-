from graph import get_graph_for_scenario, SCENARIO_DESCRIPTIONS

from dfs import dfs
from heuristic import greedy_bfs, astar, heuristic as HEURISTIC


def get_scenario():
    print("\n" + "=" * 55)
    print("       Simulasi Pemilahan Sampah Plastik")
    print("=" * 55)

    print("\n=== PILIH SKENARIO ===")
    print("\n-- Lintasan Berhasil --")
    for k in ["1", "2", "3", "4", "5", "6"]:
        print(f"  {k}. {SCENARIO_DESCRIPTIONS[k]}")

    print("\n-- Lintasan Gagal --")
    for k in ["7", "8", "9", "10"]:
        print(f" {k}. {SCENARIO_DESCRIPTIONS[k]}")

    pilihan = input("\nMasukkan pilihan (1-10): ").strip()

    if pilihan not in SCENARIO_DESCRIPTIONS:
        print("Input tidak valid.")
        return None

    return pilihan


def status_akhir(path):
    if not path:
        return "Tidak ditemukan"
    last = path[-1]
    if last == "T":
        return "BERHASIL (Grade Terbaik)"
    elif last == "G":
        return "GAGAL (Grade Rendah / Kontaminasi)"
    elif last == "J":
        return "GAGAL (Residu / Sampah)"
    return f"Berhenti di {last}"


def tabel_heuristik(nama, path, show_f=False):
    if not path:
        return

    NODE_NAMES = {
        "M": "Sampah Masuk",       "A": "Sorting Manual",
        "B": "Bersih Label",       "C": "Pencacahan",
        "D": "Pencucian Massal",   "E": "Pisah Jenis",
        "F": "Pengeringan",        "H": "Peletisasi",
        "T": "Grade Terbaik",      "G": "Grade Rendah",
        "I": "Degradasi Polimer",  "J": "Residu/Sampah",
    }

    print(f"\n-- Detail {nama} --")
    if show_f:
        print(f"  {'Node':<6} {'Nama':<25} {'g(n)':<6} {'h(n)':<6} {'f(n)'}")
        print(f"  {'-'*50}")
    else:
        print(f"  {'Node':<6} {'Nama':<25} {'g(n)':<6} {'h(n)'}")
        print(f"  {'-'*43}")

    for i, node in enumerate(path):
        g     = i
        h_val = HEURISTIC.get(node, 99)
        h_str = "inf" if h_val == 99 else str(h_val)
        f_str = "inf" if h_val == 99 else str(g + h_val)
        nama_node = NODE_NAMES.get(node, node)

        if show_f:
            print(f"  {node:<6} {nama_node:<25} {g:<6} {h_str:<6} {f_str}")
        else:
            print(f"  {node:<6} {nama_node:<25} {g:<6} {h_str}")

    if show_f:
        print("  g=langkah nyata | h=estimasi ke T | f=g+h (prioritas A*)")
    else:
        print("  g=langkah nyata | h=estimasi ke T (prioritas Greedy)")


def run():
    scenario_id = get_scenario()
    if not scenario_id:
        return

    print(f"\nSkenario: {SCENARIO_DESCRIPTIONS[scenario_id]}")

    graph = get_graph_for_scenario(scenario_id)
    start = "M"

    # Jalankan semua algoritma
  
    dfs_path    = dfs(graph, start)
    greedy_path = greedy_bfs(graph, start)
    astar_path  = astar(graph, start)

    # Hitung jumlah langkah
  
    dfs_steps    = len(dfs_path)    - 1 if dfs_path    else None
    greedy_steps = len(greedy_path) - 1 if greedy_path else None
    astar_steps  = len(astar_path)  - 1 if astar_path  else None

    # Tabel hasil
    print("\n" + "=" * 65)
    print("                      HASIL")
    print("=" * 65)
    print(f"\n  {'Algoritma':<10} {'Path':<35} {'Steps'}")
    print(f"  {'-'*55}")

    for nama, path, steps in [
       
        ("DFS",    dfs_path,    dfs_steps),
        ("Greedy", greedy_path, greedy_steps),
        ("A*",     astar_path,  astar_steps),
    ]:
        path_str  = " -> ".join(path) if path else "-"
        steps_str = str(steps) if steps is not None else "-"
        print(f"  {nama:<10} {path_str:<35} {steps_str}")

    # Status tiap algoritma
    print(f"\n  {'Algoritma':<10} {'Status'}")
    print(f"  {'-'*55}")
    for nama, path in [ ("DFS", dfs_path),
                       ("Greedy", greedy_path), ("A*", astar_path)]:
        print(f"  {nama:<10} {status_akhir(path)}")

    # Detail heuristik Greedy & A*
    tabel_heuristik("Greedy", greedy_path, show_f=False)
    tabel_heuristik("A*",     astar_path,  show_f=True)

    print("\n" + "=" * 65)

    lagi = input("\nJalankan lagi? (y/n): ").strip().lower()
    if lagi == "y":
        run()
    else:
        print("\nProgram selesai.\n")


if __name__ == "__main__":
    run()