"""Leitura e validação das entradas digitadas pelo usuário."""


class EntradaUsuario:
    """Agrupa as perguntas ao usuário, repetindo até receber um valor válido.

    A função de leitura é injetável (``leitor``), o que permite testar o
    fluxo sem digitar nada.
    """

    def __init__(self, leitor=input, escritor=print):
        self.ler = leitor
        self.escrever = escritor

    def texto(self, pergunta: str) -> str:
        while True:
            valor = self.ler(pergunta).strip()
            if valor:
                return valor
            self.escrever("  ! Este campo não pode ficar vazio.")

    def opcao(self, pergunta: str, opcoes: dict[str, str]) -> str:
        """Mostra um menu numerado e devolve a chave escolhida."""
        chaves = list(opcoes)
        while True:
            self.escrever(pergunta)
            for i, chave in enumerate(chaves, start=1):
                self.escrever(f"  [{i}] {opcoes[chave]}")
            valor = self.ler("Escolha: ").strip()
            if valor.isdigit() and 1 <= int(valor) <= len(chaves):
                return chaves[int(valor) - 1]
            self.escrever(f"  ! Opção inválida. Digite um número de 1 a {len(chaves)}.")

    def sim_nao(self, pergunta: str) -> bool:
        while True:
            valor = self.ler(f"{pergunta} (s/n): ").strip().lower()
            if valor in ("s", "sim"):
                return True
            if valor in ("n", "nao", "não"):
                return False
            self.escrever("  ! Responda com 's' para sim ou 'n' para não.")

    def inteiro(self, pergunta: str, minimo: int, maximo: int | None = None) -> int:
        while True:
            valor = self.ler(pergunta).strip()
            if valor.lstrip("-").isdigit():
                numero = int(valor)
                if numero >= minimo and (maximo is None or numero <= maximo):
                    return numero
            faixa = f"entre {minimo} e {maximo}" if maximo is not None else f"maior ou igual a {minimo}"
            self.escrever(f"  ! Valor inválido. Digite um número inteiro {faixa}.")
