# Design: Sistema de Controle de Estoque (CLI + Excel)

## Visão geral

Ferramenta de linha de comando em Python que gerencia entradas, saídas e
reposição de estoque, usando uma planilha Excel (`estoque.xlsx`) como única
fonte de dados. Projeto de portfólio: demonstra automação de um processo de
negócio comum (gestão de estoque) usando Python + openpyxl/pandas.

## Decisões de escopo

- **Tecnologia**: Python lendo/escrevendo Excel via `openpyxl`/`pandas`.
  Escolhido por ser fácil de evoluir depois para banco de dados real / app
  web, sem reescrever a lógica de negócio.
- **Armazenamento**: Excel é a única fonte de dados (Opção A). Mais simples
  para MVP e mais fácil de demonstrar em portfólio do que um banco invisível.
  Risco aceito: não há proteção contra edição concorrente do arquivo.
- **Interface**: menu de terminal (CLI), numerado, sem dependências de UI.
- **Categorização**: produtos têm Categoria e Local (suporta múltiplos
  locais de estoque).
- **Previsão de ruptura**: baseada em consumo médio dos últimos 7 dias
  (mais sensível a mudanças recentes que uma média de 30 dias ou histórico
  completo).

## Estrutura de dados (estoque.xlsx)

### Aba `Produtos`
| Campo | Tipo | Exemplo |
|---|---|---|
| ID | texto curto | P001 |
| Nome | texto | Parafuso M8 |
| Categoria | texto | Ferragens |
| Local | texto | Almoxarifado A |
| Quantidade Atual | número | 150 |
| Ponto de Reposição | número | 50 |

`Quantidade Atual` é sempre recalculada a partir do histórico de
`Movimentos` — nunca editada manualmente nem fica dessincronizada.

### Aba `Movimentos`
| Campo | Tipo | Exemplo |
|---|---|---|
| Data | data | 2026-06-20 |
| ID Produto | texto | P001 |
| Tipo | texto | Entrada / Saída |
| Quantidade | número | 30 |

Histórico append-only: toda entrada/saída gera uma nova linha; linhas
existentes nunca são editadas.

## Menu (CLI)

```
=== Controle de Estoque ===
1. Registrar entrada
2. Registrar saída
3. Ver estoque atual (por categoria/local)
4. Alertas de reposição
5. Relatório de giro de estoque
6. Previsão de quando vai faltar
7. Cadastrar novo produto
0. Sair
```

## Lógica de cada funcionalidade

- **Registrar entrada/saída**: valida se o produto existe → grava linha em
  `Movimentos` → recalcula `Quantidade Atual` em `Produtos` → salva o Excel.
- **Ver estoque atual**: lê `Produtos`, agrupa por Categoria/Local, mostra
  tabela com quantidade e status (🟢 ok / 🔴 abaixo do ponto de reposição).
- **Alertas de reposição**: filtra produtos onde
  `Quantidade Atual <= Ponto de Reposição`.
- **Relatório de giro de estoque**: a partir de `Movimentos`, soma saídas
  por produto num período e ordena do mais ao menos movimentado.
- **Previsão de ruptura**: consumo médio diário = soma de saídas dos
  últimos 7 dias / 7. `dias restantes = Quantidade Atual / consumo médio
  diário`. Se consumo médio for 0 → "sem consumo recente — sem previsão".
- **Cadastrar novo produto**: pede campos da aba `Produtos`, valida ID
  único, grava nova linha.

## Tratamento de erros

- Produto não encontrado → mensagem clara, retorna ao menu sem quebrar o
  programa.
- Saída maior que o estoque disponível → avisa e pede confirmação antes de
  permitir saldo negativo.
- Excel aberto/travado por outro processo (ex.: aberto no próprio Excel) →
  mensagem amigável pedindo para fechar o arquivo e tentar novamente.

## Fora de escopo (YAGNI para este MVP)

- Unidade de medida, custo unitário, fornecedor, SKU — não incluídos agora.
- Interface gráfica ou planilha-como-interface — descartado em favor do
  menu CLI.
- Múltiplos usuários simultâneos / banco de dados — adiado para uma
  eventual v2 (migração natural: trocar a camada de leitura/escrita do
  Excel por SQLite, mantendo a lógica de negócio).
