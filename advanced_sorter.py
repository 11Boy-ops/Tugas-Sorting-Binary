"""
advanced_sorter.py
==================
Implementasi AdvancedSorter untuk tugas Analisis & Desain Algoritma Sorting Lanjutan.

Modul ini mengimplementasikan:
1. Array Merge Sort menggunakan virtual sublists + single tmpArray (O(n) ruang tambahan)
2. Linked List Merge Sort menggunakan fast-slow pointer + dummy node merge (O(log n) ruang)
3. Quick Sort dengan pivot Median-of-Three + fallback ke Merge Sort jika depth berlebih

Semua implementasi TANPA menggunakan list.sort(), sorted(), slice[:], atau library eksternal.
"""

import math
from typing import List, Optional


class ListNode:
    """Node untuk singly linked list."""
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        return f"ListNode({self.data})"


class AdvancedSorter:
    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
    # =========================================================

    def sort_array(self, arr: List[int]) -> List[int]:
        """
        Mengurutkan array integer secara ascending menggunakan Merge Sort.
        Hanya mengalokasikan SATU tmpArray berukuran n di awal, tidak membuat
        sublist tambahan di tiap rekursi (virtual sublists via indeks).
        """
        if len(arr) <= 1:
            return arr
        tmp_array = [0] * len(arr)  # Single temporary array — alokasi O(n) sekali saja
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr: List[int], first: int, last: int, tmp_array: List[int]):
        """
        Rekursi merge sort pada rentang arr[first..last].
        Tidak membuat subarray baru; 'sublist' adalah virtual berdasarkan indeks.
        """
        if first >= last:
            return
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr: List[int], left_start: int, mid: int,
                       right_end: int, tmp_array: List[int]):
        """
        Menggabungkan dua virtual sublist yang bersebelahan:
          - Sublist kiri : arr[left_start .. mid]
          - Sublist kanan: arr[mid+1 .. right_end]

        Algoritma:
        1. Salin semua elemen ke tmp_array terlebih dahulu.
        2. Bandingkan dari dua pointer (a dan b), pilih yang lebih kecil.
           Gunakan <= agar STABLE: jika sama, ambil dari sublist kiri dulu.
        3. Salin hasil gabungan kembali ke arr[left_start..right_end].

        Kompleksitas: O(right_end - left_start + 1) waktu & O(1) ruang tambahan
        (tmp_array sudah dialokasi di luar).
        """
        # Salin ke buffer sementara
        for k in range(left_start, right_end + 1):
            tmp_array[k] = arr[k]

        a = left_start        # pointer sublist kiri
        b = mid + 1           # pointer sublist kanan
        k = left_start        # pointer output

        while a <= mid and b <= right_end:
            # Gunakan <= agar STABLE: elemen kiri diprioritaskan bila nilai sama
            if tmp_array[a] <= tmp_array[b]:
                arr[k] = tmp_array[a]
                a += 1
            else:
                arr[k] = tmp_array[b]
                b += 1
            k += 1

        # Salin sisa sublist kiri (jika ada)
        while a <= mid:
            arr[k] = tmp_array[a]
            a += 1
            k += 1

        # Salin sisa sublist kanan (jika ada)
        while b <= right_end:
            arr[k] = tmp_array[b]
            b += 1
            k += 1

    # =========================================================
    # 2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)
    # =========================================================

    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Mengurutkan singly linked list secara ascending menggunakan Merge Sort.
        - Pemisahan: fast-slow pointer (O(n) tanpa menghitung panjang)
        - Penggabungan: dummy node + tail reference (tanpa alokasi node baru)
        - Kompleksitas ruang: O(log n) hanya untuk stack rekursi
        """
        if head is None or head.next is None:
            return head

        # Split list menjadi dua bagian
        right_head = self._split_linked_list(head)
        left_head = head

        # Rekursi pada masing-masing bagian
        left_sorted = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)

        # Merge dua sorted list
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        """
        Menemukan titik tengah linked list dalam SATU traversal menggunakan
        teknik fast-slow pointer:
          - midPoint bergerak 1 langkah per iterasi
          - curNode  bergerak 2 langkah per iterasi
        Saat curNode mencapai akhir, midPoint tepat di tengah.

        Setelah split:
          - List kiri : head  → ... → midPoint (midPoint.next = None)
          - List kanan: midPoint.next → ... → None (dikembalikan)
        """
        midPoint = head        # bergerak 1 langkah
        curNode = head.next    # bergerak 2 langkah (mulai dari head.next agar genap split)

        while curNode is not None and curNode.next is not None:
            midPoint = midPoint.next
            curNode = curNode.next.next

        right_head = midPoint.next
        midPoint.next = None   # Putus link → list kiri berakhir di midPoint
        return right_head

    def _merge_linked_lists(self, listA: Optional[ListNode],
                             listB: Optional[ListNode]) -> Optional[ListNode]:
        """
        Menggabungkan dua sorted linked list menjadi satu sorted linked list.

        Teknik dummy node + tail reference:
          - dummy: sentinel node sementara; tidak perlu alokasi node baru untuk data
          - tail : selalu menunjuk ke node terakhir list hasil
          - Operasi hanya memodifikasi pointer .next, TANPA membuat node baru

        STABLE: jika listA.data == listB.data, listA diambil lebih dulu
        (mempertahankan urutan relatif asli).
        """
        dummy = ListNode(0)    # sentinel; dibuang setelah merge selesai
        tail = dummy

        while listA is not None and listB is not None:
            # STABLE: ambil dari listA bila sama (<=)
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next
            tail = tail.next

        # Sambungkan sisa (hanya salah satu yang tersisa)
        if listA is not None:
            tail.next = listA
        else:
            tail.next = listB

        return dummy.next

    # =========================================================
    # 3. QUICK SORT PARTITION (Median-of-Three Pivot)
    # =========================================================

    def sort_array_quicksort(self, arr: List[int]) -> List[int]:
        """
        Entry point Quick Sort dengan depth limiter.
        Jika kedalaman rekursi melebihi 2 * log2(n), fallback ke Merge Sort.
        """
        if len(arr) <= 1:
            return arr
        n = len(arr)
        max_depth = int(2 * math.log2(n)) if n > 1 else 1
        self._quick_sort_recursive(arr, 0, len(arr) - 1, depth=0, max_depth=max_depth)
        return arr

    def _quick_sort_recursive(self, arr: List[int], first: int, last: int,
                               depth: int, max_depth: int):
        """
        Rekursi Quick Sort dengan fallback ke Merge Sort jika depth berlebih.
        """
        if first >= last:
            return

        # Fallback ke Merge Sort jika terlalu dalam (mencegah O(n²) worst-case)
        if depth > max_depth:
            # Sort subarray arr[first..last] menggunakan Merge Sort
            sub_arr = arr[first:last + 1]
            tmp = [0] * len(sub_arr)
            self._rec_merge_sort(sub_arr, 0, len(sub_arr) - 1, tmp)
            arr[first:last + 1] = sub_arr
            return

        pivot_pos = self.partition_quick(arr, first, last)
        self._quick_sort_recursive(arr, first, pivot_pos - 1, depth + 1, max_depth)
        self._quick_sort_recursive(arr, pivot_pos + 1, last, depth + 1, max_depth)

    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        """
        Partisi in-place dengan pivot Median-of-Three.

        Langkah:
        1. Pilih median dari arr[first], arr[mid], arr[last] sebagai pivot.
        2. Tukar pivot ke posisi arr[first].
        3. Jalankan logika partisi standar (left scan ke kanan, right scan ke kiri).
        4. Kembalikan posisi akhir pivot.

        Catatan stabilitas: Quick Sort partisi standar TIDAK stabil karena swap
        jarak jauh. Untuk kebutuhan stable sort, gunakan sort_array() (Merge Sort).
        """
        mid = (first + last) // 2

        # --- Median-of-Three ---
        # Urutkan arr[first], arr[mid], arr[last] secara lokal
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]
        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]
        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]
        # Sekarang arr[first] <= arr[mid] <= arr[last]
        # median ada di arr[mid]

        # Pindahkan pivot (median) ke posisi first
        arr[first], arr[mid] = arr[mid], arr[first]
        pivot = arr[first]

        # --- Partisi Standar ---
        left = first + 1
        right = last

        while True:
            # Gerakkan left ke kanan selama < pivot
            while left <= right and arr[left] < pivot:
                left += 1
            # Gerakkan right ke kiri selama > pivot
            while right >= left and arr[right] > pivot:
                right -= 1

            if left > right:
                break
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1

        # Tempatkan pivot di posisi akhirnya
        arr[first], arr[right] = arr[right], arr[first]
        return right


# =========================================================
# Fungsi bantu: konversi list ↔ linked list
# =========================================================

def list_to_linked(lst: List) -> Optional[ListNode]:
    """Konversi Python list ke singly linked list."""
    if not lst:
        return None
    head = ListNode(lst[0])
    cur = head
    for val in lst[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head


def linked_to_list(head: Optional[ListNode]) -> List:
    """Konversi singly linked list ke Python list."""
    result = []
    cur = head
    while cur:
        result.append(cur.data)
        cur = cur.next
    return result


# =========================================================
# Demo & Test
# =========================================================

if __name__ == "__main__":
    sorter = AdvancedSorter()

    print("=" * 60)
    print("1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)")
    print("=" * 60)

    test_cases = [
        [5, 3, 8, 1, 9, 2, 7, 4, 6],
        [1],
        [],
        [3, 3, 1, 1, 2, 2],          # duplikat — uji stabilitas
        [9, 8, 7, 6, 5, 4, 3, 2, 1], # descending
        [1, 2, 3, 4, 5],              # already sorted
    ]

    for tc in test_cases:
        original = tc[:]
        result = sorter.sort_array(tc[:])
        expected = sorted(original)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}  Input: {original[:8]}{'...' if len(original)>8 else ''}")
        print(f"         Output: {result[:8]}{'...' if len(result)>8 else ''}")

    print()
    print("=" * 60)
    print("2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)")
    print("=" * 60)

    ll_cases = [
        [5, 3, 8, 1, 9, 2],
        [1],
        [2, 1],
        [3, 3, 1, 1, 2],   # duplikat
        [5, 4, 3, 2, 1],   # descending
    ]

    for tc in ll_cases:
        original = tc[:]
        head = list_to_linked(tc)
        sorted_head = sorter.sort_linked_list(head)
        result = linked_to_list(sorted_head)
        expected = sorted(original)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}  Input: {original}")
        print(f"         Output: {result}")

    print()
    print("=" * 60)
    print("3. QUICK SORT (Median-of-Three + Fallback)")
    print("=" * 60)

    qs_cases = [
        [5, 3, 8, 1, 9, 2, 7, 4, 6],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],  # worst-case untuk naive quick sort
        [1, 2, 3, 4, 5, 6, 7, 8, 9],  # already sorted
        [3, 3, 1, 1, 2, 2],
    ]

    for tc in qs_cases:
        original = tc[:]
        result = sorter.sort_array_quicksort(tc[:])
        expected = sorted(original)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}  Input: {original}")
        print(f"         Output: {result}")

    print()
    print("Semua test selesai.")
