
import random

def quick_sort(data):
    """
    Quick Sort iterativo com contagem de comparisons e swaps.
    Retorna: sorted_data, comparisons, swaps
    """

    arr = data.copy()  # não altera a lista original
    comparisons = 0
    swaps = 0
    n = len(arr)

    # pilha para armazenar intervalos (low, high)
    stack = [(0, n - 1)]

    while stack:
        low, high = stack.pop()
        if low < high:
            # ----- Partition com pivô aleatório -----
            pivot_index = random.randint(low, high)
            arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
            swaps += 1

            pivot = arr[high]["popularity"]
            i = low - 1
            for j in range(low, high):
                comparisons += 1
                if arr[j]["popularity"] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    swaps += 1
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            swaps += 1

            p = i + 1

            # adiciona subarrays à pilha
            stack.append((low, p - 1))
            stack.append((p + 1, high))

    return arr, comparisons, swaps

