"""Hierarquia de imóveis da R.M Imóveis.

Cada tipo de imóvel conhece o próprio aluguel-base e as próprias regras
de adicionais e descontos. O restante do sistema trata todos os imóveis
da mesma forma (polimorfismo), chamando apenas ``valor_mensal()`` e
``itens_orcamento()``.
"""

from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

CENTAVOS = Decimal("0.01")


def arredondar(valor: Decimal) -> Decimal:
    """Arredonda um valor monetário para 2 casas decimais."""
    return valor.quantize(CENTAVOS, rounding=ROUND_HALF_UP)


class ItemOrcamento:
    """Uma linha do orçamento: descrição + valor (positivo ou negativo)."""

    def __init__(self, descricao: str, valor: Decimal):
        self.descricao = descricao
        self.valor = arredondar(valor)

    def __repr__(self) -> str:
        return f"ItemOrcamento({self.descricao!r}, {self.valor})"


class Imovel(ABC):
    """Classe base abstrata para qualquer imóvel locável."""

    tipo: str = "Imóvel"
    aluguel_base: Decimal = Decimal("0")

    def __init__(self, quartos: int = 1):
        self.quartos = quartos

    # --- regras específicas: cada subclasse implementa as suas ---
    @abstractmethod
    def calcular_adicionais(self) -> list[ItemOrcamento]:
        """Retorna os acréscimos aplicáveis ao aluguel-base."""

    def calcular_descontos(self, subtotal: Decimal) -> list[ItemOrcamento]:
        """Retorna os descontos aplicáveis. Por padrão, nenhum."""
        return []

    # --- algoritmo comum a todos os imóveis (não se repete) ---
    def itens_orcamento(self) -> list[ItemOrcamento]:
        """Monta a composição completa do aluguel mensal, em ordem."""
        itens = [ItemOrcamento(f"Aluguel-base ({self.descricao()})", self.aluguel_base)]
        itens.extend(self.calcular_adicionais())
        subtotal = sum((i.valor for i in itens), Decimal("0"))
        itens.extend(self.calcular_descontos(subtotal))
        return itens

    def valor_mensal(self) -> Decimal:
        """Valor final do aluguel mensal (base + adicionais - descontos)."""
        return arredondar(sum((i.valor for i in self.itens_orcamento()), Decimal("0")))

    def descricao(self) -> str:
        sufixo = "quarto" if self.quartos == 1 else "quartos"
        return f"{self.tipo} de {self.quartos} {sufixo}"


class ImovelComGaragem(Imovel):
    """Base para casas e apartamentos, que compartilham a regra de 1 vaga."""

    valor_garagem = Decimal("300.00")
    adicional_segundo_quarto = Decimal("0")

    def __init__(self, quartos: int = 1, garagem: bool = False):
        if quartos not in (1, 2):
            raise ValueError("Casas e apartamentos podem ter 1 ou 2 quartos.")
        super().__init__(quartos)
        self.garagem = garagem

    def calcular_adicionais(self) -> list[ItemOrcamento]:
        adicionais = []
        if self.quartos == 2:
            adicionais.append(ItemOrcamento("Adicional por 2 quartos", self.adicional_segundo_quarto))
        if self.garagem:
            adicionais.append(ItemOrcamento("Vaga de garagem", self.valor_garagem))
        return adicionais


class Apartamento(ImovelComGaragem):
    tipo = "Apartamento"
    aluguel_base = Decimal("700.00")
    adicional_segundo_quarto = Decimal("200.00")
    percentual_desconto_sem_criancas = Decimal("0.05")

    def __init__(self, quartos: int = 1, garagem: bool = False, possui_criancas: bool = True):
        super().__init__(quartos, garagem)
        self.possui_criancas = possui_criancas

    def calcular_descontos(self, subtotal: Decimal) -> list[ItemOrcamento]:
        # O desconto incide sobre o valor já com os adicionais.
        if self.possui_criancas:
            return []
        desconto = arredondar(subtotal * self.percentual_desconto_sem_criancas)
        return [ItemOrcamento("Desconto de 5% (sem crianças)", -desconto)]


class Casa(ImovelComGaragem):
    tipo = "Casa"
    aluguel_base = Decimal("900.00")
    adicional_segundo_quarto = Decimal("250.00")


class Estudio(Imovel):
    tipo = "Estúdio"
    aluguel_base = Decimal("1200.00")
    valor_pacote_estacionamento = Decimal("250.00")  # inclui 2 vagas
    vagas_no_pacote = 2
    valor_vaga_adicional = Decimal("60.00")

    def __init__(self, pacote_estacionamento: bool = False, vagas_adicionais: int = 0):
        super().__init__(quartos=1)
        if vagas_adicionais < 0:
            raise ValueError("O número de vagas adicionais não pode ser negativo.")
        if vagas_adicionais > 0 and not pacote_estacionamento:
            raise ValueError("Vagas adicionais exigem o pacote inicial de 2 vagas.")
        self.pacote_estacionamento = pacote_estacionamento
        self.vagas_adicionais = vagas_adicionais

    def descricao(self) -> str:
        return self.tipo

    def total_vagas(self) -> int:
        if not self.pacote_estacionamento:
            return 0
        return self.vagas_no_pacote + self.vagas_adicionais

    def calcular_adicionais(self) -> list[ItemOrcamento]:
        adicionais = []
        if self.pacote_estacionamento:
            adicionais.append(ItemOrcamento("Pacote de estacionamento (2 vagas)", self.valor_pacote_estacionamento))
        if self.vagas_adicionais:
            adicionais.append(ItemOrcamento(
                f"{self.vagas_adicionais} vaga(s) adicional(is) x R$ 60,00",
                self.valor_vaga_adicional * self.vagas_adicionais,
            ))
        return adicionais
