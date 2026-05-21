# Jawaban Analisis Teori — Sorting Lanjutan & Binary Tree

---

## BAGIAN 1: Analisis & Desain Algoritma Sorting Lanjutan

---

### a. Ruang & Distribusi Sort

**Mengapa Radix Sort standar (array of 10 queues) tidak memenuhi batasan O(1)?**

Radix Sort standar mengalokasikan 10 antrian (bucket) untuk setiap digit. Pada implementasi berbasis array/linked-list, setiap bucket berpotensi menampung hingga seluruh n elemen. Total ruang yang dibutuhkan adalah O(n + k) di mana k = 10 (basis desimal), sehingga **overhead memori ekstra menjadi O(n)** — melanggar batasan O(1) Modul A.

**Bagaimana `tmpArray` tunggal pada Improved Merge Sort menekan overhead?**

Versi berbasis *slice* (`arr[first:mid+1]`) membuat salinan fisik subarray baru di setiap level rekursi. Pada kedalaman rekursi log₂(n), total memori yang terpakai bisa mencapai O(n log n) dalam kasus terburuk (semua salinan aktif bersamaan di stack).

`tmpArray` tunggal berukuran n dialokasikan **sekali** di awal `sort_array()`. Setiap panggilan `_merge_virtual()` meminjam rentang `tmpArray[left_start..right_end]` hanya untuk durasi merge tersebut, lalu hasilnya langsung disalin kembali ke `arr`. Tidak pernah ada lebih dari satu "salinan" aktif di `tmpArray` pada saat yang sama — overhead ruang tambahan tetap **O(n)** konstan (satu array ekstra berukuran n).

**Strategi Radix Sort tanpa melanggar O(1):**

Strategi paling realistis adalah **American Flag Sort** (in-place radix sort): alih-alih mendistribusikan ke bucket terpisah, algoritma ini menghitung histogram distribusi digit terlebih dahulu (O(k) ruang, k = 10 untuk desimal), lalu melakukan permutasi in-place berdasarkan histogram tersebut. Setiap digit membutuhkan satu pass O(n), sehingga kompleksitas waktu tetap **O(d·n)** tetapi ruang ekstra menjadi **O(k) = O(1)** (konstanta 10 bucket). Kelemahannya: implementasi lebih kompleks dan konstanta waktu lebih besar dibanding Radix Sort standar.

---

### b. Linked List & Pointer Manipulation

**Bagaimana `_splitLinkedList()` menemukan titik tengah dalam satu traversal?**

Fungsi ini menggunakan teknik **fast-slow pointer**:
- `midPoint` (`slow`) bergerak **1 langkah** per iterasi.
- `curNode` (`fast`) bergerak **2 langkah** per iterasi.

Kondisi loop: `while curNode is not None and curNode.next is not None`.

Ketika `curNode` mencapai akhir list (panjang n), `midPoint` telah berjalan n/2 langkah — tepat di titik tengah. Tidak perlu menghitung panjang list secara terpisah. Setelah loop, `right_head = midPoint.next` dan `midPoint.next = None` memutus list menjadi dua bagian.

**Mengapa dummy node + tail reference memungkinkan merge tanpa alokasi memori?**

Pendekatan konvensional tanpa dummy node memerlukan penanganan khusus untuk node pertama (kasus edge), yang sering memaksa alokasi node baru sebagai "head sementara". Dengan **dummy node statis**:

```
dummy (sentinel) → [node hasil merge] → [node hasil merge] → ...
tail selalu menunjuk ke ujung terakhir list hasil
```

Operasi `tail.next = listA` (atau `listB`) hanya **memodifikasi pointer `.next`** yang sudah ada — tidak membuat node baru. `dummy` sendiri adalah satu node statis (bukan alokasi baru per elemen). Setelah merge selesai, `dummy.next` adalah head list hasil.

Karena tidak ada alokasi node baru, **ruang ekstra untuk merge = O(1)**. Satu-satunya overhead ruang adalah stack rekursi yang berkedalaman log₂(n) level, sehingga **total kompleksitas ruang = O(log n)**.

---

### c. Quick Sort Worst-Case & Pivot Strategy

**Bagaimana pivot naif menyebabkan O(n) rekursi pada data descending?**

Pada implementasi standar dengan pivot = elemen pertama (`arr[first]`), dan input sudah terurut menurun `[n, n-1, ..., 2, 1]`:

- Pivot selalu menjadi elemen **terbesar** di partisi saat itu.
- Setelah `partitionSeq()`, semua elemen lain berada di sublist kiri, sublist kanan kosong.
- Kedalaman rekursi: n → n-1 → n-2 → ... → 1, menghasilkan **O(n) level rekursi**.
- Total perbandingan: n + (n-1) + ... + 1 = **O(n²)**.

`left` bergerak dari `first+1` ke kanan dan tidak menemukan elemen yang perlu ditukar (semua < pivot yang merupakan elemen terbesar), sementara `right` langsung berhenti di `first+1`. Partisi tidak membagi array secara seimbang.

**Strategi Median-of-Three:**

