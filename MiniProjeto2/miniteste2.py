import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

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

# 6. Função Utilitária para Testes
def testar_dificuldade(p_pontuacao, p_precisao):
    simulador.input['pontuacao'] = p_pontuacao
    simulador.input['precisao'] = p_precisao
    simulador.compute()
    resultado = simulador.output['dificuldade']
    
    print(f"Entradas -> Pontuação: {p_pontuacao} | Precisão: {p_precisao}%")
    print(f"Saída    -> Dificuldade ajustada para: {resultado:.2f}/100\n")
    return resultado

# Executando os Casos de Teste
if __name__ == "__main__":
    print("--- CASOS DE TESTE ---")
    
    # Caso 1: O exemplo exato que você propôs
    testar_dificuldade(80, 75)
    
    # Caso 2: Jogador com muita dificuldade (Sofrendo muito)
    testar_dificuldade(15, 20)
    
    # Caso 3: Jogador mediano com precisão razoável
    testar_dificuldade(45, 60)
    
    # Opcional: Gerar gráfico da saída do Caso 3
    # dificuldade.view(sim=simulador)
    # plt.show() # Necessário importar matplotlib.pyplot as plt