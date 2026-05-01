# Aula 3 — Modelagem Matematica do CVRP (Parte 1)

## Objetivo

Formular e implementar um modelo de Programacao Linear Inteira Mista (MILP) para o CVRP usando Pyomo + Gurobi. O modelo desta etapa e propositalmente incompleto: nao inclui restricoes de eliminacao de subtours (MTZ), para evidenciar a importancia dessas restricoes na formulacao.

## Modelo matematico

### Variaveis de decisao

- $x_{ij} \in \{0, 1\}$: 1 se o veiculo percorre o arco $i \to j$

### Funcao objetivo

Minimizar custo variavel (distancia) + custo fixo por veiculo:

$$\min \sum_{(i,j) \in A} c_{ij} \cdot x_{ij} + f \cdot m$$

onde $m = \sum_{j \in C} x_{0j}$ (numero de veiculos = arcos saindo do deposito).

### Restricoes implementadas

1. **Visita unica** — cada cliente tem exatamente 1 arco de entrada e 1 de saida
2. **Conservacao de fluxo** — para cada cliente, fluxo de entrada = fluxo de saida
3. **Balanco no deposito** — numero de saidas = numero de retornos ao deposito
4. **Capacidade agregada** — demanda total <= Q * m

### Restricoes ausentes (propositalmente)

- Eliminacao de subtours (MTZ) — sera adicionada na Aula 4
- Jornada maxima como restricao do modelo (apenas validada em pos-processamento)

## Parametros

| Parametro | Valor |
|-----------|-------|
| Frota | Homogenea (somente VUC) |
| Capacidade VUC (Q) | 3.000 kg |
| Custo fixo VUC (f) | R$ 550/dia |
| Jornada maxima (H) | 8 h |
| Velocidade media (v) | 40 km/h |
| Tempo de atendimento (s) | 15 min/cliente |
| Solver | Gurobi 13.0.1 (licenca academica PUC-Rio) |
| TimeLimit | 120 s |

## Resultados — Metodo exato sem MTZ

| Instancia | Clientes | Demanda (kg) | Custo (R$) | Veiculos | Subtours | Tempo (s) | Status |
|-----------|----------|-------------|-----------|----------|----------|-----------|--------|
| C1_10 | 10 | 141,6 | 668,80 | 1 | 4 | 0,03 | optimal |
| C2_25 | 25 | 754,5 | 666,15 | 1 | 11 | 0,06 | optimal |
| C3_40 | 40 | 1.295,3 | 678,34 | 1 | 19 | 0,08 | optimal |
| C4_60 | 60 | 1.958,1 | 738,63 | 1 | 27 | 0,17 | optimal |

### Observacoes

- Todas as instancias foram resolvidas de forma otima em menos de 0,2 s.
- O solver utiliza apenas 1 veiculo em todos os casos (minimiza custo fixo).
- Praticamente todos os clientes ficam em subtours desconectados do deposito: apenas 1-2 clientes sao atendidos via rota que passa pelo CD.
- Os custos reportados sao artificialmente baixos porque o solver "trapaceia" com subtours — as rotas nao sao operacionalmente viaveis.
- Isso demonstra que a formulacao sem MTZ esta matematicamente correta mas operacionalmente incompleta.

### Conclusao

O solver segue exatamente o que a formulacao pede. O problema nao e do solver, e da formulacao. Sem restricoes de eliminacao de subtours, ciclos desconectados do deposito sao "solucoes otimas" validas. A Aula 4 corrigira isso com restricoes MTZ.

## Arquivos

```
Aulas/3/
├── Aula3_Modelagem_MILP.ipynb    # notebook completo (Aula 3)
└── README.md                      # este arquivo
```

## Pendencias para proximas aulas

- ~~Adicionar restricoes MTZ (Aula 4)~~ — feito na Aula 4
- Modelar jornada maxima como restricao (nao apenas validacao) — validada em pos-processamento por enquanto
- ~~Re-executar experimentos com modelo completo~~ — feito na Aula 4 (C1–C4 com MTZ + frota heterogenea)
- ~~Comparar resultados com/sem MTZ~~ — feito nos experimentos da Aula 5 (cells 28–29 do notebook da Aula 4)
