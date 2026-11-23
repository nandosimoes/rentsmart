"""Ponto de entrada do RentSmart.

Uso:
    python main.py            # modo interativo
    python main.py --demo     # gera um orçamento de exemplo sem perguntas
"""

import sys
from datetime import datetime
from pathlib import Path

from rentsmart import Apartamento, Casa, Estudio, Orcamento, TaxaContratual
from rentsmart.entrada import EntradaUsuario

PASTA_SAIDA = Path(__file__).parent / "saida"


class AplicacaoRentSmart:
    """Conduz o atendimento: coleta dados, monta o orçamento e gera o CSV."""

    TIPOS = {"apartamento": "Apartamento (R$ 700,00)",
             "casa": "Casa (R$ 900,00)",
             "estudio": "Estúdio (R$ 1.200,00)"}

    def __init__(self, entrada: EntradaUsuario | None = None):
        self.entrada = entrada or EntradaUsuario()

    def criar_imovel(self):
        tipo = self.entrada.opcao("\nQual o tipo de imóvel?", self.TIPOS)
        if tipo == "estudio":
            pacote = self.entrada.sim_nao("Deseja o pacote de estacionamento com 2 vagas (R$ 250,00)?")
            extras = 0
            if pacote:
                extras = self.entrada.inteiro("Quantas vagas adicionais (R$ 60,00 cada)? [0 a 10]: ", 0, 10)
            return Estudio(pacote_estacionamento=pacote, vagas_adicionais=extras)

        quartos = self.entrada.inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = self.entrada.sim_nao("Deseja vaga de garagem (R$ 300,00)?")
        if tipo == "casa":
            return Casa(quartos=quartos, garagem=garagem)
        criancas = self.entrada.sim_nao("O cliente possui crianças?")
        return Apartamento(quartos=quartos, garagem=garagem, possui_criancas=criancas)

    def criar_taxa(self) -> TaxaContratual:
        parcelas = self.entrada.inteiro(
            "Em quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00? [1 a 5]: ", 1, 5)
        return TaxaContratual(parcelas=parcelas)

    def gerar(self, orcamento: Orcamento) -> Path:
        print("\n" + orcamento.resumo())
        nome = f"projecao_12_meses_{datetime.now():%Y%m%d_%H%M%S_%f}.csv"
        caminho = orcamento.exportar_csv(PASTA_SAIDA / nome)
        print(f"\nProjeção de 12 meses salva em: {caminho}")
        return caminho

    def executar(self) -> None:
        print("=" * 62)
        print("Bem-vindo ao RentSmart — R.M Imóveis".center(62))
        print("=" * 62)
        while True:
            cliente = self.entrada.texto("\nNome do cliente: ")
            imovel = self.criar_imovel()
            taxa = self.criar_taxa()
            self.gerar(Orcamento(cliente, imovel, taxa))
            if not self.entrada.sim_nao("\nDeseja fazer outro orçamento?"):
                print("Obrigado por usar o RentSmart!")
                break


def demo() -> None:
    orcamento = Orcamento("Cliente Exemplo",
                          Apartamento(quartos=2, garagem=True, possui_criancas=False),
                          TaxaContratual(parcelas=4))
    AplicacaoRentSmart().gerar(orcamento)


if __name__ == "__main__":
    try:
        demo() if "--demo" in sys.argv else AplicacaoRentSmart().executar()
    except (KeyboardInterrupt, EOFError):
        print("\nAtendimento encerrado.")
