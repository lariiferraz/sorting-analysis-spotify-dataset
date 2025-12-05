from algorithms.merge import merge_sort

def test_merge_sort():
    data = [
        {"track_name": "A", "popularity": 70},
        {"track_name": "B", "popularity": 10},
        {"track_name": "C", "popularity": 40},
        {"track_name": "D", "popularity": 20},
    ]

    sorted_data, comparisons, swaps = merge_sort(data)

    assert [d["popularity"] for d in sorted_data] == [10, 20, 40, 70]

    print("OK! Merge Sort funcionando. {}".format(data))

if __name__ == "__main__":
    test_merge_sort()