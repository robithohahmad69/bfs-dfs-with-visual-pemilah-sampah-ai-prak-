# ♻️ Simulasi Pemilahan Sampah Plastik — BFS, DFS, Greedy & A*

Proyek simulasi proses daur ulang sampah plastik menggunakan algoritma pencarian graf:
**BFS**, **DFS**, **Greedy Best-First Search**, dan **A\* Search**.
Dibangun dengan **Python (Flask)** di backend dan **vis.js** di frontend untuk visualisasi graf interaktif.

---

## 📌 Deskripsi Proyek

Proyek ini memodelkan alur pengolahan sampah plastik sebagai **State Space Graph**, di mana:

- Setiap **node** merepresentasikan tahapan proses atau kondisi akhir
- Setiap **edge** merepresentasikan transisi antar tahapan
- **Node awal (M)** = Sampah Plastik Campuran masuk
- **Node tujuan (T)** = Biji Plastik Grade Terbaik (Food Grade)

Pengguna memilih skenario kondisi awal sampah, kemudian menjalankan salah satu dari 4 algoritma untuk melihat jalur proses yang ditempuh beserta analisisnya.

---

## 🗺️ Peta Node (Keadaan)

| Node | Nama | Keterangan |
|------|------|------------|
| **M** | Sampah Masuk | Titik awal — sampah plastik campuran masuk |
| **A** | Sorting Manual | Pemilahan berdasarkan jenis plastik |
| **B** | Bersihkan Label | Pembersihan label dan tutup botol |
| **C** | Pencacahan | Proses crushing / shredding plastik |
| **D** | Pencucian Massal | Pencucian kimia / panas skala besar |
| **E** | Pisah Jenis | Pemisahan massa jenis (Sink-Float) |
| **F** | Pengeringan | Proses pengeringan sebelum ekstrusi |
| **H** | Peletisasi | Ekstrusi dan pembentukan biji plastik |
| **T** | ✅ Grade Terbaik | **Tujuan** — Biji plastik food grade |
| **G** | ❌ Grade Rendah | Gagal — kontaminasi tidak teratasi |
| **I** | ❌ Degradasi | Gagal — polimer rusak / rapuh |
| **J** | ❌ Residu | Gagal — sampah tak terolah |

---

## 🛣️ Jalur yang Tersedia

### ✅ Jalur Berhasil (mencapai T)

| # | Jalur | Keterangan |
|---|-------|------------|
| 1 | `M → A → B → C → E → H → T` | Jalur lengkap dan standar |
| 2 | `M → D → C → E → H → T` | Jalur alternatif — sampah relatif seragam |
| 3 | `M → A → C → E → T` | Jalur pendek — plastik sudah tersortir rapi |

### ❌ Jalur Gagal (tidak mencapai T)

| # | Jalur | Penyebab |
|---|-------|----------|
| 4 | `M → A → B → C → E → F → G` | Kontaminasi zat kimia ditemukan saat pengeringan |
| 5 | `M → D → C → E → I → J` | Polimer asing menyebabkan degradasi |
| 6 | `M → D → I → J` | Plastik terlalu rusak sejak awal masuk |

---

## 🎛️ Skenario Input

| Skenario | Kondisi Awal | Jalur yang Ditempuh |
|----------|-------------|---------------------|
| 1 | Plastik campuran belum disortir | M-A-B-C-E-H-T |
| 2 | Plastik seragam, siap cuci massal | M-D-C-E-H-T |
| 3 | Plastik sudah tersortir rapi | M-A-C-E-T |
| 4 | Tersortir, ada indikasi zat kimia | M-A-B-C-E-F-G |
| 5 | Cuci massal, polimer asing belum terdeteksi | M-D-C-E-I-J |
| 6 | Plastik terlihat rusak parah sejak awal | M-D-I-J |

---

## 🧠 Algoritma yang Digunakan

### 1. BFS — Breadth-First Search
- **Struktur data:** Queue (FIFO)
- **Cara kerja:** Telusuri semua node level per level sebelum masuk lebih dalam
- **Keunggulan:** Menjamin jalur dengan jumlah langkah paling sedikit
- **Kompleksitas:** Waktu O(V+E), Ruang O(V)

### 2. DFS — Depth-First Search
- **Struktur data:** Stack / Rekursi (LIFO)
- **Cara kerja:** Masuk sedalam mungkin ke satu jalur, backtrack jika buntu
- **Keunggulan:** Hemat memori dibanding BFS
- **Kompleksitas:** Waktu O(V+E), Ruang O(V)

