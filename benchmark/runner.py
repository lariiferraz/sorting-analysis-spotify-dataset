import time
import tracemalloc
import random
from loader.loader import load_spotify_dataset
from algorithms import bubble_sort, insertion_sort, merge_sort, quick_sort

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}

SIZES = [100, 500, 2000, 10000, 50000, 100000, 114000]  # ajuste conforme tamanho do dataset

PATTERNS = ["random", "sorted", "reversed"]


# --------- Funções de benchmark ---------
def measure(algorithm, data):
    """Roda algoritmo e mede tempo e memória, retornando métricas."""
    tracemalloc.start()
    start = time.perf_counter()

    sorted_data, comparisons, swaps = algorithm(data)

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "sorted_data": sorted_data,
        "comparisons": comparisons,
        "swaps": swaps,
        "time_ms": (end - start) * 1000,
        "memory_kb": peak / 1024
    }


def generate_patterns(data):
    """Gera diferentes padrões de entrada: random, sorted e reversed."""
    # ALEATÓRIO
    random_data = data.copy()
    random.shuffle(random_data)

    # ORDENADO
    sorted_data = sorted(data, key=lambda x: x["popularity"])

    # REVERSO
    reversed_data = list(reversed(sorted_data))

    return {
        "random": random_data,
        "sorted": sorted_data,
        "reversed": reversed_data
    }


# --------- Função principal ---------
def main():
    print("Carregando dataset...")
    data = load_spotify_dataset("dataset.csv") 

    results = {}

    for size in SIZES:
        print(f"\n=== Benchmark com {size} músicas ===")
        sliced_data = data[:size]

        patterns = generate_patterns(sliced_data)
        results[size] = {}

        for alg_name, alg_func in ALGORITHMS.items():
            results[size][alg_name] = {}
            print(f"\nExecutando {alg_name}...")

            for pattern_name in PATTERNS:
                dataset = patterns[pattern_name].copy()
                metrics = measure(alg_func, dataset)

                results[size][alg_name][pattern_name] = {
                    "time_ms": metrics["time_ms"],
                    "memory_kb": metrics["memory_kb"],
                    "comparisons": metrics["comparisons"],
                    "swaps": metrics["swaps"]
                }

                print(f"{pattern_name.capitalize():<10} -> "
                      f"tempo: {metrics['time_ms']:.2f}ms | "
                      f"memória: {metrics['memory_kb']:.2f}KB | "
                      f"comparisons: {metrics['comparisons']} | "
                      f"swaps: {metrics['swaps']}")

    # Salva resultados em JSON
    import json
    with open("benchmark/results/all_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("\n✅ Benchmark completo! Resultados salvos em benchmark/results/all_results.json")


if __name__ == "__main__":
    main()
