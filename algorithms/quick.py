def quick_sort(data):
    """
    Quick Sort para lista de dicionários usando o campo 'popularity' como chave.

    Retorna:
        sorted_data (list)
        comparisons (int)
        swaps (int)
    """

    arr = data.copy()
    comparisons = 0
    swaps = 0

    def partition(low, high):
        nonlocal comparisons, swaps
        pivot = arr[high]["popularity"]
        i = low - 1

        for j in range(low, high):
            comparisons += 1
            if arr[j]["popularity"] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1

        # Colocar o pivô na posição correta
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1

        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            p = partition(low, high)
            quick_sort_recursive(low, p - 1)
            quick_sort_recursive(p + 1, high)

    quick_sort_recursive(0, len(arr) - 1)
    return arr, comparisons, swaps
