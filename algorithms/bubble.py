def bubble_sort(data):
    """
    Implementação do Bubble Sort.
    Retorna uma nova lista ordenada e métricas:
        - sorted_data
        - comparisons
        - swaps
    """

    arr = data.copy()  # evita alterar a lista original
    n = len(arr)

    comparisons = 0
    swaps = 0

    for i in range(n):
        swapped = False  # otimização: para quando já estiver ordenado

        for j in range(0, n - i - 1):
            comparisons += 1  # contamos a comparação
            if arr[j]["popularity"] > arr[j + 1]["popularity"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True

        if not swapped:
            break  # lista já ordenada

    return arr, comparisons, swaps
