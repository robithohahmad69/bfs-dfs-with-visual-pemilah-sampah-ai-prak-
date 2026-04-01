# ============================================================
# DEFINISI NODE:
# M=Sampah Masuk, A=Sorting Manual, B=Bersih Label/Tutup,
# C=Pencacahan, D=Pencucian Kimia/Panas, E=Pemisahan Massa Jenis,
# F=Pengeringan, H=Ekstrusi/Peletisasi,
# T=Grade Terbaik (Goal),
# G=Gagal: Kontaminasi, I=Gagal: Degradasi, J=Gagal: Residu
# ============================================================

# ============================================================
# BASE GRAPH — semua koneksi yang mungkin ada
# ============================================================
BASE_GRAPH = {
    "M": ["A", "D"],
    "A": ["B", "C"],
    "B": ["C"],
    "C": ["E"],
    "D": ["C", "I"],
    "E": ["H", "F", "T"],   # E bisa ke H, F, atau langsung T
    "F": ["G"],
    "G": [],
    "H": ["T"],
    "I": ["J"],
    "J": [],
    "T": []
}


# ============================================================
# GRAPH PER SKENARIO
# Setiap skenario membatasi tetangga agar hanya menelusuri
# jalur yang relevan dengan kondisi yang digambarkan
# ============================================================
def get_graph_for_scenario(scenario_id):
    import copy
    base = copy.deepcopy(BASE_GRAPH)

    # ----------------------------------------------------------
    # SUCCESS PATHS
    # ----------------------------------------------------------

    if scenario_id == "1":
        # Lintasan: M-A-B-C-E-H-T
        # Kondisi: Plastik campuran, belum disortir, proses lengkap
        base["M"] = ["A"]
        base["A"] = ["B"]
        base["E"] = ["H"]
        # H → T sudah ada di base

    elif scenario_id == "2":
        # Lintasan: M-D-C-E-H-T
        # Kondisi: Plastik seragam, langsung cuci massal
        base["M"] = ["D"]
        base["D"] = ["C"]
        base["E"] = ["H"]

    elif scenario_id == "3":
        # Lintasan: M-A-C-E-T (lintasan pendek, hasil flakes)
        # Kondisi: Plastik sudah tersortir rapi, skip label bersih & peletisasi
        base["M"] = ["A"]
        base["A"] = ["C"]
        base["E"] = ["T"]   # langsung ke T (flakes bersih)

    elif scenario_id == "4":
        # Lintasan: M-A-B-C-E-T
        # Kondisi: Tersortir + bersih label, tapi skip peletisasi
        base["M"] = ["A"]
        base["A"] = ["B"]
        base["E"] = ["T"]

    elif scenario_id == "5":
        # Lintasan: M-A-C-E-H-T
        # Kondisi: Tersortir, langsung cacah, lalu peletisasi
        base["M"] = ["A"]
        base["A"] = ["C"]
        base["E"] = ["H"]

    elif scenario_id == "6":
        # Lintasan: M-D-C-E-T
        # Kondisi: Plastik seragam, cuci massal, langsung jadi grade terbaik
        base["M"] = ["D"]
        base["D"] = ["C"]
        base["E"] = ["T"]

    # ----------------------------------------------------------
    # DEAD-END / FAILURE PATHS
    # ----------------------------------------------------------

    elif scenario_id == "7":
        # Lintasan: M-A-B-C-E-F-G
        # Masalah: Kontaminasi ditemukan saat pengeringan → Grade Rendah
        base["M"] = ["A"]
        base["A"] = ["B"]
        base["E"] = ["F"]
        # F → G sudah ada di base

    elif scenario_id == "8":
        # Lintasan: M-D-C-E-F-G
        # Masalah: Tanpa sortir awal, kontaminan tersebar saat dicacah
        base["M"] = ["D"]
        base["D"] = ["C"]
        base["E"] = ["F"]

    elif scenario_id == "9":
        # Lintasan: M-A-C-E-F-G
        # Masalah: Skip label bersih, lem & kotoran ikut tercacah
        base["M"] = ["A"]
        base["A"] = ["C"]
        base["E"] = ["F"]

    elif scenario_id == "10":
        # Lintasan: M-D-I-J
        # Masalah: Plastik sudah rusak parah (UV exposure), hancur saat dicuci
        base["M"] = ["D"]
        base["D"] = ["I"]
        # I → J sudah ada di base

    return base


# ============================================================
# DESKRIPSI SKENARIO (untuk dropdown di frontend)
# ============================================================
SCENARIO_DESCRIPTIONS = {
    "1":  "✅ Skenario 1 — Proses Lengkap: Plastik campuran belum disortir, perlu semua tahapan dari awal hingga peletisasi.",
    "2":  "✅ Skenario 2 — Cuci Massal + Peletisasi: Plastik seragam jenis, langsung cuci tanpa sortir manual, lalu peletisasi.",
    "3":  "✅ Skenario 3 — Lintasan Pendek (Flakes): Plastik tersortir rapi, langsung cacah, hasil akhir berupa flakes bersih.",
    "4":  "✅ Skenario 4 — Sortir + Label Bersih (Flakes): Plastik tersortir dan dibersihkan labelnya, hasil akhir flakes tanpa peletisasi.",
    "5":  "✅ Skenario 5 — Sortir + Peletisasi: Plastik tersortir, langsung cacah lalu peletisasi tanpa pembersihan label.",
    "6":  "✅ Skenario 6 — Cuci Massal (Flakes): Plastik seragam, cuci massal, hasil akhir flakes langsung tanpa peletisasi.",
    "7":  "❌ Skenario 7 — Gagal: Kontaminasi Saat Pengeringan: Plastik tersortir & label bersih, tapi zat kimia tidak hilang saat dikeringkan.",
    "8":  "❌ Skenario 8 — Gagal: Kontaminan Tersebar Saat Cacah: Tanpa sortir awal, kontaminan ikut tercacah dan tidak bisa dipisahkan.",
    "9":  "❌ Skenario 9 — Gagal: Label & Lem Ikut Tercacah: Skip pembersihan label, kotoran ikut hancur dan mencemari hasil.",
    "10": "❌ Skenario 10 — Gagal: Plastik Rusak Parah (UV): Plastik sudah terdegradasi sejak awal, hancur saat dicuci.",
}