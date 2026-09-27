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
    
    # Caso 1: Jogador de alto nível (Ativa os conjuntos "Boa" e "Alta")
    # O controlador deve elevar a dificuldade em direção ao máximo para manter o engajamento.
    testar_dificuldade(80, 75)
    
    # Caso 2: Jogador com desempenho crítico (Ativa os conjuntos "Ruim" e "Baixa")
    # O controlador deve ancorar o jogo no nível Fácil para evitar a frustração do usuário.
    testar_dificuldade(15, 20)
    
    # Caso 3: Jogador casual com progresso estável (Ativa o conjunto "Média")
    # O controlador deve entregar um desafio perfeitamente equilibrado, próximo ao centro de massa.
    testar_dificuldade(45, 60)
    
    # Caso 4: Jogador "Spammer" (Ativa os conjuntos "Boa" e "Baixa")
    # Alta eficácia de pontuação, mas baixa eficiência mecânica (ex: atira para todo lado).
    # O sistema aplica uma dificuldade moderada para compensar a imprecisão sem desvalorizar o progresso.
    testar_dificuldade(90, 15)

    # Caso 5: Jogador "Camper" ou passivo (Ativa os conjuntos "Ruim" e "Alta")
    # Taxa de acerto impecável, porém com pouquíssimo impacto no progresso do jogo.
    # O sistema restringe o aumento drástico da dificuldade, reconhecendo que o jogador ainda não domina o mapa.
    testar_dificuldade(10, 95)
