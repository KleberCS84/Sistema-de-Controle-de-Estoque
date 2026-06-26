"""
setup_planilha.py

Cria o arquivo estoque.xlsx com a estrutura inicial (abas Produtos e
Movimentos), caso ele ainda não exista. Rode este script uma única vez,
antes de usar o sistema pela primeira vez.

Uso:
    python setup_planilha.py
"""

import os
from openpyxl import Workbook

NOME_ARQUIVO = "estoque.xlsx"

COLUNAS_PRODUTOS = [
    "ID",
    "Nome",
    "Categoria",
    "Local",
    "Quantidade Atual",
    "Ponto de Reposição",
]

COLUNAS_MOVIMENTOS = [
    "Data",
    "ID Produto",
    "Tipo",
    "Quantidade",
]


def criar_planilha(caminho: str = NOME_ARQUIVO) -> None:
    """Cria o arquivo Excel com as abas Produtos e Movimentos.

    Se o arquivo já existir, não faz nada (evita sobrescrever dados).
    """
    if os.path.exists(caminho):
        print(f"O arquivo '{caminho}' já existe. Nada foi alterado.")
        return

    wb = Workbook()

    # Aba Produtos (substitui a aba padrão "Sheet")
    aba_produtos = wb.active
    aba_produtos.title = "Produtos"
    aba_produtos.append(COLUNAS_PRODUTOS)

    # Aba Movimentos
    aba_movimentos = wb.create_sheet("Movimentos")
    aba_movimentos.append(COLUNAS_MOVIMENTOS)

    wb.save(caminho)
    print(f"Arquivo '{caminho}' criado com sucesso, com as abas:")
    print(f"  - Produtos: {COLUNAS_PRODUTOS}")
    print(f"  - Movimentos: {COLUNAS_MOVIMENTOS}")


if __name__ == "__main__":
    criar_planilha()
