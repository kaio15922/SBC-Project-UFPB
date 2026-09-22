# Mini-Projeto 1: Sistema Especialista em Compras no Counter-Strike (CS)

## Descrição do Domínio
Este projeto implementa um Sistema Baseado em Conhecimento (SBC) de regras IF-THEN utilizando a biblioteca `experta` em Python. O domínio escolhido foi a **Tomada de Decisão Econômica e Tática no Counter-Strike**. 

No CS, as compras de equipamentos no início de cada rodada são vitais e dependem de múltiplos fatores contextuais. O sistema atua como um "Assistente de IGL (In-Game Leader)", avaliando o lado da equipe (CT/TR), o dinheiro disponível, a função do jogador e o tipo de round, para recomendar a melhor compra e postura tática, simulando o raciocínio de um jogador experiente.

O sistema opera em 3 níveis de encadeamento:
1. **Nível 1:** Avaliação da situação econômica e do perfil do jogador.
2. **Nível 2:** Definição da intenção tática da rodada.
3. **Nível 3:** Decisão final do equipamento a ser comprado.

Para a resolução de conflitos e ordenação lógica do raciocínio, o sistema utiliza ativamente o parâmetro `salience` (prioridade).

---

## Listagem das Regras em Linguagem Natural

O sistema possui um total de 16 regras. Abaixo estão descritas em linguagem natural:

**Nível 1: Economia e Perfil (Prioridade Alta)**
1. **Regra Economia Pistol:** SE o tipo de round é "pistol", ENTÃO a economia é classificada como "round pistol".
2. **Regra Economia Eco:** SE o dinheiro do jogador é menor que 2000, ENTÃO a economia é classificada como "eco" (pouco dinheiro).
3. **Regra Economia Rico:** SE o dinheiro do jogador é maior ou igual a 4750, ENTÃO a economia é "full buy" (compra total).
4. **Regra Perfil Sniper:** SE a função do jogador é "awper", ENTÃO o seu perfil de jogo é "sniper".
5. **Regra Perfil Atirador:** SE a função do jogador NÃO é "awper" E NÃO É "igl-rifler", ENTÃO o perfil é "atirador de assalto".
6. **Regra Perfil IGL:** SE a função do jogador é "igl-rifler", ENTÃO o seu perfil de jogo é "igl-rifler".

**Nível 2: Definição da Intenção Tática (Prioridade Média)**
7. **Regra Tática Pistol:** SE a economia é "round pistol", ENTÃO a intenção tática é "compra inicial".
8. **Regra Tática Poupança:** SE a economia é "eco" E o perfil NÃO é "igl-rifler", ENTÃO a intenção tática é "econômico".
9. **Regra Tática Investimento Pesado:** SE a economia é "full buy" E o perfil é "sniper", ENTÃO a intenção tática é de "investimento pesado".
10. **Regra Tática Investimento Padrão:** SE a economia é "full buy" E o perfil é "atirador", ENTÃO a intenção tática é de "investimento padrão".
11. **Regra Tática IGL Suporte:** SE a economia é "eco" E o perfil é "igl-rifler", ENTÃO a intenção tática é de "suporte tático" (preparação de jogada para a equipe).

**Nível 3: Decisão Final de Equipamento (Prioridade Baixa)**
12. **Regra Final Colete:** SE a tática é "compra inicial", ENTÃO a decisão é comprar Colete 1.
13. **Regra Final Poupança:** SE a tática é "econômico", ENTÃO a decisão é comprar uma pistola barata (ex: Five-Seven) ou não comprar nada.
14. **Regra Final AWP CT:** SE a tática é "investimento pesado" E o jogador está do lado "CT", ENTÃO a decisão é comprar uma AWP e Colete 2.
15. **Regra Final AK TR:** SE a tática é "investimento padrão" E o jogador está do lado "TR", ENTÃO a decisão é comprar AK-47, Colete e Granadas.
16. **Regra Final Deagle Smoke:** SE a tática é "suporte tático", ENTÃO a decisão é comprar uma Desert Eagle e uma Smoke.

---

## Casos de Teste

O sistema foi validado com 4 casos de teste que cobrem as diferentes ramificações lógicas do encadeamento (presentes no notebook).

### Teste 1: Round de Pistolas
* **Entrada:** Jogador(nome="FalleN", lado="TR", dinheiro=800, funcao="igl-rifler", tipo_round="pistol")
* **Raciocínio Esperado:** O sistema identifica o round pistol (R1) e define a tática de compra inicial (R6).
* **Saída Esperada:** O jogador "FalleN" deve receber a recomendação de comprar Colete 1, explicando que as regras R1 e R6 dispararam.

### Teste 2: AWPer CT com Economia Alta (Full Buy)
* **Entrada:** Jogador(nome="S1mple", lado="CT", dinheiro=6000, funcao="awper", tipo_round="normal")
* **Raciocínio Esperado:** O sistema identifica dinheiro suficiente para full buy (R3) e função de sniper (R4). A tática vira investimento alto (R8).
* **Saída Esperada:** O jogador "S1mple" deve receber a recomendação de comprar AWP + Colete 2, justificando com as regras R3, R4 e R8.

### Teste 3: Rifler TR com Economia Alta (Full Buy)
* **Entrada:** Jogador(nome="NiKo", lado="TR", dinheiro=5000, funcao="rifler", tipo_round="normal")
* **Raciocínio Esperado:** O sistema identifica full buy (R3) e perfil de atirador (R5), levando à tática padrão de mapa (R9).
* **Saída Esperada:** O jogador "NiKo" deve comprar AK + Colete + Granadas, embasado pelas regras R3, R5 e R9.

### Teste 4: IGL em Situação de Pouco Dinheiro (Eco)
* **Entrada:** Jogador(nome="Karrigan", lado="TR", dinheiro=1500, funcao="igl-rifler", tipo_round="normal")
* **Raciocínio Esperado:** O sistema nota o pouco dinheiro (R2) e a função de IGL (R5b). Diferente de um jogador comum em eco, a tática muda para suporte tático (R10).
* **Saída Esperada:** O jogador "Karrigan" comprará Deagle e Smoke para auxiliar o time, com base nas regras R2, R5b e R10.