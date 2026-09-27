# Miniprojeto 2: Controlador Fuzzy para Ajuste Dinâmico de Dificuldade em Jogos
**Disciplina:** Sistemas Baseados em Conhecimento (SBC)

## 1. Introdução
Este projeto propõe um sistema de inferência Fuzzy (Mamdani) desenhado para ajustar a dificuldade de um jogo em tempo real, baseando-se no desempenho contínuo do jogador. O objetivo é manter o estado de "Flow" do usuário, evitando frustração extrema (jogo muito difícil para iniciantes) ou tédio (jogo muito fácil para veteranos).

## 2. Definição do Domínio
O sistema utiliza duas variáveis de entrada para capturar a eficácia e a eficiência do jogador, e uma variável de saída correspondente à dificuldade do sistema. Todas as variáveis operam em um universo de discurso de 0 a 100.

### Entradas (Antecedentes)
*   **Pontuação (0 a 100):** Mede o impacto geral do jogador e o cumprimento de objetivos (ex: K/D ratio, progressão de mapa).
    *   Conjuntos: `Ruim`, `Média`, `Boa`.
*   **Precisão (0 a 100%):** Mede a eficiência mecânica e a taxa de acertos, filtrando jogadores que avançam apenas por tentativa e erro.
    *   Conjuntos: `Baixa`, `Média`, `Alta`.
 
<img width="1200" height="600" alt="fuzzy_pontuacao" src="https://github.com/user-attachments/assets/48e59fed-8d61-4089-b87f-b39e96894b5c" />

<img width="1200" height="600" alt="fuzzy_precisao" src="https://github.com/user-attachments/assets/e0d0e7a8-3999-4ceb-9246-4d65939c6cc6" />

### Saída (Consequente)
*   **Dificuldade (0 a 100):** O nível de desafio imposto pela inteligência artificial do jogo (ex: dano dos inimigos, tempo de reação).
    *   Conjuntos: `Fácil`, `Média`, `Difícil`.

<img width="1200" height="600" alt="fuzzy_dificuldade" src="https://github.com/user-attachments/assets/383388ae-7bf4-44bc-9adb-ec4096f20adc" />

## 3. Base de Regras
Foi definida uma matriz de 9 regras conectadas pelo operador lógico `E` (AND) para garantir transições suaves:

1. SE Pontuação é Ruim E Precisão é Baixa ENTÃO Dificuldade é Fácil.
2. SE Pontuação é Ruim E Precisão é Média ENTÃO Dificuldade é Fácil.
3. SE Pontuação é Ruim E Precisão é Alta ENTÃO Dificuldade é Média.
4. SE Pontuação é Média E Precisão é Baixa ENTÃO Dificuldade é Fácil.
5. SE Pontuação é Média E Precisão é Média ENTÃO Dificuldade é Média.
6. SE Pontuação é Média E Precisão é Alta ENTÃO Dificuldade é Difícil.
7. SE Pontuação é Boa E Precisão é Baixa ENTÃO Dificuldade é Média.
8. SE Pontuação é Boa E Precisão é Média ENTÃO Dificuldade é Difícil.
9. SE Pontuação é Boa E Precisão é Alta ENTÃO Dificuldade é Difícil.

## 4. Análise Crítica e Evolução do Modelo (Triângulos vs. Trapézios)
Durante a fase de testes e validação da defuzzificação (método do centróide), identificou-se uma limitação matemática ao utilizar exclusivamente funções de pertinência triangulares (`trimf`).

### O Problema da Abordagem 100% Triangular
Com bases triangulares indo de 0 a 100, a área da função central ("Média") exercia uma força gravitacional desproporcional sobre o centro de massa da área agregada. Isso impedia que a saída atingisse as extremidades lógicas do universo.
*   **Cenário de Teste (Alta Performance):** Pontuação = 80, Precisão = 75%.
*   **Saída Obtida:** Dificuldade = 57.04/100.
*   **Análise:** Um jogador com desempenho inegavelmente bom estava receben
do uma dificuldade marginalmente acima da média, falhando no propósito do sistema. O mesmo ocorreu para desempenhos muito ruins (Pontuação = 15, Precisão = 20%), resultando em uma dificuldade de 38.96, que não aliviava a pressão sobre o jogador adequadamente.

<img width="338" height="144" alt="image" src="https://github.com/user-attachments/assets/025f02c3-214a-44e0-b484-554aa8452151" />

### A Solução: Funções de Pertinência Mistas (Trapézios nas Pontas)
Para corrigir o deslocamento do centróide, o modelo foi refatorado substituindo as funções triangulares das extremidades (`Ruim`/`Boa`, `Baixa`/`Alta`, `Fácil`/`Difícil`) por funções trapezoidais (`trapmf`), mantendo a função triangular apenas no conjunto central (`Média`).

**Parâmetros Trapezoidais (Cortes em 20 e 80):**
*   Ruim / Baixa / Fácil: `[0, 0, 20, 50]`
*   Boa / Alta / Difícil: `[50, 80, 100, 100]`

