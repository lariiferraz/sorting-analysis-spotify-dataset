from benchmark.runner import run_full_benchmark, run_quick_benchmark
import json
import os
import matplotlib.pyplot as plt
import numpy as np

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
#  FUNÇÕES DE GRÁFICOS (APENAS 3 GRÁFICOS)
# -------------------------
def load_results():
    """Carrega os resultados do arquivo JSON"""
    try:
        with open(ALL_RESULTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {ALL_RESULTS_FILE} não encontrado!")
        return None


def generate_enhanced_graphs():
    """Gera os 3 gráficos principais para análise de desempenho"""
    
    results = load_results()
    if not results:
        print("❌ Não foi possível carregar os resultados. Execute o benchmark completo primeiro.")
        return
    
    # Ordenar tamanhos numericamente
    sizes = sorted([int(s) for s in results.keys()])
    algorithms = ["Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort"]
    patterns = ["random", "sorted", "reversed"]
    pattern_names = {"random": "Random", "sorted": "Ordenado", "reversed": "Invertido"}
    
    # Configurações de estilo
    plt.style.use('seaborn-v0_8-darkgrid')
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    print("\n" + "="*60)
    print("🚀 GERANDO OS 3 GRÁFICOS PRINCIPAIS")
    print("="*60)
    
    # ========================================================
    # GRÁFICO 1: Desempenho Temporal por Padrão de Entrada
    # ========================================================
    print("\n📊 Gerando Gráfico 1: Desempenho Temporal por Padrão de Entrada")
    
    fig1, axes1 = plt.subplots(1, 3, figsize=(18, 5))
    
    for pattern_idx, pattern in enumerate(patterns):
        ax = axes1[pattern_idx]
        
        for idx, algo in enumerate(algorithms):
            times = []
            valid_sizes = []
            
            for size in sizes:
                metrics = results[str(size)][algo][pattern]
                if metrics["time_ms"] is not None:
                    times.append(metrics["time_ms"])
                    valid_sizes.append(size)
            
            if times:
                ax.loglog(valid_sizes, times, 'o-', label=algo, 
                         color=colors[idx], linewidth=2, markersize=6)
        
        ax.set_title(f'Padrão: {pattern_names[pattern]}', fontsize=13, fontweight='bold')
        ax.set_xlabel('Tamanho do Array', fontsize=11)
        ax.set_ylabel('Tempo (ms)', fontsize=11)
        ax.grid(True, which="both", ls="-", alpha=0.2)
        
        if pattern_idx == 0:
            ax.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig('desempenho_temporal_padroes.png', dpi=300, bbox_inches='tight')
    print("✅ Salvo: desempenho_temporal_padroes.png")
    
    # ========================================================
    # GRÁFICO 2: Análise de Complexidade: Comparações vs Tamanho
    # ========================================================
    print("\n📊 Gerando Gráfico 2: Análise de Complexidade: Comparações vs Tamanho")
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    for idx, algo in enumerate(algorithms):
        comparisons = []
        valid_sizes = []
        
        for size in sizes:
            metrics = results[str(size)][algo]["random"]
            if metrics["comparisons"] is not None:
                comparisons.append(metrics["comparisons"])
                valid_sizes.append(size)
        
        if comparisons:
            ax2.loglog(valid_sizes, comparisons, 'D-', label=algo, 
                      color=colors[idx], linewidth=2, markersize=6, alpha=0.8)
    
    # Adicionar linhas de referência teóricas
    x_ref = np.array([100, 2000])
    ax2.loglog(x_ref, x_ref**2/2, 'k--', label='O(n²)', alpha=0.5, linewidth=1)
    ax2.loglog(x_ref, x_ref * np.log(x_ref), 'k:', label='O(n log n)', alpha=0.5, linewidth=1)
    
    ax2.set_title('Análise de Complexidade: Comparações vs Tamanho (Random)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Tamanho do Array (n)', fontsize=12)
    ax2.set_ylabel('Número de Comparações', fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('comparacoes_vs_tamanho.png', dpi=300, bbox_inches='tight')
    print("✅ Salvo: comparacoes_vs_tamanho.png")
    
    # ========================================================
    # GRÁFICO 3: Análise de Consumo de Memória por Algoritmo
    # ========================================================
    print("\n📊 Gerando Gráfico 3: Análise de Consumo de Memória por Algoritmo")
    
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    
    for idx, algo in enumerate(["Merge Sort", "Quick Sort"]):
        mem_values = []
        valid_sizes = []
        
        for size in sizes:
            metrics = results[str(size)][algo]["random"]
            if metrics["memory_kb"] is not None:
                mem_values.append(metrics["memory_kb"])
                valid_sizes.append(size)
        
        if mem_values:
            ax3.plot(valid_sizes, mem_values, 's-', label=algo, 
                    color=colors[idx+2], linewidth=2, markersize=8)
    
    ax3.set_title('Análise de Consumo de Memória por Algoritmo (Random)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Tamanho do Array (n)', fontsize=12)
    ax3.set_ylabel('Memória (KB)', fontsize=12)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig('memoria_vs_tamanho.png', dpi=300, bbox_inches='tight')
    print("✅ Salvo: memoria_vs_tamanho.png")
    
    # Mostrar os gráficos
    plt.show()
    
    print("\n" + "="*60)
    print("🎉 OS 3 GRÁFICOS PRINCIPAIS FORAM GERADOS COM SUCESSO!")
    print("="*60)
    print("\n📁 Arquivos gerados na pasta atual:")
    print("1. desempenho_temporal_padroes.png - Desempenho Temporal por Padrão de Entrada")
    print("2. comparacoes_vs_tamanho.png - Análise de Complexidade: Comparações vs Tamanho")
    print("3. memoria_vs_tamanho.png - Análise de Consumo de Memória por Algoritmo")


# -------------------------
#  MENU PRINCIPAL
# -------------------------
def main():
    while True:
        print("\n" + "="*50)
        print("=== MENU PRINCIPAL - ANÁLISE DE ALGORITMOS ===")
        print("="*50)
        print("1 - Executar benchmark COMPLETO (demorado)")
        print("2 - Executar benchmark RÁPIDO")
        print("3 - Mostrar resultados COMPLETOS salvos")
        print("4 - Mostrar resultados RÁPIDOS salvos")
        print("5 - Gerar os 3 gráficos principais")
        print("6 - Mostrar tabelas detalhadas do benchmark completo")
        print("7 - Sair")
        print("-"*50)

        opt = input("\nEscolha uma opção: ").strip()

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
            print("\n📈 Gerando os 3 gráficos principais...")
            generate_enhanced_graphs()

        elif opt == "6":
            print("\n📋 Mostrando tabelas detalhadas do benchmark completo...")
            show_detailed_tables(ALL_RESULTS_FILE)

        elif opt == "7":
            print("\n👋 Saindo do programa...")
            break

        else:
            print("\n❌ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()