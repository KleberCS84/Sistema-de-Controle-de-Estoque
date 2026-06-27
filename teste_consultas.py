"""
Teste manual das consultas (estoque_consultas.py).
"""

from datetime import date, timedelta

import estoque_dados as dados
import estoque_consultas as consultas

hoje = date.today()

print("=== Setup: cadastrar 2 produtos ===")
dados.salvar_produto({
    "ID": "P001", "Nome": "Parafuso M8", "Categoria": "Ferragens",
    "Local": "Almoxarifado A", "Quantidade Atual": 0, "Ponto de Reposição": 50,
})
dados.salvar_produto({
    "ID": "P002", "Nome": "Luva de Proteção", "Categoria": "EPI",
    "Local": "Almoxarifado B", "Quantidade Atual": 0, "Ponto de Reposição": 20,
})
print("OK")

print("\n=== Setup: movimentos de P001 (entrada 150, saídas espalhadas) ===")
dados.adicionar_movimento("P001", "Entrada", 150, data_movimento=hoje - timedelta(days=10))
# Saídas dentro da janela de 7 dias: 10 + 10 + 10 = 30 em 7 dias -> média 30/7
dados.adicionar_movimento("P001", "Saída", 10, data_movimento=hoje - timedelta(days=6))
dados.adicionar_movimento("P001", "Saída", 10, data_movimento=hoje - timedelta(days=3))
dados.adicionar_movimento("P001", "Saída", 10, data_movimento=hoje - timedelta(days=1))
# Saída antiga, fora da janela de 7 dias -- não deve contar na previsão
dados.adicionar_movimento("P001", "Saída", 50, data_movimento=hoje - timedelta(days=20))
dados.recalcular_quantidade("P001")

print("\n=== Setup: movimentos de P002 (estoque baixo, sem saídas recentes) ===")
dados.adicionar_movimento("P002", "Entrada", 15, data_movimento=hoje - timedelta(days=5))
dados.recalcular_quantidade("P002")

print("\n--- Saldos após setup ---")
print(dados.buscar_produto("P001"))
print(dados.buscar_produto("P002"))

print("\n=== 1. Estoque atual agrupado por Categoria ===")
grupos = consultas.estoque_atual("Categoria")
for categoria, produtos in grupos.items():
    print(f"{categoria}:")
    for p in produtos:
        print(f"  {p['Nome']}: {p['Quantidade Atual']} ({p['Status']})")
assert grupos["Ferragens"][0]["Status"] == "OK"  # P001 tem saldo bem acima do ponto
assert grupos["EPI"][0]["Status"] == "BAIXO"     # P002: 15 <= ponto de reposição 20

print("\n=== 2. Estoque atual agrupado por Local ===")
grupos_local = consultas.estoque_atual("Local")
print(list(grupos_local.keys()))
assert "Almoxarifado A" in grupos_local
assert "Almoxarifado B" in grupos_local

print("\n=== 3. agrupar_por inválido (deve lançar erro) ===")
try:
    consultas.estoque_atual("Cor")
    print("ERRO: deveria ter lançado exceção!")
except ValueError as e:
    print("OK, exceção esperada:", e)

print("\n=== 4. Alertas de reposição ===")
alertas = consultas.alertas_reposicao()
print(alertas)
ids_alerta = [a["ID"] for a in alertas]
assert "P002" in ids_alerta
assert "P001" not in ids_alerta

print("\n=== 5. Giro de estoque (últimos 30 dias) ===")
giro = consultas.giro_estoque(dias=30)
print(giro)
# Em 30 dias entram a saída antiga (50) + as 3 recentes (30) = 80
assert giro[0]["ID"] == "P001"
assert giro[0]["Total Saída"] == 50 + 30

print("\n=== 6. Giro de estoque (últimos 7 dias, exclui saída antiga) ===")
giro_7 = consultas.giro_estoque(dias=7)
print(giro_7)
assert giro_7[0]["Total Saída"] == 30  # só as 3 saídas recentes

print("\n=== 7. Previsão de ruptura - P001 (tem consumo recente) ===")
previsao = consultas.previsao_ruptura("P001")
print(previsao)
# consumo médio = 30 / 7 dias
assert abs(previsao["consumo_medio_diario"] - (30 / 7)) < 0.001
assert previsao["dias_restantes"] is not None
print(f"Dias restantes estimados: {previsao['dias_restantes']:.1f}")

print("\n=== 8. Previsão de ruptura - P002 (sem saídas, sem previsão possível) ===")
previsao_p002 = consultas.previsao_ruptura("P002")
print(previsao_p002)
assert previsao_p002["consumo_medio_diario"] == 0.0
assert previsao_p002["dias_restantes"] is None
assert previsao_p002["data_estimada_ruptura"] is None

print("\n=== 9. Previsão para produto inexistente (deve lançar erro) ===")
try:
    consultas.previsao_ruptura("P999")
    print("ERRO: deveria ter lançado exceção!")
except dados.ProdutoNaoEncontradoError as e:
    print("OK, exceção esperada:", e)

print("\n✅ TODOS OS TESTES PASSARAM")
