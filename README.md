# Tugas: Analisis & Desain Algoritma Sorting Lanjutan + Binary Tree

> **Mata Kuliah:** Analisis & Desain Algoritma  
> **Topik:** Sorting Lanjutan (Bab 12) + Binary Tree & Heap (Bab 13)

---

## Struktur Repository

```
.
├── advanced_sorter.py      # Implementasi AdvancedSorter (Bagian 1)
├── expr_heap_sorter.py     # Implementasi ExprHeapSorter (Bagian 2)
├── jawaban_teori.md        # Jawaban analisis teori (semua pertanyaan a–d)
└── README.md               # Dokumentasi ini
```

---

## Bagian 1 — `advanced_sorter.py`

### Deskripsi

Modul `AdvancedSorter` mengurutkan dua struktur data berbeda menggunakan teknik yang dibahas di Bab 12, dengan batasan memori ketat dan tanpa fungsi bawaan Python (`list.sort()`, `sorted()`, `slice[:]`).

### Algoritma yang Diimplementasikan

#### 1. Array Merge Sort — `sort_array()`

**Teknik:** Virtual sublists + single `tmpArray`

```python
sorter = AdvancedSorter()
result = sorter.sort_array([5, 3, 8, 1, 9, 2, 7, 4, 6])
# → [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

- Hanya satu `tmpArray` berukuran n dialokasikan **sekali** di awal.
- Rekursi bekerja dengan indeks (`first`, `mid`, `last`) tanpa membuat sublist fisik.
- `_merge_virtual()` menggunakan `<=` untuk **stabilitas**: elemen kiri diprioritaskan bila nilai sama.
- **Kompleksitas:** Waktu O(n log n), Ruang ekstra O(n).

#### 2. Linked List Merge Sort — `sort_linked_list()`

**Teknik:** Fast-slow pointer + dummy node merge

```python
head = list_to_linked([5, 3, 8, 1, 9, 2])
sorted_head = sorter.sort_linked_list(head)
# → 1 → 2 → 3 → 5 → 8 → 9
```

- `_split_linked_list()`: `midPoint` bergerak 1 langkah, `curNode` 2 langkah — titik tengah ditemukan dalam **satu traversal** tanpa menghitung panjang.
- `_merge_linked_lists()`: dummy node statis + `tail` reference — hanya memodifikasi `.next`, **tanpa alokasi node baru**.
- **Stabilitas** terjaga (`<=` saat merge).
- **Kompleksitas:** Waktu O(n log n), Ruang O(log n) hanya untuk stack rekursi.

#### 3. Quick Sort — `sort_array_quicksort()` + `partition_quick()`

**Teknik:** Median-of-Three pivot + fallback ke Merge Sort

```python
result = sorter.sort_array_quicksort([9, 8, 7, 6, 5, 4, 3, 2, 1])
# → [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

- Pivot dipilih sebagai **median dari `arr[first]`, `arr[mid]`, `arr[last]`** — menghindari O(n²) pada data terurut.
- Jika kedalaman rekursi melebihi `2 × log₂(n)`, otomatis **fallback ke Merge Sort**.
- **Kompleksitas:** Waktu O(n log n) rata-rata, Ruang O(log n) stack.

### Batasan yang Dipenuhi

| Persyaratan | Status |
|---|---|
| Tidak menggunakan `list.sort()` / `sorted()` | ✅ |
| Tidak menggunakan `slice[:]` untuk pemisahan | ✅ |
| Array sort: hanya satu `tmpArray` | ✅ |
| Linked list: hanya modifikasi pointer `.next` | ✅ |
| Stabilitas wajib untuk Merge Sort | ✅ |
| Quick Sort fallback jika depth > 2·log₂(n) | ✅ |

---

## Bagian 2 — `expr_heap_sorter.py`

### Deskripsi

Modul `ExprHeapSorter` menggabungkan tiga komponen dari Bab 13: Expression Tree, In-Place Heapsort, dan Complete Tree Validator.

### Komponen yang Diimplementasikan

#### 1. Expression Tree Builder & Evaluator — `parse_and_evaluate()`

```python
sorter = ExprHeapSorter("((8 * 5) + (9 / (7 - 4)))")
result = sorter.parse_and_evaluate()
# Evaluasi: (8×5) + (9÷(7-4)) = 40 + 3 = 43
```

- `_tokenize()`: tokenisasi manual mendukung bilangan bulat multi-digit.
- `_build_tree()`: rekursi berbasis antrian token (`deque`) mengikuti pola `( kiri OP kanan )`.
- `_eval_tree()`: evaluasi **postorder** — kiri → kanan → root.
- Menangani **pembagian nol** (`raise ValueError`) dan **token tidak valid**.

#### 2. In-Place Heapsort — `heapsort_inplace()`

