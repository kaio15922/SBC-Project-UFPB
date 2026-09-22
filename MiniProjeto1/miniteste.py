#pip install experta
#pip install --upgrade frozendict

# Mini-Projeto 1 da disciplina de Sistemas baseados em Conhecimento

from experta import KnowledgeEngine, Rule, Fact, MATCH, AS
from experta import P, AND

class Jogador(Fact):
    """Um jogador de CS com os seus atributos contextuais (lado, dinheiro, funcao, tipo_round)."""
    pass

class MotorDeRegrasCS(KnowledgeEngine):

    # ==========================================
    # NÍVEL 1: Avaliação de Economia e Perfil
    # ==========================================

    @Rule(Jogador(tipo_round="pistol", nome=MATCH.nome), salience=30)
    def regra_economia_pistol(self, nome):
        print(f"[R1] {nome} está num round pistol.")
        self.declare(Fact(economia="round_pistol", jogador=nome))

    @Rule(Jogador(dinheiro=P(lambda d: d < 2000), tipo_round="normal", nome=MATCH.nome), salience=30)
    def regra_economia_eco(self, nome):
        print(f"[R2] {nome} tem pouco dinheiro (eco).")
        self.declare(Fact(economia="eco", jogador=nome))

    @Rule(Jogador(dinheiro=P(lambda d: d >= 4750), tipo_round="normal", nome=MATCH.nome), salience=30)
    def regra_economia_rico(self, nome):
        print(f"[R3] {nome} tem saldo para compra total (full buy).")
        self.declare(Fact(economia="full_buy", jogador=nome))

    @Rule(Jogador(funcao="awper", nome=MATCH.nome), salience=30)
    def regra_perfil_sniper(self, nome):
        print(f"[R4] {nome} atua como Sniper.")
        self.declare(Fact(perfil="sniper", jogador=nome))

    @Rule(Jogador(funcao=P(lambda f: f not in ["awper", "igl-rifler"]), nome=MATCH.nome), salience=30)
    def regra_perfil_atirador(self, nome):
        print(f"[R5] {nome} atua como Atirador de Assalto (Rifler/Entry/Lurker).")
        self.declare(Fact(perfil="atirador", jogador=nome))

    @Rule(Jogador(funcao="igl-rifler", nome=MATCH.nome), salience=30)
    def regra_perfil_igl(self, nome):
        print(f"[R5b] {nome} atua como IGL.")
        self.declare(Fact(perfil="igl-rifler", jogador=nome))

    # ==========================================
    # NÍVEL 2: Definição da Intenção Tática
    # ==========================================

    @Rule(Fact(economia="round_pistol", jogador=MATCH.nome), salience=20)
    def regra_tatica_pistol(self, nome):
        print(f"[R6] {nome} -> tática: Rush B padrão.")
        self.declare(Fact(tatica="compra_inicial", jogador=nome))

    @Rule(AND(Fact(economia="eco", jogador=MATCH.nome),
              Fact(perfil=P(lambda p: p != "igl-rifler"), jogador=MATCH.nome)), salience=20)
    def regra_tatica_poupanca(self, nome):
        print(f"[R7] {nome} -> tática: economico.")
        self.declare(Fact(tatica="economico", jogador=nome))

    @Rule(AND(Fact(economia="full_buy", jogador=MATCH.nome),
              Fact(perfil="sniper", jogador=MATCH.nome)), salience=20)
    def regra_tatica_investimento_pesado(self, nome):
        print(f"[R8] {nome} -> tática: investimento alto.")
        self.declare(Fact(tatica="investimento_pesado", jogador=nome))

    @Rule(AND(Fact(economia="full_buy", jogador=MATCH.nome),
              Fact(perfil="atirador", jogador=MATCH.nome)), salience=20)
    def regra_tatica_investimento_padrao(self, nome):
        print(f"[R9] {nome} -> tática: padrão de mapa.")
        self.declare(Fact(tatica="investimento_padrao", jogador=nome))

    @Rule(AND(Fact(economia="eco", jogador=MATCH.nome),
              Fact(perfil="igl-rifler", jogador=MATCH.nome)), salience=20)
    def regra_tatica_igl_suporte(self, nome):
        print(f"[R10] {nome} -> tática: preparação de jogada.")
        self.declare(Fact(tatica="suporte_tatico", jogador=nome))

    # ==========================================
    # NÍVEL 3: Decisão Final de Equipamento
    # ==========================================

    @Rule(Fact(tatica="compra_inicial", jogador=MATCH.nome), salience=10)
    def regra_final_colete(self, nome):
        print(f"DECISÃO: {nome} compra Colete 1 porque as regras R1 e R6 dispararam.")

    @Rule(Fact(tatica="economico", jogador=MATCH.nome), salience=10)
    def regra_final_poupanca(self, nome):
        print(f"DECISÃO: {nome} compra Five-Seven ou nada porque as regras R2 e R7 dispararam.")

    @Rule(AND(Fact(tatica="investimento_pesado", jogador=MATCH.nome),
              Jogador(lado="CT", nome=MATCH.nome)), salience=10)
    def regra_final_awp_ct(self, nome):
        print(f"DECISÃO: {nome} compra AWP + Colete 2 porque as regras R3, R4 e R8 dispararam.")

    @Rule(AND(Fact(tatica="investimento_padrao", jogador=MATCH.nome),
              Jogador(lado="TR", nome=MATCH.nome)), salience=10)
    def regra_final_ak_tr(self, nome):
        print(f"DECISÃO: {nome} compra AK + Colete + Granadas porque as regras R3, R5 e R9 dispararam.")

    @Rule(Fact(tatica="suporte_tatico", jogador=MATCH.nome), salience=10)
    def regra_final_deagle_smoke(self, nome):
        print(f"DECISÃO: {nome} compra Deagle e smoke porque as regras R2, R5b e R10 dispararam.")


# ==========================================
# CASOS DE TESTE COMENTADOS
# ==========================================
engine = MotorDeRegrasCS()

print("--- TESTE 1: Round de Pistolas ---")
engine.reset()
engine.declare(Jogador(nome="FalleN", lado="TR", dinheiro=800, funcao="igl-rifler", tipo_round="pistol"))
engine.run()

print("\n--- TESTE 2: AWPer CT full buy ---")
engine.reset()
engine.declare(Jogador(nome="S1mple", lado="CT", dinheiro=6000, funcao="awper", tipo_round="normal"))
engine.run()

print("\n--- TESTE 3: Rifler TR full buy ---")
engine.reset()
engine.declare(Jogador(nome="NiKo", lado="TR", dinheiro=5000, funcao="rifler", tipo_round="normal"))
engine.run()

print("\n--- TESTE 4: IGL em Eco ---")
engine.reset()
engine.declare(Jogador(nome="Karrigan", lado="TR", dinheiro=1500, funcao="igl-rifler", tipo_round="normal"))
engine.run()