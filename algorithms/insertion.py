def insertion_sort(data):
    """
    Insertion Sort para ordenar uma lista de dicionários pelo campo 'popularity'.

    Retorna:
        sorted_data (list): lista ordenada
        comparisons (int): total de comparações realizadas
        swaps (int): total de trocas realizadas
    """
    arr = data.copy()
    n = len(arr)

    comparisons = 0
    swaps = 0

    for i in range(1, n):
        key_item = arr[i]
        j = i - 1

        # Move elementos maiores que key_item para a direita
        while j >= 0:
            comparisons += 1
            if arr[j]["popularity"] > key_item["popularity"]:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break

        arr[j + 1] = key_item

    return arr, comparisons, swaps
