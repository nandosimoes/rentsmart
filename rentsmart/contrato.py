"""Taxa contratual — custo separado do aluguel mensal."""

from decimal import Decimal

from .imoveis import arredondar


class TaxaContratual:
    """Taxa de contrato de R$ 2.000,00, parcelável em até 5 vezes."""

    VALOR_PADRAO = Decimal("2000.00")
    MAX_PARCELAS = 5

    def __init__(self, parcelas: int = 1, valor: Decimal = VALOR_PADRAO):
        if not 1 <= parcelas <= self.MAX_PARCELAS:
            raise ValueError(f"A taxa contratual pode ser paga em 1 a {self.MAX_PARCELAS} parcelas.")
        self.valor = arredondar(Decimal(valor))
        self.parcelas = parcelas

    def valores_parcelas(self) -> list[Decimal]:
        """Lista com o valor de cada parcela.

        Quando a divisão não é exata (ex.: 2000 / 3), a diferença de
        centavos vai para a última parcela, garantindo que a soma seja
        exatamente o valor da taxa.
        """
        parcela = arredondar(self.valor / self.parcelas)
        valores = [parcela] * self.parcelas
        valores[-1] = self.valor - parcela * (self.parcelas - 1)
        return valores

    def parcela_do_mes(self, mes: int) -> Decimal:
        """Valor da taxa cobrado no mês informado (1 = primeiro mês)."""
        if 1 <= mes <= self.parcelas:
            return self.valores_parcelas()[mes - 1]
        return Decimal("0.00")

    def descricao(self) -> str:
        if self.parcelas == 1:
            return "à vista (1x)"
        valores = self.valores_parcelas()
        if len(set(valores)) == 1:
            return f"{self.parcelas}x de R$ {formatar(valores[0])}"
        return f"{self.parcelas}x: " + " + ".join(f"R$ {formatar(v)}" for v in valores)


def formatar(valor: Decimal) -> str:
    """Formata no padrão brasileiro: 1234.5 -> '1.234,50'."""
    texto = f"{valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")
