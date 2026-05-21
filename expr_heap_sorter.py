"""
expr_heap_sorter.py
===================
Implementasi ExprHeapSorter untuk tugas Teori & Analisis Algoritma Binary Tree.

Modul ini mengimplementasikan:
1. Expression Tree Builder & Evaluator — memparse ekspresi terparentheses penuh
2. In-Place Max-Heap Construction — tanpa alokasi array tambahan
3. Heapsort In-Place — ascending sort menggunakan sift-down
4. Complete Tree Validator — memeriksa properti complete binary tree

Semua implementasi TANPA list.sort(), sorted(), heapq, atau library eksternal.
"""

from typing import List, Optional
from collections import deque


class ExprHeapSorter:
    def __init__(self, expr_str: str):
        """
        Parameters
        ----------
        expr_str : str
            Ekspresi aritmetika terparentheses penuh, mis. "((8 * 5) + (9 / (7 - 4)))"
        """
        self.expr = expr_str
        self.values: List[int] = []

    # =========================================================
    # 1. EXPRESSION TREE BUILDER & EVALUATOR
    # =========================================================

    def parse_and_evaluate(self) -> List[int]:
        """
        Membangun pohon ekspresi dari self.expr, mengevaluasi nilainya,
        dan mengembalikan list berisi nilai hasil evaluasi (single-element list
        agar konsisten dengan antarmuka heapsort).
        """
        # Tokenisasi: pisahkan string menjadi token (angka multi-digit, operator, tanda kurung)
        tokens = deque(self._tokenize(self.expr))
        root = self._build_tree(tokens)
        result = self._eval_tree(root)
        self.values = [result]
        return self.values

    def _tokenize(self, expr: str) -> List[str]:
        """
        Mengubah string ekspresi menjadi list token.
        Menangani bilangan bulat multi-digit dan spasi.
        """
        tokens = []
        i = 0
        while i < len(expr):
            ch = expr[i]
            if ch.isspace():
                i += 1
                continue
            if ch.isdigit():
                j = i
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                tokens.append(expr[i:j])
                i = j
            elif ch in '()+*/-':
                tokens.append(ch)
                i += 1
            else:
                raise ValueError(f"Token tidak valid: '{ch}'")
        return tokens

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """
        Membangun pohon ekspresi secara rekursif dari antrian token.

        Pola rekursi (untuk ekspresi terparentheses penuh):
          '('  → buat node operator
                  kiri  = _build_tree(tokens)
                  ambil operator
                  kanan = _build_tree(tokens)
                  ')'  diabaikan (dikonsumsi)
          digit → buat node operand (leaf)

        Setiap node direpresentasikan sebagai dict:
          {'val': operator/operand, 'left': node|None, 'right': node|None}
        """
        if not tokens:
            raise ValueError("Token habis sebelum ekspresi selesai diparse")

        token = tokens.popleft()

        if token == '(':
            # Sub-ekspresi: ( kiri OP kanan )
            left = self._build_tree(tokens)

            if not tokens:
                raise ValueError("Operator tidak ditemukan setelah operand kiri")
            operator = tokens.popleft()
            if operator not in ('+', '-', '*', '/'):
                raise ValueError(f"Operator tidak valid: '{operator}'")

            right = self._build_tree(tokens)

            # Konsumsi ')'
            if not tokens or tokens.popleft() != ')':
                raise ValueError("Tanda kurung tutup ')' tidak ditemukan")

            return {'val': operator, 'left': left, 'right': right}

        elif token.lstrip('-').isdigit():
            # Node daun (operand)
            return {'val': int(token), 'left': None, 'right': None}

        else:
            raise ValueError(f"Token tidak terduga: '{token}'")

    def _eval_tree(self, node: Optional[dict]) -> int:
        """
        Mengevaluasi pohon ekspresi secara postorder (kiri → kanan → root).
        Menangani pembagian nol dan operator tidak valid.

        Returns
        -------
        int
            Nilai numerik hasil evaluasi subtree/node ini.
        """
        if node is None:
            raise ValueError("Node kosong ditemukan saat evaluasi")

        # Node daun: kembalikan nilai langsung
        if node['left'] is None and node['right'] is None:
            return int(node['val'])

        # Evaluasi postorder
        left_val = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])

        op = node['val']
        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ValueError("Pembagian dengan nol tidak diizinkan")
            return left_val // right_val  # integer division
        else:
            raise ValueError(f"Operator tidak dikenal: '{op}'")

    # =========================================================
    # 2 & 3. IN-PLACE HEAPSORT
    # =========================================================

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """
        Mengurutkan array secara ascending menggunakan in-place heapsort.

        Fase 1 — Build max-heap:
          Mulai dari node non-leaf terakhir (index n//2 - 1) hingga root (index 0),
          panggil sift-down untuk membangun max-heap. O(n) total.

        Fase 2 — Extract & sort:
          Tukar root (elemen terbesar) dengan elemen terakhir heap,
          kurangi heap_size, sift-down dari root. Ulangi. O(n log n) total.

        Kompleksitas ruang: O(1) — hanya variabel indeks & counter.
        Catatan: heapsort inherently TIDAK stable.
        """
        n = len(arr)
        if n <= 1:
            return arr

        # Fase 1: Build max-heap in-place (bottom-up)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # Fase 2: Extract max berulang kali
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]  # swap root ke akhir
            self._sift_down(arr, end, 0)          # restore heap property

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """
        Memulihkan heap order property dengan mendorong elemen di idx ke bawah.

        Algoritma:
        1. Hitung indeks anak kiri (left = 2*idx+1) dan kanan (right = 2*idx+2).
        2. Temukan indeks elemen terbesar di antara idx, left, right.
        3. Jika largest != idx, tukar dan lanjutkan sift-down dari posisi baru.

        Jumlah perbandingan maksimum: 2 * floor(log2(n)) karena tinggi heap = floor(log2(n)).
        """
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < heap_size and arr[left] > arr[largest]:
                largest = left
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            if largest == idx:
                break  # Heap property terpenuhi

            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest  # Turun ke posisi baru (iteratif, bukan rekursif)

    # =========================================================
    # 4. COMPLETE TREE VALIDATOR
    # =========================================================

    def is_complete_tree(self, arr: List[int]) -> bool:
        """
        Memvalidasi apakah array memenuhi properti complete binary tree
        ketika dipetakan ke struktur heap berbasis array.

        Properti complete binary tree:
        - Semua level terisi penuh kecuali mungkin level terakhir.
        - Node pada level terakhir rapat ke kiri.

        Untuk array 0-indexed dengan n elemen:
        - Jika node i ada (i < n), dan 2*i+1 >= n, maka tidak boleh ada node
          di indeks mana pun setelah itu yang bernilai "ada" (tidak ada lubang).

        Implementasi: cari indeks pertama anak yang tidak ada; semua indeks
        setelah itu di array juga harus tidak ada. Jika ada indeks setelah
        "lubang" pertama yang masih terisi → bukan complete tree.
        """
        n = len(arr)
        if n == 0:
            return True

        # Temukan apakah ada "lubang" — node tanpa anak kiri tapi ada node lain setelahnya
        found_gap = False
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2

            if left >= n:
                # Node i tidak punya anak kiri → semua node setelah i harus kosong
                found_gap = True
            elif found_gap:
                # Ada node yang seharusnya kosong tapi ternyata ada → bukan complete
                return False

            if right >= n:
                # Node i tidak punya anak kanan (boleh, tapi tandai gap)
                found_gap = True
            elif found_gap:
                return False

        return True

    # =========================================================
    # Pipeline lengkap: parse → heap → sort → validate
    # =========================================================

    def run_pipeline(self, extra_values: List[int] = None) -> dict:
        """
        Menjalankan seluruh pipeline:
        1. Parse & evaluasi ekspresi
        2. Gabungkan dengan extra_values (opsional)
        3. Heapsort in-place
        4. Validasi complete tree

        Returns
        -------
        dict berisi semua hasil intermediate.
        """
        eval_result = self.parse_and_evaluate()
        print(f"  Hasil evaluasi ekspresi '{self.expr}' = {eval_result[0]}")

        data = eval_result[:]
        if extra_values:
            data.extend(extra_values)

        print(f"  Data sebelum sort: {data}")

        sorted_data = self.heapsort_inplace(data[:])  # sort salinan
        print(f"  Data setelah sort: {sorted_data}")

        is_complete = self.is_complete_tree(sorted_data)
        print(f"  Apakah complete binary tree? {is_complete}")

        return {
            'expr_value': eval_result[0],
            'data_before': data,
            'data_sorted': sorted_data,
            'is_complete': is_complete,
        }


