import json
import os
import matplotlib.pyplot as plt

ALL_RESULTS_FILE = "benchmark/results/all_results.json"  # benchmark completo

def generate_complete_graphs():
    if not os.path.exists(ALL_RESULTS_FILE):
        print(f"\n❌ Nenhum resultado salvo em {ALL_RESULTS_FILE}")
        return

    with open(ALL_RESULTS_FILE, "r") as f:
        results = json.load(f)

    sizes = sorted([int(s) for s in results.keys()])
    algorithms = list(next(iter(results.values())).keys())

    # ------------------------------
    # 1. Tempo x Tamanho (Random) – todas as curvas
    # ------------------------------
    plt.figure(figsize=(10,6))
    for algo in algorithms:
        times = []
        for size in sizes:
            metrics = results[str(size)][algo].get("random", {})
            time_ms = metrics.get("time_ms")
            times.append(time_ms if time_ms is not None else 0)
        plt.plot(sizes, times, marker='o', label=algo)

    plt.title("Tempo x Tamanho do dataset (Random input)")
    plt.xlabel("Número de músicas")
    plt.ylabel("Tempo de execução (ms)")
    plt.legend()
    plt.grid(True)
    plt.xticks(sizes, rotation=45)
    plt.tight_layout()
    plt.savefig("tempo_random.png")
    plt.show()
    print("✅ Gráfico salvo: tempo_random.png")

    # ------------------------------
    # 2. Tempo x Tamanho por padrões (Bubble e Merge)
    # ------------------------------
    for algo in ["Bubble Sort", "Merge Sort"]:
        plt.figure(figsize=(10,6))
        for pattern in ["random", "sorted", "reversed"]:
            times = []
            for size in sizes:
                metrics = results[str(size)][algo].get(pattern, {})
                time_ms = metrics.get("time_ms")
                times.append(time_ms if time_ms is not None else 0)
            plt.plot(sizes, times, marker='o', label=pattern.capitalize())

        plt.title(f"Tempo x Tamanho do dataset ({algo})")
        plt.xlabel("Número de músicas")
        plt.ylabel("Tempo de execução (ms)")
        plt.legend()
        plt.grid(True)
        plt.xticks(sizes, rotation=45)
        plt.tight_layout()
        plt.savefig(f"tempo_patterns_{algo.replace(' ', '_')}.png")
        plt.show()
        print(f"✅ Gráfico salvo: tempo_patterns_{algo.replace(' ', '_')}.png")

    # ------------------------------
    # 3. Memória x Tamanho (Merge e Quick)
    # ------------------------------
    plt.figure(figsize=(10,6))
    for algo in ["Merge Sort", "Quick Sort"]:
        mem_values = []
        for size in sizes:
            metrics = results[str(size)][algo].get("random", {})
            mem = metrics.get("memory_kb")
            mem_values.append(mem if mem is not None else 0)
        plt.plot(sizes, mem_values, marker='o', label=algo)

    plt.title("Memória x Tamanho do dataset (Random input)")
    plt.xlabel("Número de músicas")
    plt.ylabel("Memória consumida (KB)")
    plt.legend()
    plt.grid(True)
    plt.xticks(sizes, rotation=45)
    plt.tight_layout()
    plt.savefig("memory_random.png")
    plt.show()
    print("✅ Gráfico salvo: memory_random.png")

    # ------------------------------
    # 4. Comparações x Tamanho (todas as curvas)
    # ------------------------------
    plt.figure(figsize=(10,6))
    for algo in algorithms:
        comp_values = []
        for size in sizes:
            metrics = results[str(size)][algo].get("random", {})
            comp = metrics.get("comparisons")
            comp_values.append(comp if comp is not None else 0)
        plt.plot(sizes, comp_values, marker='o', label=algo)

    plt.title("Comparações x Tamanho do dataset (Random input)")
    plt.xlabel("Número de músicas")
    plt.ylabel("Número de comparações")
    plt.legend()
    plt.grid(True)
    plt.xticks(sizes, rotation=45)
    plt.tight_layout()
    plt.savefig("comparisons_random.png")
    plt.show()
    print("✅ Gráfico salvo: comparisons_random.png")

    # ------------------------------
    # 5. Swaps x Tamanho (todas as curvas)
    # ------------------------------
    plt.figure(figsize=(10,6))
    for algo in algorithms:
        swap_values = []
        for size in sizes:
            metrics = results[str(size)][algo].get("random", {})
            swaps = metrics.get("swaps")
            swap_values.append(swaps if swaps is not None else 0)
        plt.plot(sizes, swap_values, marker='o', label=algo)

    plt.title("Swaps x Tamanho do dataset (Random input)")
    plt.xlabel("Número de músicas")
    plt.ylabel("Número de swaps")
    plt.legend()
    plt.grid(True)
    plt.xticks(sizes, rotation=45)
    plt.tight_layout()
    plt.savefig("swaps_random.png")
    plt.show()
    print("✅ Gráfico salvo: swaps_random.png")
