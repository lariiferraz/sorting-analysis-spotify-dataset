def bubble_sort(data):
    """
    Implementação do Bubble Sort.
    Retorna uma nova lista ordenada sem modificar a original.
    """

    arr = data.copy()  # evita alterar a lista original
    n = len(arr)

    for i in range(n):
        swapped = False  # otimização: para quando já estiver ordenado

        for j in range(0, n - i - 1):
            if arr[j]["popularity"] > arr[j + 1]["popularity"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break  # lista já ordenada

    return arr