# =========================================================
# Demo & Test
# =========================================================

def _assert_eq(label, got, expected):
    status = "✓ PASS" if got == expected else f"✗ FAIL (got {got}, expected {expected})"
    print(f"  {status}  {label}")


if __name__ == "__main__":
    print("=" * 60)
    print("1. EXPRESSION TREE — PARSE & EVALUATE")
    print("=" * 60)

    expr_tests = [
        ("((8 * 5) + (9 / (7 - 4)))", 43),   # 40 + 3 = 43
        ("(3 + 4)", 7),
        ("((10 - 3) * (2 + 5))", 49),
        ("(8 / 2)", 4),
        ("((6 + 2) * (9 - 3))", 48),
    ]

    for expr, expected in expr_tests:
        sorter = ExprHeapSorter(expr)
        tokens = deque(sorter._tokenize(expr))
        root = sorter._build_tree(tokens)
        result = sorter._eval_tree(root)
        _assert_eq(f"eval('{expr}')", result, expected)

    print()
    print("Uji pembagian nol:")
    try:
        s = ExprHeapSorter("(5 / (3 - 3))")
        tokens = deque(s._tokenize(s.expr))
        root = s._build_tree(tokens)
        s._eval_tree(root)
        print("  ✗ FAIL  Seharusnya raise ValueError")
    except ValueError as e:
        print(f"  ✓ PASS  ValueError: {e}")

    print()
    print("=" * 60)
    print("2 & 3. IN-PLACE HEAPSORT")
    print("=" * 60)

    heap_tests = [
        [5, 3, 8, 1, 9, 2, 7, 4, 6],
        [1],
        [],
        [3, 3, 1, 1, 2, 2],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
    ]

    s = ExprHeapSorter("(1 + 1)")
    for tc in heap_tests:
        original = tc[:]
        result = s.heapsort_inplace(tc[:])
        expected = sorted(original)
        _assert_eq(f"heapsort({original[:6]}{'...' if len(original)>6 else ''})",
                   result, expected)

    print()
    print("=" * 60)
    print("4. COMPLETE TREE VALIDATOR")
    print("=" * 60)

    complete_tests = [
        ([1, 2, 3, 4, 5, 6, 7], True),   # sempurna
        ([1, 2, 3, 4, 5, 6], True),       # complete tapi tidak sempurna
        ([1, 2, 3, 4, 5], True),
        ([], True),
        ([1], True),
    ]

    s = ExprHeapSorter("(1 + 1)")
    for arr, expected in complete_tests:
        result = s.is_complete_tree(arr)
        _assert_eq(f"is_complete({arr})", result, expected)

    print()
    print("=" * 60)
    print("5. FULL PIPELINE")
    print("=" * 60)

    print("\nEkspresi: ((8 * 5) + (9 / (7 - 4)))")
    sorter = ExprHeapSorter("((8 * 5) + (9 / (7 - 4)))")
    extra = [12, 7, 25, 3, 18, 9, 1]
    pipeline_result = sorter.run_pipeline(extra_values=extra)

    print()
    print("Semua test selesai.")
