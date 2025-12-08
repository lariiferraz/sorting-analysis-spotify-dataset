from benchmark.runner import run_full_benchmark, run_quick_benchmark
import json
import os
import matplotlib.pyplot as plt
from benchmark.graphs import generate_complete_graphs  # função que gera todos os gráficos

ALL_RESULTS_FILE = "benchmark/results/all_results.json"   # benchmark completo
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
                # fallback seguro caso métricas não existam
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
#  NOVA FUNÇÃO: TABELAS DETALHADAS
# -------------------------
def show_detailed_tables(filename):
    if not os.path.exists(filename):
        print(f"\n❌ Nenhum resultado salvo em {filename}")
        return

    with open(filename, "r") as f:
        results = json.load(f)

    for algo in next(iter(results.values())).keys():  # pega todos os algoritmos
        print(f"\n================ {algo} =================\n")
        for pattern in ["random", "sorted", "reversed"]:
            print(f"--- Padrão: {pattern.capitalize()} ---")
            print(f"{'Tamanho':>12} | {'Tempo(ms)':>15} | {'Memória(KB)':>15} | {'Comparisons':>15} | {'Swaps':>10}")
            print("-" * 75)
            for size in sorted([int(s) for s in results.keys()]):
                metrics = results[str(size)][algo].get(pattern, {})
                if metrics.get("time_ms") is None:
                    print(f"{size:>12} | {'-':>15} | {'-':>15} | {'-':>15} | {'-':>10}")
                else:
                    # Formatação com vírgula decimal e ponto de milhar
                    time_fmt = f"{metrics.get('time_ms',0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    mem_fmt = f"{metrics.get('memory_kb',0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    comp_fmt = f"{metrics.get('comparisons',0):,}".replace(",", ".")
                    swaps_fmt = f"{metrics.get('swaps',0):,}".replace(",", ".")
                    print(f"{size:>12} | {time_fmt:>15} | {mem_fmt:>15} | {comp_fmt:>15} | {swaps_fmt:>10}")
            print("\n")



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
        print("5 - Gerar gráficos a partir do benchmark completo")
        print("6 - Sair")
        print("7 - Mostrar tabelas detalhadas do benchmark completo")

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
            print("\n📊 Gerando gráficos a partir do benchmark completo...")
            generate_complete_graphs()  # chama função para gerar gráficos

        elif opt == "6":
            print("Saindo...")
            break

        elif opt == "7":
            print("\n📋 Mostrando tabelas detalhadas do benchmark completo...")
            show_detailed_tables(ALL_RESULTS_FILE)

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
