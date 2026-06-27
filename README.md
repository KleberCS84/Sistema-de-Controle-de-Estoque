# Sistema de Controle de Estoque

Sistema de linha de comando (CLI) em Python para gestão de estoque,
usando uma planilha Excel como banco de dados. Projeto desenvolvido
como peça de portfólio, aplicando 20 anos de experiência prática com
controle de fluxo e logística (mineração) a um problema de negócio comum
a qualquer empresa: saber o que tem em estoque, quando repor, e quando
algo vai faltar.

## Funcionalidades

- **Registrar entradas e saídas** de produtos, com histórico completo
- **Consulta de estoque atual**, agrupado por categoria ou por local
- **Alertas automáticos** de produtos no ponto de reposição
- **Relatório de giro de estoque** (produtos mais/menos movimentados em
  um período)
- **Previsão de ruptura**: estima em quantos dias um produto vai faltar,
  com base no consumo médio dos últimos 7 dias
- **Cadastro de novos produtos**, com categoria, local e ponto de
  reposição configuráveis

## Tecnologias

- Python 3.10+
- [openpyxl](https://openpyxl.readthedocs.io/) — leitura e escrita do
  arquivo Excel
- [pandas](https://pandas.pydata.org/) — manipulação de dados

## Arquitetura

O projeto é dividido em camadas, para manter a lógica de negócio
separada do acesso a dados e da interface:

```
menu.py                → Interface (CLI): menu interativo no terminal
estoque_operacoes.py    → Regras de negócio: entrada, saída, cadastro
estoque_consultas.py    → Relatórios: estoque atual, alertas, giro, previsão
estoque_dados.py        → Acesso a dados: lê/escreve estoque.xlsx
setup_planilha.py       → Script de inicialização (cria o Excel na primeira vez)
```

Essa separação foi uma escolha deliberada: o Excel é o "banco de dados"
da v1, mas como toda leitura/escrita passa por `estoque_dados.py`, seria
possível trocar o Excel por SQLite (ou outro banco) numa v2 sem precisar
reescrever as regras de negócio ou a interface.

### Estrutura do arquivo `estoque.xlsx`

**Aba `Produtos`**

| ID | Nome | Categoria | Local | Quantidade Atual | Ponto de Reposição |
|----|------|-----------|-------|-------------------|---------------------|
| P001 | Parafuso M8 | Ferragens | Almoxarifado A | 120 | 50 |

**Aba `Movimentos`** (histórico completo, nunca editado manualmente)

| Data | ID Produto | Tipo | Quantidade |
|------|-----------|------|------------|
| 2026-06-20 | P001 | Entrada | 150 |
| 2026-06-25 | P001 | Saída | 30 |

A `Quantidade Atual` é sempre recalculada a partir do histórico de
`Movimentos` — isso garante que o saldo nunca fica dessincronizado com o
que de fato entrou e saiu.

## Como usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Criar a planilha inicial (rodar uma única vez)

```bash
python setup_planilha.py
```

Isso cria o arquivo `estoque.xlsx` com as abas e colunas corretas. Se o
arquivo já existir, o script não faz nada (não sobrescreve dados).

### 3. Rodar o sistema

```bash
python menu.py
```

Você verá o menu principal:

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

### Primeiros passos sugeridos

1. Cadastre um produto (opção `7`)
2. Registre uma entrada de estoque (opção `1`)
3. Veja o estoque atual (opção `3`)
4. Registre uma saída (opção `2`)
5. Consulte a previsão de ruptura (opção `6`)

## Testes

O projeto inclui scripts de teste manual para cada camada, sem
dependência de frameworks externos — basta rodar e conferir a saída
`✅ TODOS OS TESTES PASSARAM`:

```bash
python teste_camada_dados.py
python teste_operacoes.py
python teste_consultas.py
```

> Os testes recriam o `estoque.xlsx` com dados de exemplo. Recomenda-se
> rodá-los num ambiente separado dos dados reais, ou apagar o arquivo
> gerado depois (`estoque.xlsx` já está no `.gitignore`).

Veja também o roteiro de teste manual completo do menu interativo em
[`docs/superpowers/roteiro-teste-manual.md`](docs/superpowers/roteiro-teste-manual.md).

## Possíveis evoluções futuras

- Migrar o armazenamento de Excel para SQLite, mantendo a mesma camada
  de regras de negócio
- Exportar relatórios para PDF ou Excel formatado
- Adicionar suporte a múltiplos usuários/locais simultâneos
- Transformar em aplicação web (Flask/FastAPI) reaproveitando
  `estoque_operacoes.py` e `estoque_consultas.py`

## Autor

Desenvolvido por Kleber ([@KleberCS84](https://github.com/KleberCS84)),
como projeto de portfólio na transição de 20 anos de experiência em
logística e mineração para desenvolvimento de software e IA aplicada.
