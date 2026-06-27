"""
estoque_operacoes.py

Funcionalidades "core" do sistema: registrar entrada, registrar saída e
cadastrar produto novo. Esta camada cuida das regras de negócio e
validações; toda leitura/escrita real no Excel é delegada a
estoque_dados.py.
"""

import estoque_dados as dados


class SaidaNaoConfirmadaError(Exception):
    """Levantado quando o usuário cancela uma saída maior que o estoque."""


def registrar_entrada(id_produto: str, quantidade: float) -> float:
    """Registra uma entrada de estoque e retorna o novo saldo.

    Levanta ProdutoNaoEncontradoError se o produto não existir.
    Levanta ValueError se a quantidade não for positiva.
    """
    if quantidade <= 0:
        raise ValueError("A quantidade de entrada deve ser maior que zero.")

    # Confirma que o produto existe antes de gravar o movimento
    dados.buscar_produto(id_produto)

    dados.adicionar_movimento(id_produto, "Entrada", quantidade)
    return dados.recalcular_quantidade(id_produto)


def registrar_saida(
    id_produto: str,
    quantidade: float,
    confirmar_negativo=None,
) -> float:
    """Registra uma saída de estoque e retorna o novo saldo.

    Se a saída deixaria o saldo negativo, pede confirmação através da
    função 'confirmar_negativo' (recebe o saldo atual e a quantidade
    solicitada, deve retornar True/False). Se 'confirmar_negativo' não
    for informada, assume False (operação cancelada) por segurança.

    Levanta ProdutoNaoEncontradoError se o produto não existir.
    Levanta ValueError se a quantidade não for positiva.
    Levanta SaidaNaoConfirmadaError se o usuário não confirmar a saída
    que deixaria o saldo negativo.
    """
    if quantidade <= 0:
        raise ValueError("A quantidade de saída deve ser maior que zero.")

    produto = dados.buscar_produto(id_produto)
    saldo_atual = produto["Quantidade Atual"]

    if quantidade > saldo_atual:
        if confirmar_negativo is None or not confirmar_negativo(
            saldo_atual, quantidade
        ):
            raise SaidaNaoConfirmadaError(
                f"Saída de {quantidade} cancelada: estoque atual é "
                f"{saldo_atual}, ficaria negativo."
            )

    dados.adicionar_movimento(id_produto, "Saída", quantidade)
    return dados.recalcular_quantidade(id_produto)


def cadastrar_produto(
    id_produto: str,
    nome: str,
    categoria: str,
    local: str,
    ponto_reposicao: float,
) -> dict:
    """Cadastra um novo produto com Quantidade Atual inicial igual a 0.

    Levanta ValueError se o ID já existir (use registrar_entrada para
    adicionar estoque a um produto já cadastrado).
    """
    if dados.produto_existe(id_produto):
        raise ValueError(f"Produto '{id_produto}' já existe.")

    if ponto_reposicao < 0:
        raise ValueError("O ponto de reposição não pode ser negativo.")

    produto = {
        "ID": id_produto,
        "Nome": nome,
        "Categoria": categoria,
        "Local": local,
        "Quantidade Atual": 0,
        "Ponto de Reposição": ponto_reposicao,
    }
    dados.salvar_produto(produto)
    return produto
