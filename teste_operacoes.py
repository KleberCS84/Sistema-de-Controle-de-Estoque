"""
Teste manual das operações core (estoque_operacoes.py).
"""

import estoque_dados as dados
import estoque_operacoes as ops

print("=== 1. Cadastrar produto novo ===")
produto = ops.cadastrar_produto(
    id_produto="P001",
    nome="Parafuso M8",
    categoria="Ferragens",
    local="Almoxarifado A",
    ponto_reposicao=50,
)
print(produto)
assert produto["Quantidade Atual"] == 0

print("\n=== 2. Cadastrar produto com ID duplicado (deve lançar erro) ===")
try:
    ops.cadastrar_produto("P001", "Outro nome", "Cat", "Local", 10)
    print("ERRO: deveria ter lançado exceção!")
except ValueError as e:
    print("OK, exceção esperada:", e)

print("\n=== 3. Registrar entrada de 150 ===")
saldo = ops.registrar_entrada("P001", 150)
print("Saldo:", saldo)
assert saldo == 150

print("\n=== 4. Registrar entrada com quantidade inválida (deve lançar erro) ===")
try:
    ops.registrar_entrada("P001", -10)
    print("ERRO: deveria ter lançado exceção!")
except ValueError as e:
    print("OK, exceção esperada:", e)

print("\n=== 5. Registrar entrada em produto inexistente (deve lançar erro) ===")
try:
    ops.registrar_entrada("P999", 10)
    print("ERRO: deveria ter lançado exceção!")
except dados.ProdutoNaoEncontradoError as e:
    print("OK, exceção esperada:", e)

print("\n=== 6. Registrar saída normal de 30 (dentro do saldo) ===")
saldo = ops.registrar_saida("P001", 30)
print("Saldo:", saldo)
assert saldo == 120

print("\n=== 7. Registrar saída maior que o saldo, SEM confirmação (deve cancelar) ===")
try:
    ops.registrar_saida("P001", 999)
    print("ERRO: deveria ter lançado exceção!")
except ops.SaidaNaoConfirmadaError as e:
    print("OK, exceção esperada:", e)
# Saldo não deve ter mudado
produto_check = dados.buscar_produto("P001")
assert produto_check["Quantidade Atual"] == 120
print("Confirmado: saldo permanece 120 (operação não foi gravada)")

print("\n=== 8. Registrar saída maior que o saldo, COM confirmação (deve permitir) ===")
saldo = ops.registrar_saida("P001", 200, confirmar_negativo=lambda atual, qtd: True)
print("Saldo (negativo, conforme esperado):", saldo)
assert saldo == -80

print("\n=== 9. Registrar saída maior, recusando confirmação explicitamente ===")
try:
    ops.registrar_saida("P001", 500, confirmar_negativo=lambda atual, qtd: False)
    print("ERRO: deveria ter lançado exceção!")
except ops.SaidaNaoConfirmadaError as e:
    print("OK, exceção esperada:", e)

print("\n=== 10. Cadastrar produto com ponto de reposição negativo (deve lançar erro) ===")
try:
    ops.cadastrar_produto("P002", "Outro", "Cat", "Local", -5)
    print("ERRO: deveria ter lançado exceção!")
except ValueError as e:
    print("OK, exceção esperada:", e)

print("\n✅ TODOS OS TESTES PASSARAM")
