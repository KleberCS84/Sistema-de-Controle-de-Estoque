# Roteiro de teste manual — menu.py

Este roteiro cobre o fluxo completo do sistema através do menu
interativo, incluindo os principais casos de erro do spec original.
Sirve como checklist para validar manualmente o sistema após qualquer
alteração no código.

> Antes de começar, apague o `estoque.xlsx` existente (se houver) e rode
> `python setup_planilha.py`, para garantir um ambiente limpo.

## 1. Cadastro de produto

1. Rode `python menu.py`
2. Escolha `7` (Cadastrar novo produto)
3. Preencha: ID `P001`, Nome `Parafuso M8`, Categoria `Ferragens`,
   Local `Almoxarifado A`, Ponto de reposição `50`
4. **Esperado**: mensagem "Produto 'P001' cadastrado com sucesso."

5. Repita a opção `7` com o mesmo ID `P001`
6. **Esperado**: mensagem de erro "Produto 'P001' já existe." (não deve
   duplicar o produto)

## 2. Registrar entrada

1. Escolha `1` (Registrar entrada)
2. ID `P001`, quantidade `150`
3. **Esperado**: "Entrada registrada. Novo saldo de 'P001': 150.0"

4. Tente registrar entrada num produto inexistente: ID `P999`,
   quantidade `10`
5. **Esperado**: "Erro: Produto 'P999' não encontrado."

## 3. Ver estoque atual

1. Escolha `3` (Ver estoque atual)
2. Escolha `1` (agrupar por Categoria)
3. **Esperado**: produto `P001` aparece sob "Ferragens" com 🟢 (saldo
   150, acima do ponto de reposição 50)

## 4. Registrar saída (caso normal)

1. Escolha `2` (Registrar saída)
2. ID `P001`, quantidade `30`
3. **Esperado**: "Saída registrada. Novo saldo de 'P001': 120.0"

## 5. Registrar saída maior que o estoque (cancelando)

1. Escolha `2`, ID `P001`, quantidade `9999`
2. Quando perguntado "Confirmar mesmo assim? (s/n)", responda `n`
3. **Esperado**: "Operação cancelada: Saída de 9999.0 cancelada..."
4. Confira no menu `3` que o saldo continua `120` (a operação cancelada
   não deve ter alterado nada)

## 6. Registrar saída maior que o estoque (confirmando)

1. Escolha `2`, ID `P001`, quantidade `9999`
2. Responda `s` à confirmação
3. **Esperado**: "Saída registrada. Novo saldo de 'P001': -9879.0"

> Esse é um teste de comportamento limite — na prática, evite deixar o
> saldo negativo de propósito. Depois deste teste, é recomendável
> recriar o `estoque.xlsx` antes de continuar usando o sistema com dados
> reais.

## 7. Alertas de reposição

1. Recrie o ambiente (`estoque.xlsx` novo) e repita os passos 1 a 4
   (cadastro + entrada de 150 + saída de 30, saldo final 120)
2. Cadastre um segundo produto: ID `P002`, Nome `Luva de Proteção`,
   Categoria `EPI`, Local `Almoxarifado B`, Ponto de reposição `20`
3. Registre uma entrada de `15` para `P002` (saldo ficará abaixo do
   ponto de reposição)
4. Escolha `4` (Alertas de reposição)
5. **Esperado**: `P002` aparece na lista de alertas; `P001` não aparece

## 8. Relatório de giro de estoque

1. Escolha `5` (Relatório de giro de estoque)
2. Pressione Enter para usar o período padrão (30 dias)
3. **Esperado**: `P001` aparece com total de saídas `30`

## 9. Previsão de ruptura

1. Escolha `6` (Previsão de quando vai faltar), ID `P001`
2. **Esperado**: mostra consumo médio diário, dias restantes e data
   estimada de ruptura (com base na saída de 30 registrada nos últimos
   7 dias)

3. Repita para `P002` (que não teve nenhuma saída registrada)
4. **Esperado**: "Sem consumo recente — sem previsão possível."

## 10. Opção de menu inválida

1. No menu principal, digite `99`
2. **Esperado**: "Opção inválida. Tente de novo." — o programa continua
   rodando, não trava nem fecha

## 11. Sair do programa

1. Digite `0`
2. **Esperado**: "Até logo!" e o programa termina normalmente

---

Se todos os passos acima produziram o resultado esperado, o sistema
está funcionando conforme o design original.
