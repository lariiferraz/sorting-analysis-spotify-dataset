from benchmark.runner import run_full_benchmark, run_quick_benchmark
import json
import os

ALL_RESULTS_FILE = "benchmark/results/all_results.json"   # benchmark grande
QUICK_RESULTS_FILE = "benchmark/results/quick_results.json"  # teste rápido


# -------------------------
#  FORMATAÇÃO EM TABELA
# -------------------------
def format_table(result_dict):
    output = ""

    for method, patterns in result_dict.items():
        output += f"\n▶ {method}\n"

        for pattern_name in ["random", "sorted", "reversed"]:
            line = f"{pattern_name.capitalize()} -> "
            p = patterns.get(pattern_name)

            if p and p.get("time_ms") is not None:

                # valores podem não existir em benchmarks antigos → fallback seguro
                time_ms = p.get("time_ms")
                mem = p.get("memory_kb", 0.0)
                comp = p.get("comparisons", 0)
                swaps = p.get("swaps", 0)

                line += (
                    f"tempo: {time_ms:.2f}ms | "
                    f"memória: {mem:.2f}KB | "
                    f"comparisons: {comp} | swaps: {swaps}"
                )
            else:
                line += "❌ não executado"

            output += line + "\n"

    return output


# -------------------------
#  EXIBIR RESULTADOS SALVOS
# -------------------------
def show_saved_results(filename, title):
    if not os.path.exists(filename):
        print(f"\n❌ Nenhum {title} salvo ainda!")
        return

    print(f"\n=== {title.upper()} ===\n")

    with open(filename, "r") as f:
        all_results = json.load(f)

    for size, algos in all_results.items():
        print(f"\n📌 {size} músicas:")
        print(format_table(algos))


# -------------------------
#  MENU PRINCIPAL
# -------------------------
def main():
    while True:
        print("\n=== MENU ===")
        print("1 - Executar benchmark COMPLETO (demorado)")
        print("2 - Executar benchmark RÁPIDO")
        print("3 - Mostrar resultados COMPLETOS salvos")
        print("4 - Mostrar resultados RÁPIDOS salvos")
        print("5 - Sair")

        opt = input("\nEscolha uma opção: ")

        if opt == "1":
            print("\n⏳ Rodando benchmark COMPLETO...")
            run_full_benchmark()
            print(f"\n✅ Benchmark completo salvo em {ALL_RESULTS_FILE}")

        elif opt == "2":
            print("\n⚡ Rodando benchmark RÁPIDO...")
            run_quick_benchmark()
            print(f"\n✅ Benchmark rápido salvo em {QUICK_RESULTS_FILE}")

        elif opt == "3":
            show_saved_results(ALL_RESULTS_FILE, "resultado do benchmark completo")

        elif opt == "4":
            show_saved_results(QUICK_RESULTS_FILE, "resultado do benchmark rápido")

        elif opt == "5":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
