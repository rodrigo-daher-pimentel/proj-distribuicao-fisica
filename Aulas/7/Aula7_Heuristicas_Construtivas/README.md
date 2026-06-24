# Aula 7 — Heuristicas Construtivas para o CVRP com Frota Heterogenea

## Objetivo

Implementar duas heuristicas construtivas — Nearest Neighbor (NN) e Clarke-Wright Savings (CW) — para o CVRP com frota heterogenea e restricao de jornada, e compara-las entre si e contra o modelo exato da Sprint 1. Esta aula corresponde ao Estagio 1 do pipeline da Sprint 2 (slide 25 da Aula 8) e fornece as solucoes iniciais consumidas pela Aula 8.

## Evolucao em relacao a Sprint 1

- Aula 3: MILP sem MTZ, frota homogenea (so VUC) — solucoes com subtours.
- Aula 4: MILP com MTZ, frota heterogenea (FIO + VUC) + restricao implicita de saida unica por tipo.
- Aula 7: heuristicas construtivas com frota heterogenea, restricao de jornada de 8 h embutida no proprio algoritmo, decisao dinamica do veiculo rota a rota.

## Heuristicas implementadas

### Nearest Neighbor (NN)

- Inicia no deposito; a cada passo, escolhe o cliente viavel mais proximo do no atual.
- Cliente e viavel se a insercao mantem (i) carga acumulada ≤ capacidade do veiculo e (ii) tempo total da rota (incluindo retorno ao deposito) ≤ 8 h.
- Quando nao ha mais cliente viavel, a rota e fechada e uma nova rota e aberta.
- Ao abrir cada rota, simula com FIO e com VUC e escolhe o veiculo segundo o criterio adotado.

### Clarke-Wright Savings (CW)

- Solucao inicial: uma rota por cliente, `[0, i, 0]`.
- Calcula `s_ij = d(0,i) + d(0,j) - d(i,j)` para todos os pares e ordena em ordem decrescente.
- Para cada par, testa a fusao das rotas que contem `i` e `j` se ambos estiverem em extremidades; aceita se a rota fundida e viavel em capacidade e jornada.
- Cada fusao re-simula com FIO e VUC e escolhe o melhor veiculo.

### Criterios de selecao do veiculo

- `total_cost`: menor custo total da rota.
- `cost_per_client`: menor custo total dividido pelo numero de clientes atendidos.

Ambos sao rodados sobre as 4 instancias (16 execucoes para cada heuristica).

## Parametros

| Parametro | Valor |
|-----------|-------|
| Fiorino — capacidade | 650 kg |
| Fiorino — custo fixo diario | R$ 250 |
| VUC — capacidade | 3.000 kg |
| VUC — custo fixo diario | R$ 550 |
| Custo variavel | R$ 1,50/km |
| Velocidade media | 40 km/h |
| Jornada maxima | 8 h |
| Tempo de atendimento | 15 min/cliente |

## Resultados — heuristicas construtivas (criterio `total_cost`)

| Instancia | Clientes | NN custo (R$) | NN rotas | CW custo (R$) | CW rotas | Ganho CW |
|-----------|----------|---------------|----------|---------------|----------|----------|
| C1 | 10 | 430,60 | 1 FIO | 423,63 | 1 FIO | -1,62 % |
| C2 | 25 | 801,08 | 2 FIO | 712,06 | 2 FIO | -11,11 % |
| C3 | 40 | 1.084,86 | 3 FIO | 1.048,29 | 1 FIO + 1 VUC | -3,37 % |
| C4 | 60 | 1.527,56 | 4 FIO | 1.410,39 | 2 FIO + 1 VUC | -7,67 % |

Tempo computacional sub-20 ms em todas as instancias para ambas as heuristicas.

## Comparacao entre criterios

`total_cost` e `cost_per_client` produzem **solucoes identicas** em todas as combinacoes heuristica × instancia. A explicacao e estrutural: como nenhum cliente extrapola individualmente a capacidade do Fiorino (maior demanda = 206 kg em C4), o NN nunca abre rota com VUC; no CW, o VUC so e escolhido por capacidade na rota fundida, situacao em que FIO nao e candidato e a comparacao entre criterios fica vazia.

## Comparacao com o exato (Aula 4)

| Instancia | Exato (R$) | Status | CW (R$) | Gap CW vs exato |
|-----------|-----------|--------|---------|------------------|
| C1 | 422,38 | optimal | 423,63 | +0,30 % |
| C2 | 754,04 | optimal | 712,06 | **-5,57 %** |
| C3 | 769,65 | maxTimeLimit | 1.048,29 | +36,21 % |
| C4 | 858,31 | maxTimeLimit | 1.410,39 | +64,32 % |

