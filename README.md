# RentSmart — Orçamento de Locação da R.M Imóveis

Aplicação de terminal em Python que calcula o orçamento de locação de **casas, apartamentos e estúdios** da R.M Imóveis, aplicando adicionais, descontos e a taxa contratual, e gera um **CSV com a projeção dos 12 primeiros meses**.

Trabalho da disciplina *Algorithmic Thinking & Introduction to Object-Oriented Programming*.
Autor: Fernando da Silva Simões

## Regras implementadas

| Imóvel | Aluguel-base | Adicionais | Desconto |
|---|---|---|---|
| Apartamento | R$ 700,00 | +R$ 200,00 (2 quartos) · +R$ 300,00 (garagem) | 5% se o cliente **não** tem crianças, aplicado após os adicionais |
| Casa | R$ 900,00 | +R$ 250,00 (2 quartos) · +R$ 300,00 (garagem) | — |
| Estúdio | R$ 1.200,00 | +R$ 250,00 (pacote com 2 vagas) · +R$ 60,00 por vaga adicional | — |

**Taxa contratual:** R$ 2.000,00, em 1 a 5 parcelas, cobrada separadamente do aluguel nos primeiros meses. Se a divisão não for exata (ex.: 3x), os centavos de diferença ficam na última parcela, para que a soma dê exatamente R$ 2.000,00.

## Requisitos

- Python **3.10 ou superior**
- Nenhuma biblioteca externa (só a biblioteca padrão: `abc`, `decimal`, `csv`, `pathlib`)

## Como executar

```bash
git clone https://github.com/nandosimoes/rentsmart.git
cd rentsmart

python main.py          # modo interativo (no Linux/macOS pode ser python3)
python main.py --demo   # gera um orçamento de exemplo sem perguntas
```

No modo interativo o sistema pede: nome do cliente → tipo de imóvel → quartos, garagem e crianças (ou estacionamento, no estúdio) → número de parcelas da taxa. Entradas inválidas são recusadas e a pergunta é repetida.

Ao final, o orçamento detalhado aparece no terminal e o CSV é salvo em `saida/projecao_12_meses_<data_hora>.csv`. O arquivo usa `;` como separador e vírgula decimal, então abre direto no Excel em português.

### Exemplo de saída

```
==============================================================
        RENTSMART — R.M IMÓVEIS | ORÇAMENTO DE LOCAÇÃO
==============================================================
Cliente: Cliente Exemplo
Imóvel : Apartamento de 2 quartos
--------------------------------------------------------------
COMPOSIÇÃO DO ALUGUEL MENSAL
  Aluguel-base (Apartamento de 2 quartos)    R$     700,00
  Adicional por 2 quartos                    R$     200,00
  Vaga de garagem                            R$     300,00
  Desconto de 5% (sem crianças)             -R$      60,00
--------------------------------------------------------------
  ALUGUEL MENSAL                             R$   1.140,00
--------------------------------------------------------------
TAXA CONTRATUAL (cobrada à parte do aluguel)
  Valor total da taxa                        R$   2.000,00
  Parcelamento: 4x de R$ 500,00
--------------------------------------------------------------
  Total previsto no 1º ano                   R$  15.680,00
==============================================================
```

CSVs de exemplo estão na pasta `exemplos/`.

## Testes

```bash
python -m unittest -v
```

São 20 testes cobrindo as regras de cada imóvel, o parcelamento da taxa, a projeção, o CSV e a validação das entradas.

## Estrutura do projeto

```
rentsmart/
├── main.py                 # ponto de entrada + classe AplicacaoRentSmart (interface)
├── rentsmart/
│   ├── imoveis.py          # Imovel (abstrata), ImovelComGaragem, Apartamento, Casa, Estudio, ItemOrcamento
│   ├── contrato.py         # TaxaContratual
│   ├── orcamento.py        # Orcamento (resumo, projeção, CSV)
│   └── entrada.py          # EntradaUsuario (leitura e validação)
├── tests/test_regras.py    # testes automatizados
├── exemplos/               # CSVs de exemplo
└── docs/                   # parte teórica (PDF) e fluxograma
```

## Classes principais

- **`Imovel`** (abstrata): guarda `aluguel_base` e `quartos`; define o algoritmo comum `itens_orcamento()` → base + `calcular_adicionais()` + `calcular_descontos()`, e `valor_mensal()`.
- **`ImovelComGaragem`**: regra compartilhada por casa e apartamento (1 ou 2 quartos, garagem de R$ 300,00).
- **`Apartamento`**, **`Casa`**, **`Estudio`**: cada uma só define seus valores e o que muda (desconto do apartamento, estacionamento do estúdio).
- **`TaxaContratual`**: valor, número de parcelas, `valores_parcelas()` e `parcela_do_mes()`.
- **`Orcamento`**: junta cliente + imóvel + taxa; gera `resumo()`, `projecao()` e `exportar_csv()`.
- **`EntradaUsuario`**: perguntas com validação (`opcao`, `sim_nao`, `inteiro`, `texto`).
- **`AplicacaoRentSmart`**: conduz o atendimento no terminal.
