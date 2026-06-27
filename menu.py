"""
menu.py

Ponto de entrada do Sistema de Controle de Estoque. Apresenta um menu
interativo no terminal e delega cada operação para os módulos
estoque_dados, estoque_operacoes e estoque_consultas.

Uso:
    python menu.py
"""

import estoque_dados as dados
import estoque_operacoes as ops
import estoque_consultas as consultas

TEXTO_MENU = """
=== Controle de Estoque ===
1. Registrar entrada
2. Registrar saída
3. Ver estoque atual (por categoria/local)
4. Alertas de reposição
5. Relatório de giro de estoque
6. Previsão de quando vai faltar
7. Cadastrar novo produto
0. Sair
"""


def pedir_numero(mensagem: str) -> float:
    """Pede um número ao usuário, repetindo até receber um valor válido."""
    while True:
        valor = input(mensagem).strip()
        try:
            return float(valor)
        except ValueError:
            print("Valor inválido. Digite um número (ex: 10 ou 10.5).")


def confirmar_no_terminal(saldo_atual: float, quantidade: float) -> bool:
    """Pergunta ao usuário se ele confirma uma saída que deixaria o saldo negativo."""
    resposta = input(
        f"Estoque atual é {saldo_atual}, essa saída de {quantidade} "
        f"deixaria o saldo negativo. Confirmar mesmo assim? (s/n): "
    ).strip().lower()
    return resposta == "s"


def opcao_registrar_entrada() -> None:
    id_produto = input("ID do produto: ").strip()
    quantidade = pedir_numero("Quantidade de entrada: ")
    try:
        saldo = ops.registrar_entrada(id_produto, quantidade)
        print(f"Entrada registrada. Novo saldo de '{id_produto}': {saldo}")
    except (dados.ProdutoNaoEncontradoError, ValueError) as e:
        print(f"Erro: {e}")


def opcao_registrar_saida() -> None:
    id_produto = input("ID do produto: ").strip()
    quantidade = pedir_numero("Quantidade de saída: ")
    try:
        saldo = ops.registrar_saida(
            id_produto, quantidade, confirmar_negativo=confirmar_no_terminal
        )
        print(f"Saída registrada. Novo saldo de '{id_produto}': {saldo}")
    except (dados.ProdutoNaoEncontradoError, ValueError) as e:
        print(f"Erro: {e}")
    except ops.SaidaNaoConfirmadaError as e:
        print(f"Operação cancelada: {e}")


def opcao_ver_estoque_atual() -> None:
    escolha = input("Agrupar por (1) Categoria ou (2) Local? ").strip()
    agrupar_por = "Local" if escolha == "2" else "Categoria"

    grupos = consultas.estoque_atual(agrupar_por)
    if not grupos:
        print("Nenhum produto cadastrado ainda.")
        return

    for grupo, produtos in grupos.items():
        print(f"\n{grupo}:")
        for p in produtos:
            icone = "🟢" if p["Status"] == "OK" else "🔴"
            print(f"  {icone} {p['Nome']} (ID {p['ID']}): {p['Quantidade Atual']} unid.")


def opcao_alertas_reposicao() -> None:
    alertas = consultas.alertas_reposicao()
    if not alertas:
        print("Nenhum produto está abaixo do ponto de reposição. 🎉")
        return

    print("\nProdutos que precisam de reposição:")
    for p in alertas:
        print(
            f"  🔴 {p['Nome']} (ID {p['ID']}): {p['Quantidade Atual']} unid. "
            f"(ponto de reposição: {p['Ponto de Reposição']})"
        )


def opcao_giro_estoque() -> None:
    texto_dias = input("Período em dias (Enter para 30): ").strip()
    dias = int(texto_dias) if texto_dias else 30

    giro = consultas.giro_estoque(dias=dias)
    if not giro:
        print(f"Nenhuma saída registrada nos últimos {dias} dias.")
        return

    print(f"\nGiro de estoque (últimos {dias} dias):")
    for item in giro:
        print(f"  {item['Nome']} (ID {item['ID']}): {item['Total Saída']} unid. saídas")


def opcao_previsao_ruptura() -> None:
    id_produto = input("ID do produto: ").strip()
    try:
        previsao = consultas.previsao_ruptura(id_produto)
    except dados.ProdutoNaoEncontradoError as e:
        print(f"Erro: {e}")
        return

    if previsao["dias_restantes"] is None:
        print("Sem consumo recente — sem previsão possível.")
        return

    print(
        f"Consumo médio diário (últimos {consultas.DIAS_JANELA_PREVISAO} dias): "
        f"{previsao['consumo_medio_diario']:.2f} unid./dia"
    )
    print(f"Dias restantes estimados: {previsao['dias_restantes']:.1f}")
    print(f"Data estimada de ruptura: {previsao['data_estimada_ruptura'].strftime('%d/%m/%Y')}")


def opcao_cadastrar_produto() -> None:
    id_produto = input("ID do novo produto: ").strip()
    nome = input("Nome: ").strip()
    categoria = input("Categoria: ").strip()
    local = input("Local: ").strip()
    ponto_reposicao = pedir_numero("Ponto de reposição: ")

    try:
        ops.cadastrar_produto(id_produto, nome, categoria, local, ponto_reposicao)
        print(f"Produto '{id_produto}' cadastrado com sucesso.")
    except ValueError as e:
        print(f"Erro: {e}")


OPCOES = {
    "1": opcao_registrar_entrada,
    "2": opcao_registrar_saida,
    "3": opcao_ver_estoque_atual,
    "4": opcao_alertas_reposicao,
    "5": opcao_giro_estoque,
    "6": opcao_previsao_ruptura,
    "7": opcao_cadastrar_produto,
}


def main() -> None:
    # Garante que o arquivo existe antes de começar (sem sobrescrever dados).
    try:
        dados.carregar_produtos()
    except dados.ArquivoNaoEncontradoError as e:
        print(f"Erro: {e}")
        return

    while True:
        print(TEXTO_MENU)
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Até logo!")
            break

        acao = OPCOES.get(escolha)
        if acao is None:
            print("Opção inválida. Tente de novo.")
            continue

        try:
            acao()
        except PermissionError as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    main()