```python
sorter = ExprHeapSorter("(1+1)")
result = sorter.heapsort_inplace([5, 3, 8, 1, 9, 2])
# → [1, 2, 3, 5, 8, 9]
```

**Fase 1 — Build max-heap (bottom-up):**
```
for i in range(n//2 - 1, -1, -1):
    sift_down(arr, n, i)
```
Mulai dari node non-leaf terakhir ke root → O(n).

**Fase 2 — Extract & sort:**
```
for end in range(n-1, 0, -1):
    swap(arr[0], arr[end])
    sift_down(arr, end, 0)
```
→ O(n log n).

- `_sift_down()` menggunakan `left = 2*idx+1`, `right = 2*idx+2`.
- **Benar-benar in-place**: hanya variabel indeks, **tanpa array tambahan**.

#### 3. Complete Tree Validator — `is_complete_tree()`

```python
sorter.is_complete_tree([1, 2, 3, 4, 5, 6, 7])  # → True
```

Memeriksa bahwa tidak ada "lubang" pada pemetaan array ke struktur heap: jika ditemukan node tanpa anak kiri, semua node setelahnya harus tidak ada.

#### 4. Full Pipeline — `run_pipeline()`

```python
sorter = ExprHeapSorter("((8 * 5) + (9 / (7 - 4)))")
hasil = sorter.run_pipeline(extra_values=[12, 7, 25, 3, 18, 9, 1])
# expr_value: 43
# data_sorted: [1, 3, 7, 9, 12, 18, 25, 43]
# is_complete: True
```

### Batasan yang Dipenuhi

| Persyaratan | Status |
|---|---|
| Tidak menggunakan `list.sort()` / `sorted()` / `heapq` | ✅ |
| Expression Tree dibangun dengan antrian token + rekursi | ✅ |
| Heap & Sort benar-benar in-place | ✅ |
| Penanganan pembagian nol & token tidak valid | ✅ |
| Validasi complete binary tree via rumus indeks array | ✅ |

---

## Cara Menjalankan

### Prasyarat

Python 3.7+ (tidak ada dependensi eksternal).

### Menjalankan Test

```bash
# Bagian 1: Sorting
python advanced_sorter.py

# Bagian 2: Expression Tree + Heap
python expr_heap_sorter.py
```

### Contoh Output

```
============================================================
1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
============================================================
  ✓ PASS  Input: [5, 3, 8, 1, 9, 2, 7, 4]...
         Output: [1, 2, 3, 4, 5, 6, 7, 8]...
  ✓ PASS  Input: [3, 3, 1, 1, 2, 2]
         Output: [1, 1, 2, 2, 3, 3]
...

============================================================
5. FULL PIPELINE
============================================================
  Hasil evaluasi ekspresi '((8 * 5) + (9 / (7 - 4)))' = 43
  Data sebelum sort: [43, 12, 7, 25, 3, 18, 9, 1]
  Data setelah sort: [1, 3, 7, 9, 12, 18, 25, 43]
  Apakah complete binary tree? True
```

---

## Jawaban Teori

Lihat file [`jawaban_teori.md`](jawaban_teori.md) untuk jawaban lengkap semua pertanyaan analisis:

- **Bagian 1a** — Mengapa Radix Sort melanggar O(1); mekanisme tmpArray; alternatif in-place radix
- **Bagian 1b** — Fast-slow pointer; dummy node merge; kompleksitas ruang O(log n)
- **Bagian 1c** — Worst-case Quick Sort O(n²); strategi Median-of-Three; kelayakan di linked list
- **Bagian 1d** — Lower bound Ω(n log n) vs Radix Sort O(dn); asumsi domain kunci
- **Bagian 2a** — Langkah `_buildTree()`; postorder vs inorder; kedalaman stack rekursi
- **Bagian 2b** — Rumus indeks heap; `sift_down()`; jumlah perbandingan maksimum
- **Bagian 2c** — Simple vs in-place heapsort: ruang, cache locality, overflow risk
- **Bagian 2d** — Heapsort dan lower bound; properti null link decision tree; rekursif vs iteratif

---

## Ringkasan Kompleksitas

| Algoritma | Waktu | Ruang Ekstra | Stable |
|---|---|---|---|
| Array Merge Sort | O(n log n) | O(n) — satu tmpArray | ✅ Ya |
| Linked List Merge Sort | O(n log n) | O(log n) — stack | ✅ Ya |
| Quick Sort (Median-3) | O(n log n) avg | O(log n) — stack | ❌ Tidak |
| In-Place Heapsort | O(n log n) | O(1) | ❌ Tidak |
| Expression Tree Build | O(n) | O(h) — stack | — |
| Sift-Down | O(log n) | O(1) | — |
