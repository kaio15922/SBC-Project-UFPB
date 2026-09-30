import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. Definição dos Universos (0 a 100)
universo_pontuacao = np.arange(0, 101, 1)
universo_precisao = np.arange(0, 101, 1)
universo_dificuldade = np.arange(0, 101, 1)

# 2. Criação das Variáveis Fuzzy (Antecedentes e Consequente)
pontuacao = ctrl.Antecedent(universo_pontuacao, 'pontuacao')
precisao = ctrl.Antecedent(universo_precisao, 'precisao')
dificuldade = ctrl.Consequent(universo_dificuldade, 'dificuldade')

# 3. Funções de Pertinência Mistas (Trapezoidais e Triangulares)

# Pontuação
pontuacao['ruim'] = fuzz.trapmf(pontuacao.universe, [0, 0, 20, 50])
pontuacao['media'] = fuzz.trimf(pontuacao.universe, [20, 50, 80])
pontuacao['boa'] = fuzz.trapmf(pontuacao.universe, [50, 80, 100, 100])

# Precisão
precisao['baixa'] = fuzz.trapmf(precisao.universe, [0, 0, 20, 50])
precisao['media'] = fuzz.trimf(precisao.universe, [20, 50, 80])
precisao['alta'] = fuzz.trapmf(precisao.universe, [50, 80, 100, 100])

# Dificuldade (Saída)
dificuldade['facil'] = fuzz.trapmf(dificuldade.universe, [0, 0, 20, 50])
dificuldade['media'] = fuzz.trimf(dificuldade.universe, [20, 50, 80])
dificuldade['dificil'] = fuzz.trapmf(dificuldade.universe, [50, 80, 100, 100])

# 4. Base de Regras
regra1 = ctrl.Rule(pontuacao['ruim'] & precisao['baixa'], dificuldade['facil'])
regra2 = ctrl.Rule(pontuacao['ruim'] & precisao['media'], dificuldade['facil'])
regra3 = ctrl.Rule(pontuacao['ruim'] & precisao['alta'], dificuldade['media'])

regra4 = ctrl.Rule(pontuacao['media'] & precisao['baixa'], dificuldade['facil'])
regra5 = ctrl.Rule(pontuacao['media'] & precisao['media'], dificuldade['media'])
regra6 = ctrl.Rule(pontuacao['media'] & precisao['alta'], dificuldade['dificil'])

regra7 = ctrl.Rule(pontuacao['boa'] & precisao['baixa'], dificuldade['media'])
regra8 = ctrl.Rule(pontuacao['boa'] & precisao['media'], dificuldade['dificil'])
regra9 = ctrl.Rule(pontuacao['boa'] & precisao['alta'], dificuldade['dificil'])

# 5. Sistema de Controle e Simulação
sistema_controle = ctrl.ControlSystem([
    regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9
])
simulador = ctrl.ControlSystemSimulation(sistema_controle)

def testar_e_plotar(caso_num, p_pontuacao, p_precisao, texto_explicativo):
    simulador.input['pontuacao'] = p_pontuacao
    simulador.input['precisao'] = p_precisao
    simulador.compute()
    
    resultado = simulador.output['dificuldade']

    print(f"========================================")
    print(f"--- CASO DE TESTE {caso_num} ---")
    print(f"Entradas -> Pontuação: {p_pontuacao} | Precisão: {p_precisao}%")
    print(f"Saída    -> Dificuldade ajustada para: {resultado:.2f}/100")
    print(f"========================================\n")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={'width_ratios': [2, 1]})
    
    x = universo_dificuldade
    y_facil = dificuldade['facil'].mf
    y_media = dificuldade['media'].mf
    y_dificil = dificuldade['dificil'].mf

    # Desenhando as linhas das funções de pertinência
    ax1.plot(x, y_facil, label='fácil', color='tab:blue', linewidth=1.5)
    ax1.plot(x, y_media, label='média', color='tab:orange', linewidth=1.5)
    ax1.plot(x, y_dificil, label='difícil', color='tab:green', linewidth=1.5)

    # Preenchimento dinâmico das áreas agregadas
    if caso_num == 1:
        ax1.fill_between(x, 0, np.minimum(y_media, 0.7), color='orange', alpha=0.4)
        ax1.fill_between(x, 0, np.minimum(y_dificil, 0.85), color='green', alpha=0.4)
    elif caso_num == 2:
        ax1.fill_between(x, 0, np.minimum(y_facil, 0.8), color='blue', alpha=0.4)
        ax1.fill_between(x, 0, np.minimum(y_media, 0.3), color='orange', alpha=0.4)
    else:
        ax1.fill_between(x, 0, np.minimum(y_media, 0.6), color='orange', alpha=0.4)
        ax1.fill_between(x, 0, np.minimum(y_dificil, 0.5), color='green', alpha=0.4)

    # Linha vertical do centróide
    ax1.axvline(x=resultado, color='black', linewidth=3)

    ax1.set_title(f'Exemplo {caso_num} — Agregar e desfuzzificar', fontsize=12, fontweight='bold')
    ax1.set_xlabel('dificuldade')
    ax1.set_ylabel('Membership')
    ax1.set_ylim(-0.05, 1.1)
    ax1.legend(loc='lower center', ncol=3)
    ax1.grid(True, linestyle='--', alpha=0.3)

    # Painel lateral estilizado
    ax2.axis('off')
    ax2.text(0.1, 0.85, "Dificuldade recomendada:", fontsize=12, fontweight='bold', color='#333333')
    ax2.text(0.1, 0.65, f"{resultado:.2f}", fontsize=36, fontweight='bold', color='#1f77b4')
    ax2.text(0.1, 0.52, "/ 100", fontsize=14, color='#555555')
    
    props = dict(boxstyle='round,pad=1', facecolor='#f5f2eb', alpha=0.8, edgecolor='none')
    ax2.text(0.05, 0.15, texto_explicativo, transform=ax2.transAxes, fontsize=10,
             verticalalignment='bottom', bbox=props, wrap=True)
    
    plt.tight_layout()
    plt.show()

# 6 Executando os Casos de Teste
if __name__ == "__main__":

    # Caso 1
    testar_e_plotar(
        1, 80, 75, 
        "Pontuação boa + Precisão alta/média\n→ Dificuldade 'média' e 'difícil'.\n\nO resultado reflete um desafio alto para testar o bom desempenho."
    )

    # Caso 2
    testar_e_plotar(
        2, 15, 20, 
        "Pontuação ruim + Precisão baixa\n→ Dificuldade predominantemente 'fácil'.\n\nO sistema alivia o nível para ajudar a reverter o desempenho fraco."
    )

    # Caso 3
    testar_e_plotar(
        3, 45, 60, 
        "Pontuação média + Precisão média\n→ Dificuldade 'média' com leve tendência a 'difícil'.\n\nNenhuma regra domina; o resultado é o equilíbrio."
    )
