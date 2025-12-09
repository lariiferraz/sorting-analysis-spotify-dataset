import json
import matplotlib.pyplot as plt
import numpy as np
import os

def load_results():
    """Carrega os resultados do arquivo JSON"""
    try:
        with open("all_results.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo all_results.json não encontrado!")
        return None

def generate_enhanced_graphs():
    """Gera gráficos aprimorados para análise de desempenho"""
    
    results = load_results()
    if not results:
        return
    
    # Ordenar tamanhos numericamente
    sizes = sorted([int(s) for s in results.keys()])
    algorithms = ["Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort"]
    patterns = ["random", "sorted", "reversed"]
    pattern_names = {"random": "Random", "sorted": "Ordenado", "reversed": "Invertido"}
    
    # Configurações de estilo
    plt.style.use('seaborn-v0_8-darkgrid')
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']  # Cores para cada algoritmo
    
    # ==================== 1. TEMPO vs TAMANHO (RANDOM) - Escala Logarítmica ====================
    print("\n📊 Gerando gráfico 1: Tempo vs Tamanho (Random) - Escala Log-Log")
    
    fig1, (ax1_log, ax1_linear) = plt.subplots(1, 2, figsize=(16, 6))
    
    for idx, algo in enumerate(algorithms):
        times = []
        valid_sizes = []
        
        for size in sizes:
            metrics = results[str(size)][algo]["random"]
            if metrics["time_ms"] is not None:
                times.append(metrics["time_ms"])
                valid_sizes.append(size)
        
        if times:  # Só plotar se houver dados
            # Gráfico log-log
            ax1_log.loglog(valid_sizes, times, 'o-', label=algo, 
                          color=colors[idx], linewidth=2, markersize=8)
            
            # Gráfico linear
            ax1_linear.plot(valid_sizes, times, 'o-', label=algo,
                           color=colors[idx], linewidth=2, markersize=8)
    
    ax1_log.set_title('Tempo vs Tamanho (Random) - Escala Log-Log', fontsize=14, fontweight='bold')
    ax1_log.set_xlabel('Tamanho do Array (n)', fontsize=12)
    ax1_log.set_ylabel('Tempo (ms)', fontsize=12)
    ax1_log.legend(fontsize=10)
    ax1_log.grid(True, which="both", ls="-", alpha=0.2)
    
    ax1_linear.set_title('Tempo vs Tamanho (Random) - Escala Linear', fontsize=14, fontweight='bold')
    ax1_linear.set_xlabel('Tamanho do Array (n)', fontsize=12)
    ax1_linear.set_ylabel('Tempo (ms)', fontsize=12)
    ax1_linear.legend(fontsize=10)
    ax1_linear.grid(True, alpha=0.3)
    ax1_linear.set_yscale('log')  # Mantém escala log no y para melhor visualização
    
    plt.tight_layout()
    plt.savefig('tempo_random_comparacao.png', dpi=300, bbox_inches='tight')
    print("✅ Salvo: tempo_random_comparacao.png")
    
    # ==================== 2. COMPARAÇÃO POR PADRÕES (n=2000) ====================
    print("\n📊 Gerando gráfico 2: Comparação por Padrões (n=2000)")
    
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    
    size_to_analyze = 2000
    x = np.arange(len(algorithms))
    width = 0.25
    
    for pattern_idx, pattern in enumerate(patterns):
        times = []
        for algo in algorithms:
            metrics = results[str(size_to_analyze)][algo][pattern]
            times.append(metrics["time_ms"] if metrics["time_ms"] is not None else 0)
        
        bars = ax2.bar(x + pattern_idx * width, times, width, 
                      label=pattern_names[pattern], alpha=0.8)
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:,.0f}' if height >= 10 else f'{height:.2f}',
                        ha='center', va='bottom', fontsize=9)
    
    ax2.set_title(f'Comparação de Tempo por Padrão (n={size_to_analyze})', 
                 fontsize=14, fontweight='bold')
    ax2.set_xlabel('Algoritmo', fontsize=12)
    ax2.set_ylabel('Tempo (ms)', fontsize=12)
    ax2.set_xticks(x + width)
    ax2.set_xticklabels(algorithms, rotation=15)
    ax2.legend(fontsize=10)
    ax2.set_yscale('log')  # Escala log para melhor visualização das diferenças
    
    plt.tight_layout()
    plt.savefig('comparacao_padroes_n2000.png', dpi=300, bbox_inches='tight')
    print("✅ Salvo: comparacao_padroes_n2000.png")
    
    # ==================== 3. MEMÓRIA vs TAMANHO ====================
    print("\n📊 Gerando gráfico 3: Memória vs Tamanho")
    
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
    
    ax3.set_title('Uso de Memória vs Tamanho (Random)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Tamanho do Array (n)', fontsize=12)
    ax3.set_ylabel('Memória (KB)', fontsize=12)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig('memoria_vs_tamanho.png', dpi=300, bbox_inches='tight')
    print("✅ Salvo: memoria_vs_tamanho.png")
    
    # ==================== 4. NÚMERO DE COMPARAÇÕES (RANDOM) ====================
    print("\n📊 Gerando gráfico 4: Número de Comparações")
    
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    
    for idx, algo in enumerate(algorithms):
        comparisons = []
        valid_sizes = []
        
        for size in sizes:
            metrics = results[str(size)][algo]["random"]
            if metrics["comparisons"] is not None:
                comparisons.append(metrics["comparisons"])
                valid_sizes.append(size)
        
        if comparisons:
            ax4.loglog(valid_sizes, comparisons, 'D-', label=algo, 
                      color=colors[idx], linewidth=2, markersize=6, alpha=0.8)
    
    # Adicionar linhas de referência teóricas
    x_ref = np.array([100, 2000])
    ax4.loglog(x_ref, x_ref**2/2, 'k--', label='O(n²)', alpha=0.5, linewidth=1)
    ax4.loglog(x_ref, x_ref * np.log(x_ref), 'k:', label='O(n log n)', alpha=0.5, linewidth=1)
    
    ax4.set_title('Número de Comparações vs Tamanho (Random)', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Tamanho do Array (n)', fontsize=12)
    ax4.set_ylabel('Número de Comparações', fontsize=12)
    ax4.legend(fontsize=10)
    ax4.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('comparacoes_vs_tamanho.png', dpi=300, bbox_inches='tight')
    print("✅ Salvo: comparacoes_vs_tamanho.png")
    
    # ==================== 7. RESUMO DOS ALGORITMOS O(n log n) ====================
    print("\n📊 Gerando gráfico 7: Resumo Merge vs Quick Sort")
    
    fig7, (ax7a, ax7b) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Merge Sort
    for idx, pattern in enumerate(patterns):
        times = []
        valid_sizes = []
        
        for size in sizes:
            metrics = results[str(size)]["Merge Sort"][pattern]
            if metrics["time_ms"] is not None:
                times.append(metrics["time_ms"])
                valid_sizes.append(size)
        
        if times:
            ax7a.plot(valid_sizes, times, 'o-', label=pattern_names[pattern],
                     color=colors[idx], linewidth=2, markersize=6)
    
    ax7a.set_title('Merge Sort: Tempo por Padrão', fontsize=13, fontweight='bold')
    ax7a.set_xlabel('Tamanho do Array', fontsize=11)
    ax7a.set_ylabel('Tempo (ms)', fontsize=11)
    ax7a.set_xscale('log')
    ax7a.set_yscale('log')
    ax7a.legend(fontsize=9)
    ax7a.grid(True, alpha=0.3)
    
    # Quick Sort
    for idx, pattern in enumerate(patterns):
        times = []
        valid_sizes = []
        
        for size in sizes:
            metrics = results[str(size)]["Quick Sort"][pattern]
            if metrics["time_ms"] is not None:
                times.append(metrics["time_ms"])
                valid_sizes.append(size)
        
        if times:
            ax7b.plot(valid_sizes, times, 's-', label=pattern_names[pattern],
                     color=colors[idx], linewidth=2, markersize=6)
    
    ax7b.set_title('Quick Sort: Tempo por Padrão', fontsize=13, fontweight='bold')
    ax7b.set_xlabel('Tamanho do Array', fontsize=11)
    ax7b.set_ylabel('Tempo (ms)', fontsize=11)
    ax7b.set_xscale('log')
    ax7b.set_yscale('log')
    ax7b.legend(fontsize=9)
    ax7b.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('resumo_merge_vs_quick.png', dpi=300, bbox_inches='tight')
    print("✅ Salvo: resumo_merge_vs_quick.png")
    
    # Mostrar todos os gráficos
    plt.show()
    
    print("\n" + "="*60)
    print("🎉 TODOS OS GRÁFICOS FORAM GERADOS COM SUCESSO!")
    print("="*60)
    print("\nArquivos gerados:")
    print("1. tempo_random_comparacao.png - Comparação log e linear")
    print("2. comparacao_padroes_n2000.png - Barras para n=2000")
    print("3. memoria_vs_tamanho.png - Uso de memória")
    print("4. comparacoes_vs_tamanho.png - Número de comparações")
    print("6. analise_por_padrao.png - Análise por padrão de entrada")
    print("7. resumo_merge_vs_quick.png - Merge vs Quick Sort")

# Executar a geração dos gráficos
if __name__ == "__main__":
    print("🚀 Iniciando geração de gráficos...")
    generate_enhanced_graphs()