**Resultados Pós-Refatoração:**
Ao garantir um "platô" de pertinência absoluta (grau 1.0) entre 0-20 e 80-100, a área geométrica nas extremidades aumentou, permitindo que o cálculo do centróide refletisse a realidade das regras extremas.
*   **Cenário 1 (Alta Performance):** Pontuação 80, Precisão 75% ➔ **Dificuldade Ajustada: 80.56/100** (Desempenho excelente reflete em dificuldade legitimamente difícil).
*   **Cenário 2 (Baixa Performance):** Pontuação 15, Precisão 20% ➔ **Dificuldade Ajustada: 18.57/100** (Dificuldade cai drasticamente para ajudar o jogador).
*   **Cenário 3 (Performance Mediana):** Pontuação 45, Precisão 60% ➔ **Dificuldade Ajustada: 54.28/100** (A transição pelo centro mantém a estabilidade triangular).

<img width="324" height="141" alt="image" src="https://github.com/user-attachments/assets/04d13d04-d878-482e-b05e-1a1d1e3cf814" />

Para validar a robustez do controlador Fuzzy em relação a cenários onde as variáveis de entrada entram em "conflito" (uma é extremamente alta e a outra é extremamente baixa), foram introduzidos dois casos de teste adicionais. Estes casos demonstram a superioridade da Lógica Fuzzy frente a condicionais booleanas tradicionais (`if/else`).

*   **Caso 4: O "Spammer" (Alta Pontuação, Baixa Precisão)**
    *   **Entradas:** Pontuação = 90 | Precisão = 15%
    *   **Comportamento:** Representa o jogador que avança de forma caótica. Em um cenário de jogo de tiro (como *Counter-Strike*), seria o jogador que consegue eliminações, mas gasta múltiplos carregadores atirando a esmo. 
    *   **Decisão do Controlador:** Ativa as regras associadas a "Boa" e "Baixa". O sistema reconhece a eficácia no placar, mas pune a falta de eficiência mecânica, convergindo a saída para a dificuldade **Média**. O jogo não atinge a dificuldade máxima, exigindo que o jogador melhore sua técnica antes de enfrentar o maior desafio.

*   **Caso 5: O Jogador Passivo / "Camper" (Baixa Pontuação, Alta Precisão)**
    *   **Entradas:** Pontuação = 10 | Precisão = 95%
    *   **Comportamento:** Representa o jogador extremamente cauteloso ou inativo. Ele pode acertar um tiro cirúrgico (alta precisão), mas não contribui para o progresso da fase ou para o objetivo da partida (baixa pontuação geral).
    *   **Decisão do Controlador:** Ativa as regras associadas a "Ruim" e "Alta". O motor Mamdani entende que a precisão mecânica não justifica punir o jogador com uma dificuldade elevada, já que ele mal consegue progredir no mapa. A saída converge para a dificuldade **Média**, instigando o jogador a sair da inércia sem sobrecarregá-lo.

## 5. Instruções de Execução (Build e Testes)

O projeto foi desenvolvido em Python 3.x. Siga os passos abaixo para preparar o ambiente e rodar as simulações do motor de inferência.

### 5.1. Preparando o Ambiente Virtual (Opcional, mas recomendado)

Abra o terminal no diretório raiz do projeto e crie um ambiente virtual para isolar as dependências:

```bash
# Criar o ambiente virtual (Windows/Linux/macOS)
python -m venv venv

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar no Linux/macOS
source venv/bin/activate
```

### 5.2. Instalando as Dependências

O sistema utiliza a biblioteca scikit-fuzzy para a lógica difusa, o numpy para operações numéricas e o matplotlib para a renderização dos gráficos de pertinência. Instale-os via pip:

```bash
pip install numpy scikit-fuzzy matplotlib
```

### 5.3. Executando os Casos de Teste (Motor de Inferência)

Para rodar as simulações e verificar a saída de dificuldade baseada na pontuação e precisão do jogador, execute o script de testes (certifique-se de usar o nome correto do seu arquivo, ex: miniteste2.py):

```bash
python miniteste2.py
```

O console exibirá os resultados do cálculo do centróide para cada cenário configurado no código.

### 5.4. Gerando os Gráficos dos Conjuntos Fuzzy

Para gerar as representações visuais das funções trapezoidais e triangulares (.png) diretamente na pasta do projeto (de forma silenciosa), execute:

```bash
python gerar_graficos.py
```

## 6. Conclusão

A implementação do controlador Fuzzy em Python (scikit-fuzzy) provou ser uma arquitetura leve e altamente eficaz para tomadas de decisão que envolvem graus de incerteza no comportamento humano. A calibração geométrica dos conjuntos linguísticos demonstrou na prática como a modelagem da base matemática impacta diretamente a resposta do agente autônomo, resultando em um sistema robusto e pronto para integração.
