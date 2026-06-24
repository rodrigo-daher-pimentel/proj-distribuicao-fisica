# Aula 8 — Heuristicas de Busca Local (2-opt + Relocate + Swap)

## Objetivo

Aplicar busca local sobre as 8 solucoes construtivas geradas na Aula 7 (NN/CW × C1-C4 com criterio `total_cost`), quantificar o ganho operacional dos tres movimentos da vizinhanca (2-opt intra-rota, Relocate inter-rota, Swap inter-rota) e identificar qual ponto de partida converge para o melhor otimo local. Esta aula corresponde ao Estagio 3 do pipeline da Sprint 2 (slide 25 da Aula 8).

## Movimentos implementados

### 2-opt (intra-rota)

- Remove dois arcos nao adjacentes da rota e reconecta invertendo o segmento entre eles.
- Mantem o mesmo conjunto de clientes em cada rota e o mesmo veiculo.
- Reduz distancia (e por consequencia custo variavel); custo fixo da rota e preservado.
- Estrategia: *first improvement* sobre a distancia da rota, com verificacao de viabilidade a cada candidato.

### Relocate (inter-rota)

- Remove um cliente de uma rota e o reinsere em uma posicao de outra rota.
- Pode redistribuir clientes, balancear carga e consolidar rotas (se uma rota for esvaziada, e removida).
- Estrategia: *first improvement* sobre o custo total da solucao, com viabilidade simultanea nas duas rotas envolvidas.

### Swap (inter-rota)

- Troca dois clientes de posicao simultaneamente entre rotas distintas — generalizacao do Relocate descrita nos slides 18-19 da Aula 8.
- Preserva o numero de clientes em cada rota (nao consolida) mas resolve a configuracao "cliente fora do lugar" entre rotas paralelas.
- Estrategia: *first improvement* sobre o custo total, viabilidade verificada nas duas rotas.

## Criterio de aceitacao

Melhoria estrita (`< - 1e-6`): um movimento so e aceito se reduz custo (ou distancia, no caso do 2-opt) e mantem viabilidade de capacidade e jornada. Nao ha aceitacao de pioras temporarias — metaheuristicas como Simulated Annealing e ILS ficam para a Sprint 3.

## Parametros

Identicos aos das Aulas 4 e 7: FIO 650 kg / R$ 250, VUC 3.000 kg / R$ 550, R$ 1,50/km, 40 km/h, jornada 8 h, atendimento 15 min/cliente.

## Resultados — pipeline completo

| Heur. | Inst. | Custo inicial | Custo 2-opt | Custo Relocate | Custo Swap | Ganho total |
|-------|-------|---------------|-------------|----------------|------------|-------------|
| NN | C1 | 430,60 | 422,38 | 422,38 | 422,38 | **-1,91 %** |
| NN | C2 | 801,08 | 760,86 | 712,49 | 712,49 | **-11,06 %** |
| NN | C3 | 1.084,86 | 1.065,66 | 1.062,31 | **1.043,69** | **-3,80 %** |
| NN | C4 | 1.527,56 | 1.506,04 | 1.431,50 | **1.410,00** | **-7,70 %** |
| CW | C1 | 423,63 | 422,38 | 422,38 | 422,38 | -0,29 % |
| CW | C2 | 712,06 | 712,05 | 712,05 | 712,05 | 0,00 % |
| CW | C3 | 1.048,29 | 1.047,99 | 1.047,99 | 1.047,99 | -0,03 % |
| CW | C4 | 1.410,39 | 1.410,21 | 1.410,21 | 1.410,21 | -0,01 % |

Zero violacoes de capacidade ou jornada em qualquer etapa. O Swap contribui marginalmente em NN-C3 (-1,75 % sobre o pos-Relocate) e NN-C4 (-1,50 %), nas instancias onde o Relocate tinha deixado clientes em rotas paralelas geograficamente trocadas.

## NN+BL × CW+BL — vencedor por instancia (pipeline completo)

| Inst. | NN+BL (R$) | CW+BL (R$) | Vencedor | Vantagem |
|-------|------------|------------|----------|----------|
| C1 | 422,38 | 422,38 | empate | 0 % |
| C2 | 712,49 | 712,05 | CW+BL | -0,06 % |
| C3 | **1.043,69** | 1.047,99 | **NN+BL** | -0,41 % |
| C4 | **1.410,00** | 1.410,21 | **NN+BL** | -0,02 % |

Com o Swap incluido, o NN+BL passa a vencer o CW+BL em C3 e C4 — inversao do resultado obtido com o pipeline truncado em 2-opt + Relocate. A leitura dialoga diretamente com os slides 23-24 da Aula 8: "NAO SIGNIFICA que CW + busca local e sempre melhor"; o NN parte de rotas com cruzamentos e clientes mal alocados que dao espaco substancial para a busca local refinar.

## Comparacao com o exato (Aula 4)

| Inst. | Exato (R$) | Status | Melhor heur+BL | Gap |
|-------|-----------|--------|-----------------|-----|
| C1 | 422,38 | optimal | 422,38 (CW+BL) | **0,00 %** |
| C2 | 754,04 | optimal | 712,05 (CW+BL) | **-5,57 %** |
| C3 | 769,65 | maxTimeLimit | 1.043,69 (NN+BL) | +35,61 % |
| C4 | 858,31 | maxTimeLimit | 1.410,00 (NN+BL) | +64,28 % |

