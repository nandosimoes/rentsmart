"""Orçamento de locação: junta imóvel + taxa contratual e gera as saídas."""

import csv
from decimal import Decimal
from pathlib import Path

from .contrato import TaxaContratual, formatar
from .imoveis import Imovel

MESES_PROJECAO = 12


class Orcamento:
    """Orçamento completo de uma locação."""

    def __init__(self, cliente: str, imovel: Imovel, taxa: TaxaContratual):
        self.cliente = cliente
        self.imovel = imovel
        self.taxa = taxa

    def valor_aluguel_mensal(self) -> Decimal:
        return self.imovel.valor_mensal()

    def projecao(self, meses: int = MESES_PROJECAO) -> list[dict]:
        """Projeção mês a mês: aluguel, parcela da taxa, total e acumulado."""
        linhas = []
        acumulado = Decimal("0.00")
        aluguel = self.valor_aluguel_mensal()
        for mes in range(1, meses + 1):
            parcela = self.taxa.parcela_do_mes(mes)
            total = aluguel + parcela
            acumulado += total
            linhas.append({
                "mes": mes,
                "aluguel": aluguel,
                "parcela_taxa": parcela,
                "total_mes": total,
                "acumulado": acumulado,
            })
        return linhas

    def total_primeiro_ano(self) -> Decimal:
        return self.projecao()[-1]["acumulado"]

    def resumo(self) -> str:
        """Texto do orçamento detalhado, pronto para exibir no terminal."""
        largura = 62
        linha = "-" * largura
        partes = [
            "=" * largura,
            "RENTSMART — R.M IMÓVEIS | ORÇAMENTO DE LOCAÇÃO".center(largura),
            "=" * largura,
            f"Cliente: {self.cliente}",
            f"Imóvel : {self.imovel.descricao()}",
            linha,
            "COMPOSIÇÃO DO ALUGUEL MENSAL",
        ]
        for item in self.imovel.itens_orcamento():
            sinal = "-" if item.valor < 0 else " "
            partes.append(f"  {item.descricao:<42}{sinal}R$ {formatar(abs(item.valor)):>10}")
        partes += [
            linha,
            f"  {'ALUGUEL MENSAL':<42} R$ {formatar(self.valor_aluguel_mensal()):>10}",
            linha,
            "TAXA CONTRATUAL (cobrada à parte do aluguel)",
            f"  {'Valor total da taxa':<42} R$ {formatar(self.taxa.valor):>10}",
            f"  Parcelamento: {self.taxa.descricao()}",
            linha,
            f"  {'Total previsto no 1º ano':<42} R$ {formatar(self.total_primeiro_ano()):>10}",
            "=" * largura,
        ]
        return "\n".join(partes)

    def exportar_csv(self, caminho: str | Path) -> Path:
        """Grava a projeção de 12 meses em CSV (separador ';', abre no Excel)."""
        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mês", "Aluguel (R$)", "Parcela taxa contratual (R$)",
                               "Total do mês (R$)", "Total acumulado (R$)"])
            for l in self.projecao():
                escritor.writerow([l["mes"], formatar(l["aluguel"]), formatar(l["parcela_taxa"]),
                                   formatar(l["total_mes"]), formatar(l["acumulado"])])
        return caminho