Em C2 a heuristica supera o exato porque a formulacao MILP da Aula 4 incorpora uma restricao adicional (saida unica por tipo de veiculo) que proibe configuracoes com mais de uma rota Fiorino — justamente a melhor escolha para C2. Em C3 e C4 o gap aparente reflete a mesma assimetria: o exato consolida tudo em um unico VUC (regime nao acessivel a heuristica com a granularidade atual), nao desvantagem genuina do metodo heuristico.

## Diagnostico da restricao de jornada

Sete das dezoito rotas geradas pelos dois algoritmos operam acima de 7 h, com folgas pequenas — entre 8 min (C4) e 30 min (C2). Nenhuma rota viola o limite de 8 h, mas a margem e apertada nas instancias maiores. O NN preenche rotas de forma mais agressiva (4 rotas proximas do limite contra 3 do CW), enquanto o CW para antes — fusoes que aproximariam demais o tempo de 8 h sao rejeitadas mesmo quando o saving seria atrativo.

### Identificacao dos clientes e regioes criticos (secao 12.1 do notebook)

As 158 ocorrencias de clientes em rotas com tempo > 7 h concentram-se em 59 clientes distintos distribuidos em tres faixas de CEP:

- **25xxx** — Mage, Belford Roxo, Duque de Caxias (Baixada Fluminense ao norte do deposito).
- **21xxx** — Bangu, Realengo, Padre Miguel (Zona Norte/Oeste do Rio ao sul).
- **22xxx-23xxx** — Bangu/Santa Cruz (Zona Oeste extrema).

CEPs mais recorrentes: 25931 (Mage), 23530 (Bangu), 25520 (Mage) — todos a >10 km do deposito em Caxias.

**Clientes que forcam estruturalmente o uso do VUC** (sem eles a carga consolidada cairia abaixo dos 650 kg do FIO):

- Em C4 rota VUC do CW: cliente 60 (CEP 26311110, 206,0 kg — maior demanda da base) e cliente 57 (CEP 22631002, 149,6 kg). A remocao de qualquer um traria a carga para baixo do limite FIO.
- Em C3 rota VUC do CW: clientes 27 (CEP 26280376, 153,6 kg), 17 (CEP 25580020, 78,0 kg), 22 (CEP 23550265, 66,0 kg), 39 (66,6 kg) e 13 (59,8 kg) compoem 423,9 kg dos 788,0 kg totais da rota.

Operacionalmente: mudancas em qualquer um desses pedidos (revisao, promocao, alteracao de volume) movem a fronteira VUC × FIO da decisao de frota.

## Recomendacao para a Sprint 2

O **Clarke-Wright** e o ponto de partida preferivel para a busca local da Aula 8: vence o NN em todas as quatro instancias, gera rotas geograficamente coerentes (visualmente sem cruzamentos), e ja produz a configuracao mista FIO+VUC que reduz custo total em C3 e C4.

## Arquivos gerados

```
Aulas/7/Aula7_Heuristicas_Construtivas/
├── notebook.ipynb              # notebook completo (45 cells)
├── notebook.md                  # versao markdown (graphify)
├── README.md                    # este arquivo
├── images/                     # plots extraidos pelo nbconvert
│   ├── notebook_36_0.png       # custos exato vs heuristicas (barras)
│   └── notebook_39_0.png ... notebook_39_3.png  # rotas NN vs CW por instancia
├── files/                       # 16 JSONs (NN/CW × C1-C4 × 2 criterios)
│   ├── solution_nn_het_C1_total_cost.json
│   ├── solution_nn_het_C1_cost_per_client.json
│   ├── ...
│   └── solution_cw_het_C4_cost_per_client.json
└── graphify-out/                # saida do graphify
```

Formato do JSON (consumido pela Aula 8):

```json
{
  "heuristic": "NN" | "CW",
  "instance": "C1" | "C2" | "C3" | "C4",
  "criterion": "total_cost" | "cost_per_client",
  "solution": [
    {"route_id": 1, "vehicle": "FIO" | "VUC", "route": [0, ..., 0], "served_clients": [...]}
  ],
  "metrics": {...},
  "elapsed_s": float
}
```

## Pendencias para proximas aulas

- ~~Aplicar 2-opt e Relocate sobre as solucoes salvas~~ — feito na Aula 8.
- Avaliar metaheuristicas (Simulated Annealing, ILS, GA) capazes de aceitar pioras temporarias e romper o regime de frota — Sprint 3.
- Refinar a formulacao MILP da Aula 4 removendo a restricao de saida unica por tipo, para tornar a comparacao com o exato menos assimetrica.
