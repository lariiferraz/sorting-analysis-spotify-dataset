from algorithms.insertion import insertion_sort

def test_insertion_sort():
    data = [
        {"track_name": "A", "popularity": 50},
        {"track_name": "B", "popularity": 10},
        {"track_name": "C", "popularity": 30},
    ]

    sorted_data, comparisons, swaps = insertion_sort(data)

    assert [d["popularity"] for d in sorted_data] == [10, 30, 50]
    print("OK! Insertion Sort funcionou.")


if __name__ == "__main__":
    test_insertion_sort()