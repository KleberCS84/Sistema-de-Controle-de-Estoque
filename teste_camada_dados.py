"""
Teste manual da camada de dados (estoque_dados.py).
Roda um cenário completo: cadastra produto, registra movimentos,
recalcula saldo, e testa os casos de erro.
"""

import estoque_dados as dados

print("=== 1. Lista de produtos vazia ===")
print(dados.carregar_produtos())
assert dados.carregar_produtos() == []

print("\n=== 2. Cadastrar produto novo ===")
produto = {
    "ID": "P001",
    "Nome": "Parafuso M8",
    "Categoria": "Ferragens",
    "Local": "Almoxarifado A",
    "Quantidade Atual": 0,
    "Ponto de Reposição": 50,
}
dados.salvar_produto(produto)
print(dados.carregar_produtos())
assert len(dados.carregar_produtos()) == 1

print("\n=== 3. Verificar produto_existe ===")
print("P001 existe:", dados.produto_existe("P001"))
print("P999 existe:", dados.produto_existe("P999"))
assert dados.produto_existe("P001") is True
assert dados.produto_existe("P999") is False

print("\n=== 4. Registrar entrada de 150 unidades ===")
dados.adicionar_movimento("P001", "Entrada", 150)
saldo = dados.recalcular_quantidade("P001")
print("Saldo após entrada:", saldo)
assert saldo == 150

print("\n=== 5. Registrar saída de 30 unidades ===")
dados.adicionar_movimento("P001", "Saída", 30)
saldo = dados.recalcular_quantidade("P001")
print("Saldo após saída:", saldo)
assert saldo == 120

print("\n=== 6. Verificar produto atualizado ===")
produto_atualizado = dados.buscar_produto("P001")
print(produto_atualizado)
assert produto_atualizado["Quantidade Atual"] == 120

print("\n=== 7. Atualizar produto existente (mudar ponto de reposição) ===")
produto_atualizado["Ponto de Reposição"] = 80
dados.salvar_produto(produto_atualizado)
produtos = dados.carregar_produtos()
print(produtos)
assert len(produtos) == 1  # não deve duplicar linha
assert produtos[0]["Ponto de Reposição"] == 80

print("\n=== 8. Buscar produto inexistente (deve lançar erro) ===")
try:
    dados.buscar_produto("P999")
    print("ERRO: deveria ter lançado exceção!")
except dados.ProdutoNaoEncontradoError as e:
    print("OK, exceção esperada:", e)

print("\n=== 9. Movimento com tipo inválido (deve lançar erro) ===")
try:
    dados.adicionar_movimento("P001", "Transferência", 10)
    print("ERRO: deveria ter lançado exceção!")
except ValueError as e:
    print("OK, exceção esperada:", e)

print("\n=== 10. Verificar histórico de movimentos ===")
movimentos = dados.carregar_movimentos()
print(movimentos)
assert len(movimentos) == 2

print("\n✅ TODOS OS TESTES PASSARAM")
