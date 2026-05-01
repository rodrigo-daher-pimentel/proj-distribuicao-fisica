# Aula 4 — Modelagem Matematica do CVRP (Parte 2) + Experimentos Sprint 1

## Objetivo

Evolucao do modelo da Aula 3: frota heterogenea (Fiorino + VUC), restricoes MTZ para eliminacao de subtours, e experimentos computacionais sistematicos exigidos na Aula 5.

## Evolucao em relacao a Aula 3

- Aula 3: frota homogenea (so VUC), sem MTZ — solucoes com subtours.
- Aula 4: frota heterogenea (FIO + VUC), restricoes MTZ — solucoes conectadas ao deposito.

## Modelo matematico

### Variaveis de decisao

- $x_{ijk} \in \{0, 1\}$: 1 se o veiculo tipo $k$ percorre o arco $i \to j$
- $y_k \in \{0, 1\}$: 1 se o veiculo tipo $k$ e ativado
- $u_i$: variavel auxiliar MTZ (ordem de visita do cliente $i$)

### Funcao objetivo

Minimizar custo variavel (deslocamento) + custo fixo (ativacao de veiculos):

$$\min \sum_{(i,j,k) \in A} c_{ij} \cdot x_{ijk} + \sum_{k \in K} f_k \cdot y_k$$

### Restricoes

1. Visita unica (grau de entrada e saida = 1 para cada cliente)
2. Balanco no deposito (saidas = retornos por tipo de veiculo)
3. Saida unica por tipo (cada tipo faz no maximo 1 rota)
4. Capacidade agregada heterogenea
5. Conservacao de fluxo por tipo de veiculo
6. MTZ — eliminacao de subtours ($u_i - u_j + (n-1) \cdot \sum_k x_{ijk} \leq n-2$)
7. Ativacao de veiculos (se sai do deposito, y[k]=1)

### Parametros

| Parametro | Fiorino | VUC |
|-----------|---------|-----|
| Capacidade (kg) | 650 | 3.000 |
| Custo fixo diario (R$) | 250 | 550 |

Velocidade media: 40 km/h | Jornada: 8 h (validada em pos-processamento) | Solver: Gurobi 13.0.1

## Resultados — Metodo exato com MTZ + frota heterogenea

| Instancia | Clientes | Custo (R$) | VUC | FIO | Rotas | Tempo (s) | Status |
|-----------|----------|-----------|-----|-----|-------|-----------|--------|
| C1_10 | 10 | 422,38 | 0 | 1 | 1 | 0,27 | optimal |
| C2_25 | 25 | 754,04 | 1 | 0 | 1 | 52,69 | optimal |
| C3_40 | 40 | 769,65 | 1 | 0 | 1 | 300,73 | maxTimeLimit |
| C4_60 | 60 | 858,31 | 1 | 0 | 1 | 300,88 | maxTimeLimit |

## Experimentos computacionais — Aula 5

Experimentos adicionados ao notebook conforme exigencias da Aula 5 (Acompanhamento Sprint 1).

### Exp. 1: Comparacao com/sem MTZ (obrigatorio)

| Instancia | COM MTZ (R$) | Restricoes | Tempo | SEM MTZ (R$) | Restricoes | Subtours | Tempo |
|-----------|-------------|-----------|-------|-------------|-----------|----------|-------|
| C1_10 | 422,38 | 139 | 0,79s | 368,80 | 49 | 4 | 0,13s |
| C2_25 | 754,04 | 709 | 65,01s | 666,15 | 109 | 11 | 0,20s |
| C3_40 | 769,65 | 1.729 | 300,98s | 676,69 | 169 | 19 | 0,17s |
| C4_60 | 858,31 | 3.789 | 300,54s | 734,59 | 249 | 28 | 0,18s |

Sem MTZ o custo e menor, mas as solucoes contem subtours — sao inviaveis operacionalmente.

### Exp. 2: Gap x time limit (obrigatorio + opcional)

| Instancia | TL=30s | Gap | TL=60s | Gap | TL=300s | Gap |
|-----------|--------|-----|--------|-----|---------|-----|
| C1_10 | 422,38 | 0,00% | 422,38 | 0,00% | 422,38 | 0,00% |
| C2_25 | 754,04 | 0,45% | 754,04 | 0,14% | 754,04 | 0,00% |
| C3_40 | 792,17 | 7,79% | 776,20 | 5,80% | 769,65 | 3,56% |
| C4_60 | 875,61 | 7,03% | 862,20 | 5,15% | 858,31 | 4,37% |

Mais tempo melhora a solucao incumbente significativamente para C3 e C4.

### Exp. 3: Comparacao de solvers (obrigatorio)

| Instancia | Gurobi (R$) | Tempo | HiGHS (R$) | Tempo |
|-----------|------------ |-------|------------|-------|
| C1_10 | 422,38 | 0,58s | 422,38 | 6,39s |
| C2_25 | 754,04 | 77,05s | 760,18 | 300,23s |

Gurobi e significativamente mais rapido e encontra solucoes de melhor qualidade.

### Analise de sensibilidade (opcional)

Realizadas na secao original do notebook (cell 21):
- Variacao do custo fixo do VUC (R$ 550 → R$ 1.500)
- Variacao da capacidade do VUC (3.000 kg → 1.000 kg)

## Arquivos

```
Aulas/4/
├── Aula4_Modelagem_MILP_Parte2/
│   └── notebook.ipynb              # notebook do grupo (completo, executado)
├── ENG_4560_Aula_4_.../
│   └── notebook.ipynb              # template do professor (com TODOs)
├── ENG 4560 - Aula 4 - ....pdf     # slides da aula
├── ENG 4010 - Aula 4B - ....pdf    # slides de gestao (Canvas, E/NaoE)
└── README.md                       # este arquivo
```
