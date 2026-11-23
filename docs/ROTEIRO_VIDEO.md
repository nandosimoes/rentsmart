# Roteiro do Vídeo Pitch — RentSmart (até 4 minutos)

Gravação de tela (OBS Studio, ou Win + Alt + R no Windows). Deixe abertos: o PDF (fluxograma e diagrama de classes), o VS Code com o projeto e um terminal na pasta do projeto.

| Tempo | O que mostrar na tela | O que falar (sugestão) |
|---|---|---|
| 0:00–0:25 | PDF, página 2 (regras) | "Olá, sou o Fernando. A R.M Imóveis calculava orçamentos de locação na mão, o que gerava demora e erros em adicionais, descontos e na taxa de contrato. O RentSmart automatiza esse cálculo em Python, mostra a composição do valor e gera a projeção de 12 meses em CSV." |
| 0:25–0:55 | PDF, fluxograma | "A lógica é: ler e validar os dados do cliente e do imóvel; somar o aluguel-base e os adicionais; aplicar o desconto de 5% do apartamento, quando não há crianças, depois dos adicionais; parcelar a taxa de 2 mil em até 5 vezes; e, num laço de 12 meses, somar aluguel e parcela. Toda entrada inválida faz a pergunta se repetir." |
| 0:55–1:35 | PDF, diagrama de classes | "Imovel é uma classe abstrata com o algoritmo comum: base, adicionais e descontos. ImovelComGaragem reúne a regra que casa e apartamento compartilham. Apartamento só acrescenta o desconto; Casa só define seus valores; Estudio tem sua regra própria de estacionamento. TaxaContratual cuida do parcelamento, e Orcamento junta imóvel e taxa e gera o resumo e o CSV." |
| 1:35–2:20 | VS Code: `imoveis.py` → `itens_orcamento()`, `Apartamento.calcular_descontos()`, `Estudio.calcular_adicionais()`; `contrato.py` → `valores_parcelas()` | "Este é o método comum a todos os imóveis… aqui o apartamento sobrescreve só o desconto, calculado sobre o subtotal já com adicionais… no estúdio, pacote de 250 mais 60 por vaga extra… e aqui a taxa: quando a divisão não fecha, os centavos ficam na última parcela, para somar exatamente 2 mil." |
| 2:20–3:15 | Terminal: `python main.py` | Faça um orçamento completo. Sugestão: nome "Maria" → **1** (apartamento) → **2** quartos → garagem **s** → crianças **n** → **4** parcelas. Antes de acertar, digite um valor inválido (ex.: "9" nos quartos) para mostrar a validação. Comente: "aluguel de 1.140: 700 + 200 + 300, menos 5%; a taxa aparece separada, em 4x de 500." |
| 3:15–3:40 | Abrir o CSV da pasta `saida/` no Excel | "O CSV traz os 12 meses: nos 4 primeiros, aluguel mais parcela da taxa; depois, só o aluguel; e o acumulado do ano, 15.680 reais." |
| 3:40–4:00 | Diagrama de classes ou código | "A Orientação a Objetos deixou cada regra no lugar certo: herança evitou repetir código, polimorfismo deixou o orçamento tratar todos os imóveis da mesma forma, e separar regras da interface permitiu escrever testes automáticos. Para incluir um novo tipo de imóvel, basta criar uma subclasse. Obrigado!" |

## Checklist antes de enviar
- [ ] Vídeo com até 4:00, publicado no YouTube como **Não listado**
- [ ] Abrir o link numa aba anônima para confirmar que o vídeo abre
- [ ] Repositório do GitHub **público**, com README, código, `docs/` e `exemplos/`
- [ ] Trocar `SEU-USUARIO` pelo seu usuário do GitHub no README (linha do `git clone`)
