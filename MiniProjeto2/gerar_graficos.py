import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# 1. Definir o Universo (0 a 100)
x = np.arange(0, 101, 1)

# 2. Criar os conjuntos Fuzzy com a abordagem Mista
# Trapézio na esquerda [0, 0, 20, 50]
# Triângulo no meio [20, 50, 80]
# Trapézio na direita [50, 80, 100, 100]
conjunto_baixo = fuzz.trapmf(x, [0, 0, 20, 50])
conjunto_medio = fuzz.trimf(x, [20, 50, 80])
conjunto_alto  = fuzz.trapmf(x, [50, 80, 100, 100])

# 3. Função utilitária para desenhar e guardar os gráficos silenciosamente
def plot_variavel_fuzzy(nome_variavel, label_baixo, label_medio, label_alto, nome_ficheiro):
    plt.figure(figsize=(8, 4))
    
    # Linhas dos conjuntos
    plt.plot(x, conjunto_baixo, 'r', linewidth=2, label=f'{label_baixo} (Trapézio)')
    plt.plot(x, conjunto_medio, 'g', linewidth=2, label=f'{label_medio} (Triângulo)')
    plt.plot(x, conjunto_alto, 'b', linewidth=2, label=f'{label_alto} (Trapézio)')
    
    # Preenchimento das áreas
    plt.fill_between(x, 0, conjunto_baixo, color='r', alpha=0.1)
    plt.fill_between(x, 0, conjunto_medio, color='g', alpha=0.1)
    plt.fill_between(x, 0, conjunto_alto, color='b', alpha=0.1)
    
    # Formatação do gráfico
    plt.title(f'Variável Linguística: {nome_variavel}', fontsize=14, fontweight='bold')
    plt.xlabel('Valor (0-100)', fontsize=12)
    plt.ylabel('Grau de Pertinência ($\mu$)', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xlim(0, 100)
    plt.ylim(0, 1.05)
    plt.tight_layout()
    
    # Salvar imagem diretamente
    plt.savefig(nome_ficheiro, dpi=150)
    print(f"Gráfico salvo como: {nome_ficheiro}")
    
    # Limpar a figura da memória (sem abrir pop-up)
    plt.close()

if __name__ == "__main__":
    print("Gerando os gráficos dos conjuntos fuzzy em segundo plano...")
    
    # Gerar gráfico 1: Pontuação (Entrada 1)
    plot_variavel_fuzzy('Pontuação', 'Ruim', 'Média', 'Boa', 'fuzzy_pontuacao.png')
    
    # Gerar gráfico 2: Precisão (Entrada 2)
    plot_variavel_fuzzy('Precisão', 'Baixa', 'Média', 'Alta', 'fuzzy_precisao.png')
    
    # Gerar gráfico 3: Dificuldade (Saída)
    plot_variavel_fuzzy('Dificuldade (Saída)', 'Fácil', 'Média', 'Difícil', 'fuzzy_dificuldade.png')
    
    print("Concluído! Os arquivos .png estão na sua pasta.")