Pilih pivot sebagai **median dari `arr[first]`, `arr[mid]`, `arr[last]``. Pada data descending, median adalah elemen tengah (sekitar nilai n/2), yang membagi array menjadi dua bagian yang hampir sama besar → kedalaman rekursi menjadi **O(log n)** → kompleksitas waktu **O(n log n)** rata-rata.

**Kelayakan pada singly linked list:**

Pada singly linked list, akses ke elemen tengah membutuhkan traversal O(n). Untuk median-of-three, kita perlu `arr[first]` (O(1)), `arr[mid]` (O(n)), dan `arr[last]` (O(n)) — **total O(n) hanya untuk memilih pivot**. Biaya ini ditambahkan ke setiap level rekursi sehingga overhead lebih besar. Strategi yang lebih cocok untuk linked list adalah **Merge Sort** (seperti Modul B), yang tidak memerlukan akses acak dan memiliki kompleksitas O(n log n) terlepas dari distribusi data.

---

### d. Batas Teoretis & Paradigma Sorting

**Mengapa Radix Sort O(dn) tidak kontradiktif dengan lower bound Ω(n log n)?**

Lower bound Ω(n log n) berlaku khusus untuk **comparison-based sorting** — algoritma yang hanya menentukan urutan melalui operasi perbandingan `<`, `>`, `=` antara dua elemen. Bukti formal menggunakan *decision tree*: setiap algoritma comparison sort adalah pohon biner dengan n! leaf (semua permutasi), sehingga tinggi pohon ≥ log₂(n!) ≈ n log n.

Radix Sort **tidak melakukan perbandingan langsung antar elemen**. Ia mengekstraksi digit dan mendistribusikan elemen ke bucket — operasi yang tidak termasuk dalam model komputasi comparison sort. Oleh karena itu, lower bound Ω(n log n) **tidak berlaku** untuk Radix Sort.

**Dua asumsi implisit yang membuat Radix Sort "melampaui" batas comparison sort:**

1. **Kunci memiliki representasi digit dengan panjang tetap d**: Radix Sort berasumsi bahwa setiap kunci dapat dipecah menjadi d digit dalam basis k. Kompleksitas O(dn) hanya lebih baik dari O(n log n) jika `d` bersifat konstan atau sangat kecil. Jika kunci berupa bilangan bulat tak terbatas (d tumbuh dengan n, misalnya d = log n), maka O(d·n) = O(n log n) — tidak ada keunggulan.

2. **Nilai kunci terbatas dalam rentang [0, k^d - 1]**: Bucket/counting sort yang digunakan tiap pass membutuhkan O(k) ruang dan O(n + k) waktu. Jika k sangat besar (basis yang besar atau kunci dengan domain tak terbatas), overhead O(k) mendominasi dan keunggulan linear hilang. Asumsi ini membatasi Radix Sort hanya efektif pada domain kunci yang terdefinisi dan terbatas.

---

## BAGIAN 2: Teori & Analisis Algoritma Binary Tree

---

### a. Pohon Ekspresi & Traversal

**Langkah-langkah `_buildTree()` untuk `((8 * 5) + (9 / (7 - 4)))`:**

Token: `( ( 8 * 5 ) + ( 9 / ( 7 - 4 ) ) )`

```
1. Ambil '(' → masuk ke cabang sub-ekspresi
2. Rekursi kiri:
   a. Ambil '(' → masuk sub-ekspresi
   b. Rekursi kiri: ambil '8' → leaf node {val:8}
   c. Ambil '*' → operator
   d. Rekursi kanan: ambil '5' → leaf node {val:5}
   e. Ambil ')' → selesai → node {val:'*', left:{8}, right:{5}}
3. Ambil '+' → operator root
4. Rekursi kanan:
   a. Ambil '(' → sub-ekspresi
   b. Rekursi kiri: ambil '9' → leaf node {val:9}
   c. Ambil '/' → operator
   d. Rekursi kanan:
      i.  Ambil '(' → sub-ekspresi
      ii. Rekursi kiri: ambil '7' → leaf node {val:7}
      iii.Ambil '-' → operator
      iv. Rekursi kanan: ambil '4' → leaf node {val:4}
      v.  Ambil ')' → node {val:'-', left:{7}, right:{4}}
   e. Ambil ')' → node {val:'/', left:{9}, right:{'-'}}
5. Ambil ')' → root {val:'+', left:{'*'}, right:{'/'}}
```

Pohon hasil:
```
        +
       / \
      *    /
     / \  / \
    8   5 9   -
             / \
            7   4
