def merge_sort(data):
    """
    Merge Sort para lista de dicionários pelo campo 'popularity'.

    Retorna:
        sorted_data (list)
        comparisons (int)
        swaps (int)  -> cópias para arrays auxiliares
    """

    arr = data.copy()
    comparisons = 0
    swaps = 0

    def merge(left, right):
        nonlocal comparisons, swaps
        merged = []
        i = j = 0

        # Comparando elementos das duas metades
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i]["popularity"] <= right[j]["popularity"]:
                merged.append(left[i])
                swaps += 1
                i += 1
            else:
                merged.append(right[j])
                swaps += 1
                j += 1

        # Copiando o restante
        while i < len(left):
            merged.append(left[i])
            swaps += 1
            i += 1

        while j < len(right):
            merged.append(right[j])
            swaps += 1
            j += 1

        return merged

    def merge_sort_recursive(subarray):
        if len(subarray) <= 1:
            return subarray

        mid = len(subarray) // 2
        left = merge_sort_recursive(subarray[:mid])
        right = merge_sort_recursive(subarray[mid:])

        return merge(left, right)

    sorted_arr = merge_sort_recursive(arr)
    return sorted_arr, comparisons, swaps
