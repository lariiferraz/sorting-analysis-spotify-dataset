import json
import time
import random
import tracemalloc
from loader.loader import load_spotify_dataset
from algorithms import bubble_sort, insertion_sort, merge_sort, quick_sort

ALL_RESULTS_FILE = "benchmark/results/all_results.json"     # benchmark completo
QUICK_RESULTS_FILE = "benchmark/results/quick_results.json" # teste rápido

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}

FULL_SIZES = [100, 500, 2000, 10000, 50000, 100000, 114000]
QUICK_SIZES = [100, 500, 2000]
PATTERNS = ["random", "sorted", "reversed"]


# -----------------------------------------------------
#   MEDIÇÃO COMPLETA (tempo + memória + comp + swaps)
# -----------------------------------------------------
def measure_full(algorithm, data):
    tracemalloc.start()
    start = time.perf_counter()

    _, comp, swaps = algorithm(data)

    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "time_ms": (end - start) * 1000,
        "memory_kb": peak / 1024,
        "comparisons": comp,
        "swaps": swaps
    }


def generate_patterns(data):
    base_sorted = sorted(data, key=lambda x: x["popularity"])
    return {
        "random": random.sample(data, len(data)),
        "sorted": base_sorted,
        "reversed": list(reversed(base_sorted))
    }


# -----------------------------------------------------
#  BENCHMARK COMPLETO — FORMATO DE TABELA ORIGINAL
# -----------------------------------------------------
def run_full_benchmark():
    print("\n🚀 Executando benchmark COMPLETO...")
    data = load_spotify_dataset("dataset.csv")
    results = {}

    for size in FULL_SIZES:
        print(f"\n=== Benchmark com {size} músicas ===")
        sliced = data[:size]
        patterns = generate_patterns(sliced)

        results[size] = {}

        for alg_name, alg_func in ALGORITHMS.items():
            print(f"\nExecutando {alg_name}...")
            results[size][alg_name] = {}

            # Pular algoritmos inviáveis
            if size > 5000 and alg_name in ["Bubble Sort", "Insertion Sort"]:
                print(f"{alg_name} ignorado em {size} músicas (O(n²) inviável)")
                results[size][alg_name] = {
                    "random":   {"time_ms": None, "memory_kb": None, "comparisons": None, "swaps": None},
                    "sorted":   {"time_ms": None, "memory_kb": None, "comparisons": None, "swaps": None},
                    "reversed": {"time_ms": None, "memory_kb": None, "comparisons": None, "swaps": None}
                }
                continue

            for pattern in PATTERNS:
                dataset = patterns[pattern].copy()
                metrics = measure_full(alg_func, dataset)

                results[size][alg_name][pattern] = metrics

                # TABELA — FORMATO EXATO ORIGINAL
                print(
                    f"{pattern.capitalize():<10} -> "
                    f"tempo: {metrics['time_ms']:.2f}ms | "
                    f"memória: {metrics['memory_kb']:.2f}KB | "
                    f"comparisons: {metrics['comparisons']} | "
                    f"swaps: {metrics['swaps']}"
                )

    with open(ALL_RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=4)

    print("\n✅ Benchmark COMPLETO salvo em benchmark/results/all_results.json")


# -----------------------------------------------------
#  BENCHMARK RÁPIDO — FORMATO COMPACTO
# -----------------------------------------------------
def run_quick_benchmark():
    print("\n⚡ Executando benchmark RÁPIDO...\n")

    data = load_spotify_dataset("dataset.csv")
    results = {}

    def measure_quick(algorithm, data):
        tracemalloc.start()
        start = time.perf_counter()

        _, comparisons, swaps = algorithm(data)

        end = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "time_ms": (end - start) * 1000,
            "memory_kb": peak / 1024,
            "comparisons": comparisons,
            "swaps": swaps
        }

    for size in QUICK_SIZES:
        print(f"\n=== Benchmark com {size} músicas ===")
        sliced = data[:size]

        random_data = sliced.copy()
        random.shuffle(random_data)
        sorted_data = sorted(sliced, key=lambda x: x["popularity"])
        reversed_data = list(reversed(sorted_data))

        patterns = {
            "random": random_data,
            "sorted": sorted_data,
            "reversed": reversed_data
        }

        results[size] = {}

        for alg_name, alg_func in ALGORITHMS.items():
            print(f"\nExecutando {alg_name}...")
            results[size][alg_name] = {}

            for pattern_name in PATTERNS:
                dataset = patterns[pattern_name].copy()
                metrics = measure_quick(alg_func, dataset)

                results[size][alg_name][pattern_name] = metrics

                print(
                    f"{pattern_name.capitalize():<10} -> "
                    f"tempo: {metrics['time_ms']:.2f}ms | "
                    f"memória: {metrics['memory_kb']:.2f}KB | "
                    f"comparisons: {metrics['comparisons']} | "
                    f"swaps: {metrics['swaps']}"
                )

        print()

    with open(QUICK_RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=4)

    print("\n✅ Benchmark rápido salvo em benchmark/results/quick_results.json\n")
