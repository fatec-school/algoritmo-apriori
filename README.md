#  Detecção Simples de Anomalias com Regras de Associação (Apriori)

## Descrição

Este projeto demonstra uma abordagem básica de **detecção de fraudes/anomalias em transações** utilizando **Mineração de Regras de Associação** com o algoritmo **Apriori**.

A ideia é identificar padrões frequentes de comportamento em transações históricas e utilizar esses padrões como referência para detectar operações potencialmente suspeitas.

---

## Objetivo

O sistema:

1. Cria uma base de transações simuladas.
2. Descobre padrões frequentes utilizando o algoritmo Apriori.
3. Gera regras de associação com alta confiança.
4. Avalia novas transações para identificar possíveis anomalias.

---

## Tecnologias Utilizadas

* Python 3
* Pandas
* Mlxtend

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

---

## Estrutura dos Dados

Cada linha representa uma transação e cada coluna representa uma característica:

| Característica        | Descrição                              |
| --------------------- | -------------------------------------- |
| Valor_Alto            | Transação de alto valor                |
| Internacional         | Transação realizada em outro país      |
| Nova_Conta            | Conta criada recentemente              |
| Horario_Noturno       | Operação realizada durante a noite     |
| Dispositivo_Conhecido | Dispositivo já utilizado anteriormente |

Exemplo:

```text
   Valor_Alto  Internacional  Nova_Conta  Horario_Noturno  Dispositivo_Conhecido
0           1              0           0                0                      1
1           0              0           1                0                      1
...
```

---

## Funcionamento

### 1. Geração dos Padrões Frequentes

O algoritmo Apriori identifica combinações de características que aparecem em pelo menos 30% das transações.

```python
frequent_itemsets = apriori(
    df,
    min_support=0.3,
    use_colnames=True
)
```

### 2. Geração das Regras

Após encontrar os conjuntos frequentes, são criadas regras de associação com confiança mínima de 80%.

```python
rules = association_rules(
    frequent_itemsets,
    metric="confidence",
    min_threshold=0.8
)
```

Exemplo de regra:

```text
{Valor_Alto} -> {Dispositivo_Conhecido}
Confiança: 100%
```

Isso significa que sempre que uma transação possui valor alto, ela também ocorre em um dispositivo conhecido dentro da base analisada.

---

## Detecção de Anomalias

A função `detectar_anomalia()` aplica regras simples para identificar comportamentos suspeitos.

### Regra 1

Transação internacional realizada em dispositivo desconhecido.

```python
if transacao['Internacional'] == 1 and transacao['Dispositivo_Conhecido'] == 0:
```

### Regra 2

Transação de valor alto realizada durante a madrugada/noite.

```python
if transacao['Horario_Noturno'] == 1 and transacao['Valor_Alto'] == 1:
```

Quando alguma dessas condições é satisfeita, a transação é marcada como suspeita.

---

## Exemplo de Teste

### Transação Normal

```python
{
    'Valor_Alto': 1,
    'Internacional': 0,
    'Nova_Conta': 0,
    'Horario_Noturno': 0,
    'Dispositivo_Conhecido': 1
}
```

Resultado:

```text
✅ NORMAL
```

---

### Transação Suspeita

```python
{
    'Valor_Alto': 1,
    'Internacional': 1,
    'Nova_Conta': 1,
    'Horario_Noturno': 1,
    'Dispositivo_Conhecido': 0
}
```

Resultado:

```text
⚠️ SUSPEITA
Motivo: Transação internacional de dispositivo desconhecido.
```

