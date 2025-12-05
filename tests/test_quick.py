from algorithms.quick import quick_sort


def test_quick_sort():
    data = [
        {"track_name": "A", "popularity": 50},
        {"track_name": "B", "popularity": 10},
        {"track_name": "C", "popularity": 80},
        {"track_name": "D", "popularity": 30},
    ]

    sorted_data, comparisons, swaps = quick_sort(data)

    assert [d["popularity"] for d in sorted_data] == [10, 30, 50, 80]

    print("OK! Quick Sort funcionando.")


if __name__ == "__main__":
    test_quick_sort()
