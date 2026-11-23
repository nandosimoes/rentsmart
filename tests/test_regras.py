"""Testes das regras de negócio. Rodar com: python -m unittest -v"""

import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from rentsmart import Apartamento, Casa, Estudio, Orcamento, TaxaContratual
from rentsmart.entrada import EntradaUsuario

D = Decimal


class TestApartamento(unittest.TestCase):
    def test_base(self):
        self.assertEqual(Apartamento().valor_mensal(), D("700.00"))

    def test_dois_quartos_e_garagem(self):
        self.assertEqual(Apartamento(2, garagem=True).valor_mensal(), D("1200.00"))

    def test_desconto_sem_criancas_apos_adicionais(self):
        # (700 + 200 + 300) * 0,95 = 1140
        self.assertEqual(Apartamento(2, True, possui_criancas=False).valor_mensal(), D("1140.00"))

    def test_desconto_simples(self):
        self.assertEqual(Apartamento(possui_criancas=False).valor_mensal(), D("665.00"))

    def test_quartos_invalidos(self):
        with self.assertRaises(ValueError):
            Apartamento(quartos=3)


class TestCasa(unittest.TestCase):
    def test_base(self):
        self.assertEqual(Casa().valor_mensal(), D("900.00"))

    def test_dois_quartos_e_garagem(self):
        self.assertEqual(Casa(2, garagem=True).valor_mensal(), D("1450.00"))

    def test_casa_nao_tem_desconto(self):
        self.assertEqual(Casa(1).calcular_descontos(D("900")), [])


class TestEstudio(unittest.TestCase):
    def test_base(self):
        self.assertEqual(Estudio().valor_mensal(), D("1200.00"))

    def test_pacote(self):
        self.assertEqual(Estudio(True).valor_mensal(), D("1450.00"))
        self.assertEqual(Estudio(True).total_vagas(), 2)

    def test_vagas_adicionais(self):
        self.assertEqual(Estudio(True, 3).valor_mensal(), D("1630.00"))
        self.assertEqual(Estudio(True, 3).total_vagas(), 5)

    def test_extra_sem_pacote(self):
        with self.assertRaises(ValueError):
            Estudio(False, 1)


class TestTaxaContratual(unittest.TestCase):
    def test_parcelas_exatas(self):
        self.assertEqual(TaxaContratual(4).valores_parcelas(), [D("500.00")] * 4)

    def test_parcelas_somam_valor_total(self):
        for n in range(1, 6):
            self.assertEqual(sum(TaxaContratual(n).valores_parcelas()), D("2000.00"))

    def test_limites(self):
        for n in (0, 6):
            with self.assertRaises(ValueError):
                TaxaContratual(n)

    def test_parcela_fora_do_prazo(self):
        self.assertEqual(TaxaContratual(2).parcela_do_mes(3), D("0.00"))


class TestOrcamento(unittest.TestCase):
    def setUp(self):
        self.orc = Orcamento("Teste", Casa(2, True), TaxaContratual(5))

    def test_projecao(self):
        p = self.orc.projecao()
        self.assertEqual(len(p), 12)
        self.assertEqual(p[0]["total_mes"], D("1850.00"))
        self.assertEqual(p[5]["total_mes"], D("1450.00"))
        self.assertEqual(self.orc.total_primeiro_ano(), D("1450") * 12 + D("2000"))

    def test_csv(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = self.orc.exportar_csv(Path(pasta) / "p.csv")
            with caminho.open(encoding="utf-8-sig") as f:
                linhas = list(csv.reader(f, delimiter=";"))
        self.assertEqual(len(linhas), 13)  # cabeçalho + 12 meses
        self.assertEqual(linhas[1], ["1", "1.450,00", "400,00", "1.850,00", "1.850,00"])


class TestEntrada(unittest.TestCase):
    def test_repete_ate_valor_valido(self):
        respostas = iter(["abc", "9", "2"])
        mensagens = []
        e = EntradaUsuario(leitor=lambda _: next(respostas), escritor=mensagens.append)
        self.assertEqual(e.inteiro("> ", 1, 2), 2)
        self.assertEqual(len(mensagens), 2)

    def test_sim_nao(self):
        respostas = iter(["talvez", "N"])
        e = EntradaUsuario(leitor=lambda _: next(respostas), escritor=lambda _: None)
        self.assertFalse(e.sim_nao("?"))


if __name__ == "__main__":
    unittest.main()