```

**Mengapa postorder menghasilkan notasi postfix valid, sedangkan inorder perlu tanda kurung?**

- **Postorder** (kiri → kanan → root): menghasilkan `8 5 * 9 7 4 - / +` — notasi postfix yang valid. Setiap operator muncul setelah kedua operandnya sehingga evaluasi stack bisa dilakukan tanpa ambiguitas atau tanda kurung.
- **Inorder** (kiri → root → kanan): menghasilkan `8 * 5 + 9 / 7 - 4` yang ambigu karena tidak mencerminkan prioritas dan asosiativitas. Tanda kurung eksplisit diperlukan untuk menghasilkan `((8 * 5) + (9 / (7 - 4)))` yang benar.

**Kedalaman stack rekursi `_buildString()` untuk pohon tinggi h:**

Setiap panggilan rekursif `_buildString(node)` memanggil diri sendiri untuk `node.left` dan `node.right` sebelum kembali. Kedalaman rekursi maksimum sama dengan **tinggi pohon h**, sehingga stack rekursi mencapai **O(h) frame**. Untuk pohon seimbang dengan n node, h = O(log n), sehingga stack = O(log n).

---

### b. Struktur Heap & Pemetaan Array

**Mengapa rumus indeks hanya valid untuk complete binary tree?**

Rumus `parent = (i-1)//2`, `left = 2i+1`, `right = 2i+2` mengasumsikan **pemetaan level-order yang kontinu** — elemen pada array index i adalah node pada posisi i dalam urutan BFS. Ini hanya terjaga jika setiap level terisi penuh (kecuali mungkin level terakhir yang rapat ke kiri). Pada pohon non-complete, akan ada "lubang" sehingga rumus indeks menunjuk ke node yang salah atau tidak ada.

**Bagaimana `sift_down()` memulihkan heap order setelah ekstraksi akar?**

1. Ekstrak root (elemen terbesar) → swap dengan elemen terakhir heap.
2. Kurangi `heap_size` satu.
3. `sift_down(arr, heap_size, 0)`: node baru di root dibandingkan dengan kedua anaknya.
4. Jika ada anak yang lebih besar, swap dengan anak terbesar.
5. Turun ke posisi baru, ulangi hingga tidak ada anak yang lebih besar atau mencapai daun.

**Jumlah perbandingan maksimum dalam satu `sift_down()` untuk heap ukuran n:**

Setiap level melakukan 2 perbandingan (bandingkan dengan anak kiri dan kanan). Tinggi heap = ⌊log₂(n)⌋. Sehingga jumlah perbandingan maksimum = **2 × ⌊log₂(n)⌋ = O(log n)**.

---

### c. Heapsort In-Place vs Simple

| Aspek | Simple Heapsort | In-Place Heapsort |
|---|---|---|
| **Ruang tambahan** | O(n) — membutuhkan array terpisah untuk menyimpan elemen yang diekstraksi | O(1) — swap dilakukan dalam array yang sama; hanya variabel indeks |
| **Pola akses memori** | Lebih baik untuk cache pada fase build (akses lokal ke array heap), tapi fase extract ke array lain menyebabkan cache miss | Akses non-lokal: swap root ke akhir array dan sift-down menyebabkan lompatan jauh dalam memori → cache miss lebih sering |
| **Risiko overflow** | Berisiko tinggi pada sistem RAM terbatas karena membutuhkan satu array ekstra berukuran n | Tidak ada risiko overflow tambahan; seluruh operasi dalam satu array input |

**Mengapa in-place heapsort tetap O(n log n)?**

- **Fase build-heap**: n/2 panggilan `sift_down()`, masing-masing O(log n) → O(n log n). Namun secara amortized, fase ini sebenarnya O(n).
- **Fase extract**: n-1 swap + n-1 panggilan `sift_down()`, masing-masing O(log n) → O(n log n).
- Swap tambahan antara root dan akhir adalah operasi O(1) yang tidak mengubah orde kompleksitas.
- Total: O(n log n) terlepas dari jumlah swap.

---

### d. Batas Teoretis & Decision Tree

**Mengapa heapsort tidak melanggar lower bound Ω(n log n)?**

Heapsort adalah **comparison-based sorting** — ia hanya menentukan urutan melalui perbandingan `arr[left] > arr[largest]` dll. Lower bound Ω(n log n) memang berlaku untuknya, dan heapsort memenuhi batas itu secara tepat dengan kompleksitas Θ(n log n). Heapsort tidak "melampaui" batas, melainkan mencapainya secara optimal.

**Properti null link pada decision tree Morse Code:**

Dalam pohon keputusan decoding Morse Code, setiap cabang kiri = titik (`.`) dan kanan = garis (`-`). Node internal memiliki nilai karakter; null link menandakan bahwa urutan titik/garis tertentu **tidak valid** (tidak ada karakter Morse untuk sekuens tersebut). Saat traversal mencapai null link sebelum sekuens habis, atau sekuens habis di node null → **urutan token tidak valid terdeteksi**.

**Mengapa rekursif lebih cocok daripada iteratif untuk pohon keputusan:**

Pohon keputusan memiliki struktur hierarkis alami yang cocok dengan rekursi. Setiap pemanggilan rekursif menangani satu subtree secara independen, dan kondisi berhenti (node null atau leaf) terjadi secara natural. Implementasi iteratif memerlukan stack eksplisit untuk mensimulasikan rekursi — menambah kompleksitas kode tanpa manfaat algoritmik yang signifikan. Selain itu, kedalaman pohon Morse (≤ 4-7 level) tidak menimbulkan risiko stack overflow, sehingga rekursi lebih aman dan lebih mudah dibaca.