### 3. Greedy Best-First Search
- **Struktur data:** Priority Queue berdasarkan `h(n)`
- **Cara kerja:** Selalu pilih node dengan estimasi paling dekat ke tujuan
- **Formula:** `prioritas = h(n)`
- **Keunggulan:** Lebih cepat dari BFS/DFS karena diarahkan heuristik
- **Kelemahan:** Tidak selalu menemukan jalur optimal

### 4. A\* Search
- **Struktur data:** Priority Queue berdasarkan `f(n) = g(n) + h(n)`
- **Cara kerja:** Kombinasi biaya nyata `g(n)` dan estimasi heuristik `h(n)`
- **Formula:** `f(n) = g(n) + h(n)`
- **Keunggulan:** Optimal dan efisien — terbaik dari keempat algoritma
- **Kompleksitas:** Waktu O(E log V), Ruang O(V)

### Nilai Heuristik `h(n)`

| Node | h(n) | Keterangan |
|------|------|------------|
| M | 5 | Estimasi 5 langkah ke T |
| A | 4 | |
| B, C, D | 3 | |
| E | 2 | |
| F | 3 | Mengarah ke buntu |
| H | 1 | Satu langkah ke T |
| T | 0 | Sudah di tujuan |
| G, I, J | 99 | Node buntu — tidak diprioritaskan |

---

## 🗂️ Struktur File

```
project/
│
├── app.py              # Flask server + routing API
├── graph.py            # Definisi graph & fungsi skenario
├── bfs.py              # Implementasi BFS
├── dfs.py              # Implementasi DFS
├── heuristic.py        # Implementasi Greedy & A*
├── requirements.txt    # Dependensi Python
│
└── templates/
    └── index.html      # UI interaktif (vis.js + vanilla JS)
```

---

## ⚙️ Instalasi & Cara Menjalankan

### 1. Clone repositori
```bash
git clone https://github.com/robithohahmad69/bfs-dfs-with-visual-pemilah-sampah-ai-prak-.git
cd bfs-dfs-with-visual-pemilah-sampah-ai-prak-
```

### 2. Install dependensi
```bash
pip install -r requirements.txt
```

### 3. Jalankan server
```bash
python app.py
```

### 4. Buka browser
```
http://127.0.0.1:5000
```

---

## 🖥️ Cara Menggunakan Aplikasi

1. **Pilih skenario** dari dropdown — setiap pilihan merepresentasikan kondisi awal sampah plastik yang berbeda
2. **Klik salah satu tombol algoritma** — BFS, DFS, Greedy, atau A\*
3. **Lihat visualisasi** — node pada graf akan di-highlight sesuai jalur yang ditemukan
   - 🟩 Hijau = BFS
   - 🟦 Biru = DFS
   - 🟧 Oranye = Greedy
   - 🟪 Ungu = A\*
   - 🔴 Merah = Node buntu / gagal
4. **Baca Hasil Analisis** — menampilkan status berhasil/gagal, rute lengkap, dan tabel nilai heuristik (khusus Greedy & A\*)
5. **Klik titik legend** — untuk membaca penjelasan lengkap tentang algoritma yang dipilih
6. **Hover titik legend** — untuk melihat deskripsi singkat algoritma

---

## 🔌 API Endpoint

### `POST /run`
Menjalankan BFS atau DFS.

**Request body:**
```json
{
  "pilihan": "1",
  "algo": "bfs"
}
```

**Response:**
```json
{
  "start": "M",
  "algo": "bfs",
  "path": ["M", "A", "B", "C", "E", "H", "T"]
}
```

---

### `POST /run_heuristic`
Menjalankan Greedy Best-First Search atau A\*.

**Request body:**
```json
{
  "pilihan": "1",
  "algo": "astar"
}
```

**Response:**
```json
{
  "start": "M",
  "algo": "astar",
  "path": ["M", "A", "B", "C", "E", "H", "T"]
}
```

---

## 📦 Dependensi

| Package | Kegunaan |
|---------|----------|
| Flask | Web framework Python |
| vis.js (CDN) | Visualisasi graf interaktif di browser |
| Google Fonts (CDN) | Font Poppins untuk UI |

Install Python dependencies:
```bash
pip install flask
```

---

## 👨‍💻 Dibuat Oleh

**Robit Hohah Mad** — Mahasiswa D4 Teknik Informatika  
Proyek Praktikum Kecerdasan Buatan — Simulasi Pemilahan Sampah Plastik menggunakan BFS, DFS, Greedy, dan A\*
