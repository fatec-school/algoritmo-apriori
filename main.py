"""Detecção simples de anomalias usando regras de associação."""

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

data = {
    "Valor_Alto": [1, 0, 0, 1, 0, 0, 1, 0, 1, 1],
    "Internacional": [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    "Nova_Conta": [0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
    "Horario_Noturno": [0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    "Dispositivo_Conhecido": [1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
}

df = pd.DataFrame(data)

print("--- Base de Transações ---")
print(df)

frequent_itemsets = apriori(
    df,
    min_support=0.3,
    use_colnames=True,
)

rules = association_rules(
    frequent_itemsets,
    metric="confidence",
    min_threshold=0.8,
)

print("\n--- Regras de Comportamento Normal Identificadas ---")
print(
    rules[
        ["antecedents", "consequents", "support", "confidence"]
    ]
)


def detectar_anomalia(transacao):
    """
    Detecta possíveis anomalias em uma transação.
    """
    suspeita = False
    motivo = ""

    if (
        transacao["Internacional"] == 1
        and transacao["Dispositivo_Conhecido"] == 0
    ):
        suspeita = True
        motivo = "Transação internacional de dispositivo desconhecido."

    if (
        transacao["Horario_Noturno"] == 1
        and transacao["Valor_Alto"] == 1
    ):
        suspeita = True
        motivo = "Valor alto em horário atípico."

    return suspeita, motivo


transacao_normal = {
    "Valor_Alto": 1,
    "Internacional": 0,
    "Nova_Conta": 0,
    "Horario_Noturno": 0,
    "Dispositivo_Conhecido": 1,
}

transacao_suspeita = {
    "Valor_Alto": 1,
    "Internacional": 1,
    "Nova_Conta": 1,
    "Horario_Noturno": 1,
    "Dispositivo_Conhecido": 0,
}

for indice, transacao in enumerate(
    [transacao_normal, transacao_suspeita],
    start=1,
):
    is_fraude, mensagem = detectar_anomalia(transacao)

    status = "SUSPEITA" if is_fraude else "NORMAL"

    print(f"\nTransação {indice}: {status}")

    if is_fraude:
        print(f"Motivo: {mensagem}")