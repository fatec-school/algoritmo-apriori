import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Cada linha é uma transação e as colunas são características
data = {
    'Valor_Alto': [1, 0, 0, 1, 0, 0, 1, 0, 1, 1],
    'Internacional': [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    'Nova_Conta': [0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
    'Horario_Noturno': [0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    'Dispositivo_Conhecido': [1, 1, 1, 1, 1, 1, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

print("--- Base de Transações ---")
print(df)

# Queremos encontrar padrões que ocorrem em pelo menos 30% das transações (suporte)
frequent_itemsets = apriori(df, min_support=0.3, use_colnames=True)

# Vamos focar em regras que tenham alta confiança (acima de 80%)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.8)

print("\n--- Regras de Comportamento Normal Identificadas ---")
print(rules[['antecedents', 'consequents', 'support', 'confidence']])

# Função para detectar anomalia
def detectar_anomalia(transacao, regras):
    """
    Uma lógica simples: se a transação possui características que 
    normalmente implicariam em 'Dispositivo_Conhecido', mas não possui,
    ou se ela não se encaixa em nenhum padrão frequente.
    """
    
    suspeita = False
    motivo = ""

    # Teste manual de lógica de anomalia baseada em regras:
    if transacao['Internacional'] == 1 and transacao['Dispositivo_Conhecido'] == 0:
        suspeita = True
        motivo = "Transação internacional de dispositivo desconhecido."
    
    if transacao['Horario_Noturno'] == 1 and transacao['Valor_Alto'] == 1:
        suspeita = True
        motivo = "Valor alto em horário atípico."

    return suspeita, motivo

# Testando novas transações
transacao_normal = {'Valor_Alto': 1, 'Internacional': 0, 'Nova_Conta': 0, 'Horario_Noturno': 0, 'Dispositivo_Conhecido': 1}
transacao_suspeita = {'Valor_Alto': 1, 'Internacional': 1, 'Nova_Conta': 1, 'Horario_Noturno': 1, 'Dispositivo_Conhecido': 0}

for i, t in enumerate([transacao_normal, transacao_suspeita]):
    is_fraude, msg = detectar_anomalia(t, rules)
    status = "⚠️ SUSPEITA" if is_fraude else "✅ NORMAL"
    print(f"\nTransação {i+1}: {status}")
    if is_fraude: print(f"Motivo: {msg}")