Em C1 a heuristica refinada iguala o otimo global; em C2 supera o exato em 5,57 % (assimetria pela restricao de saida unica por tipo no MILP da Aula 4). Em C3 e C4 o gap aparente reflete a diferenca de regime — o exato consolida tudo em um unico VUC (nao permitido pela formulacao atual), enquanto a heuristica mantem multiplas rotas Fiorino — nao desvantagem genuina do metodo heuristico.

## Utilizacao de capacidade e jornada por rota (secao 9.1 do notebook)

Tabela por rota (carga em kg, util_cap %, tempo h, util_jorn %) das 18 rotas das solucoes pos-Swap.

- Sete das 18 rotas operam acima de 97 % da jornada de 8 h (NN-C4 rota 4, NN-C3 rota 2, CW-C3 rota 1, CW-C4 rotas 1 e 2).
- Tres rotas operam simultaneamente acima de 95 % de capacidade (NN-C3 rotas 1 e 2, NN-C4 rota 3, CW-C4 rota 1).
- As duas rotas VUC do CW (C3 rota 1, C4 rota 3) usam apenas ~26 % da capacidade nominal de 3.000 kg, mas suas cargas absolutas (787,8 kg e 768,9 kg) ja excedem o limite do FIO (650 kg) — VUC entra porque o cluster consolidado nao cabe em um FIO, nao porque saturou o VUC.

## Distancia em linha reta × rota operacional real (secao 11.1)

Argumento sobre a distancia Haversine como limite inferior da distancia viaria real, com identificacao dos pares de clientes em latitudes opostas em relacao ao deposito (Caxias, lat -23,06). O par mais longo em C4 — clientes 37 (CEP 26210-000) e 46 (CEP 23058-281) — registra 83,06 km Haversine; a distancia viaria real entre esses pontos passa pela BR-040 ou BR-101 + Avenida Brasil e fica entre 95 e 110 km. A consequencia operacional: rotas geometricamente curtas no modelo podem ser inviaveis no terreno; uso pratico requer substituir D Haversine por matriz de distancias reais via OSRM/Google/HERE antes da execucao.

## Trade-off computacional

- 2-opt: O(n²) por rota, sub-50 ms em todas as 8 chamadas.
- Relocate: O(k² × n²), domina o tempo total. Em NN-C4 chega a 3,15 s (unica chamada do notebook em escala de segundos); em CW-C4 cai para 220 ms.
- Swap: O(k² × n²) tambem, mas com peso menor por nao exigir copia profunda da solucao a cada candidato invalido. Maximo de 244 ms em NN-C4.
- O custo do Relocate + Swap so se paga quando a solucao inicial tem desbalanceamentos entre rotas — caso tipico do NN. Sobre o CW, o pipeline completo termina em < 290 ms na maior instancia e nao encontra melhoria.

## Recomendacao operacional

Para a Prolog, o protocolo recomendado e:

1. Gerar tanto NN quanto CW como solucoes iniciais (custo combinado < 40 ms na maior instancia).
2. Aplicar o pipeline completo (2-opt + Relocate + Swap) em ambas.
3. Selecionar a de menor custo total.

Sob esse protocolo, **NN + busca local vence em C3 e C4** (graças ao Swap), e o **CW + busca local vence em C1 e C2**. O custo computacional total fica abaixo de 3,5 s na maior instancia.

## Arquivos gerados

```
Aulas/8/Aula8_Busca_Local/
├── notebook.ipynb                              # notebook completo
├── notebook.md                                  # versao markdown (graphify)
├── README.md                                    # este arquivo
├── images/                                      # plots extraidos
│   ├── notebook_44_0.png ... notebook_44_3.png  # rotas C1-C4 (CW inicial vs NN+BL)
│   └── notebook_52_0.png                        # custos exato vs heuristicas BL
└── files/                                       # 8 JSONs finais (pos-Swap)
    ├── solution_busca_local_nn_C1.json
    ├── ...
    └── solution_busca_local_cw_C4.json
```

Formato do JSON (entrada para metaheuristicas da Sprint 3):

```json
{
  "heuristic_initial": "NN" | "CW",
  "instance": "C1" | "C2" | "C3" | "C4",
  "criterion": "total_cost",
  "pipeline": ["initial", "2-opt", "relocate", "swap"],
  "solution": [
    {"route_id": 1, "vehicle": "FIO" | "VUC", "route": [0, ..., 0]}
  ],
  "metrics": {...},
  "elapsed_s": {"2opt": float, "relocate": float, "swap": float}
}
```

## Pendencias para a Sprint 3

- Metaheuristicas (Simulated Annealing, ILS, Algoritmos Geneticos) capazes de aceitar pioras temporarias para romper a barreira entre regimes de frota que mantem o gap em C3 e C4 contra a solucao "tudo em um VUC" do exato.
- Refatoracao do MILP da Aula 4 removendo a restricao de saida unica por tipo, para tornar a comparacao com o exato menos assimetrica em C3 e C4.
- Substituir matriz Haversine por distancias viarias reais (OSRM/Google) para validar viabilidade operacional das rotas selecionadas.
