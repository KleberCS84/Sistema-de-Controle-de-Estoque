"""
estoque_consultas.py

Funcionalidades de consulta e relatórios: ver estoque atual, alertas de
reposição, giro de estoque e previsão de quando um produto vai faltar.
Apenas leitura — nenhuma função aqui grava no Excel.
"""

from datetime import date, timedelta

import estoque_dados as dados

DIAS_JANELA_PREVISAO = 7


def estoque_atual(agrupar_por: str = "Categoria") -> dict:
    """Retorna os produtos agrupados por 'Categoria' ou 'Local'.

    Cada produto vem com um campo extra 'Status': 'OK' ou 'BAIXO'
    (quando Quantidade Atual <= Ponto de Reposição).

    Retorna um dicionário {grupo: [produtos]}.
    """
    if agrupar_por not in ("Categoria", "Local"):
        raise ValueError("agrupar_por deve ser 'Categoria' ou 'Local'")

    produtos = dados.carregar_produtos()
    grupos: dict = {}

    for produto in produtos:
        produto_com_status = dict(produto)
        if produto["Quantidade Atual"] <= produto["Ponto de Reposição"]:
            produto_com_status["Status"] = "BAIXO"
        else:
            produto_com_status["Status"] = "OK"

        chave = produto[agrupar_por]
        grupos.setdefault(chave, []).append(produto_com_status)

    return grupos


def alertas_reposicao() -> list[dict]:
    """Retorna a lista de produtos com Quantidade Atual <= Ponto de Reposição."""
    produtos = dados.carregar_produtos()
    return [
        produto
        for produto in produtos
        if produto["Quantidade Atual"] <= produto["Ponto de Reposição"]
    ]


def giro_estoque(dias: int = 30) -> list[dict]:
    """Retorna produtos ordenados pelo total de saídas nos últimos 'dias' dias.

    Cada item do retorno é um dicionário:
        {"ID": ..., "Nome": ..., "Total Saída": ...}
    Ordenado do mais movimentado para o menos movimentado. Produtos sem
    nenhuma saída no período não aparecem na lista.
    """
    movimentos = dados.carregar_movimentos()
    produtos = {p["ID"]: p["Nome"] for p in dados.carregar_produtos()}

    data_limite = date.today() - timedelta(days=dias)
    totais: dict = {}

    for mov in movimentos:
        if mov["Tipo"] != "Saída":
            continue
        if mov["Data"] < data_limite:
            continue
        totais[mov["ID Produto"]] = totais.get(mov["ID Produto"], 0) + mov["Quantidade"]

    resultado = [
        {"ID": id_produto, "Nome": produtos.get(id_produto, "(desconhecido)"), "Total Saída": total}
        for id_produto, total in totais.items()
    ]
    resultado.sort(key=lambda item: item["Total Saída"], reverse=True)
    return resultado


def previsao_ruptura(id_produto: str) -> dict:
    """Estima quando um produto vai faltar, com base no consumo médio
    diário dos últimos DIAS_JANELA_PREVISAO dias.

    Retorna um dicionário:
        {
            "consumo_medio_diario": float,
            "dias_restantes": float | None,  # None se não houver consumo
            "data_estimada_ruptura": date | None,
        }

    Se não houver consumo no período, dias_restantes e
    data_estimada_ruptura vêm como None (sem previsão possível).
    """
    produto = dados.buscar_produto(id_produto)
    movimentos = dados.carregar_movimentos()

    data_limite = date.today() - timedelta(days=DIAS_JANELA_PREVISAO)
    total_saida = sum(
        mov["Quantidade"]
        for mov in movimentos
        if mov["ID Produto"] == id_produto
        and mov["Tipo"] == "Saída"
        and mov["Data"] >= data_limite
    )

    consumo_medio_diario = total_saida / DIAS_JANELA_PREVISAO

    if consumo_medio_diario <= 0:
        return {
            "consumo_medio_diario": 0.0,
            "dias_restantes": None,
            "data_estimada_ruptura": None,
        }

    dias_restantes = produto["Quantidade Atual"] / consumo_medio_diario
    data_estimada = date.today() + timedelta(days=dias_restantes)

    return {
        "consumo_medio_diario": consumo_medio_diario,
        "dias_restantes": dias_restantes,
        "data_estimada_ruptura": data_estimada,
    }
