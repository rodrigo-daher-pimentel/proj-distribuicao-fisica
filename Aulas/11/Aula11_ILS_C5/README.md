# Aula 11 — Tarefa 12 (Desafio Aberto): ILS na Instancia Secreta C5

## Objetivo

Entregar a melhor solucao possivel para a instancia secreta C5 (`COMP_ILS_SECRET_20_seed555`, 20 clientes) sob o regime livre da Tarefa 12 do Sprint Planning #3 — adaptacao livre de solucao inicial, perturbacao, criterio de aceitacao, numero de iteracoes, intensidade de perturbacao, uso de Swap, tolerancia, seeds e combinacao de estrategias.

## Solucao entregue

| Campo | Valor |
|-------|-------|
| Custo final | **R$ 609,90** |
| Numero de rotas | 2 (2 FIO + 0 VUC) |
| Distancia total | 73,27 km |
| Solucao inicial | Nearest Neighbor |
| Perturbacao | Relocate aleatorio intensificado (k=3) |
| Aceitacao | Estrita |
| Busca local | 2-opt + Relocate + Swap |
| Iteracoes | 300 |
| Seed vencedora | 42 |
| Iteracao da melhor | 207 |
| Tempo computacional | 3,45 s |

## Rotas finais

- **Rota 1 (FIO)**: `[0, 20, 7, 1, 5, 10, 9, 17, 4, 15, 19, 12, 3, 18, 11, 16, 8, 2, 0]` — 17 clientes, 526,08 kg, 63,13 km, 4,9 h.
- **Rota 2 (FIO)**: `[0, 13, 14, 6, 0]` — 3 clientes, 188,44 kg, 10,14 km, 1,2 h.

Zero violacoes de capacidade ou jornada.

## Estrategia adotada

30 execucoes de ILS combinando:

- **3 configuracoes**: A2 (double-bridge + estrita), A4 (double-bridge + tolerancia 3%), P1k3 (relocate aleatorio com k=3 + estrita).
- **5 seeds**: 42, 123, 555, 777, 2024.
- **2 trilhas de solucao inicial**: NN+busca local com Swap, CW+busca local com Swap.

Cada execucao com 300 iteracoes. Tempo total: 123,4 s.

## Resultados agregados por configuracao

| Trilha | Config | Custo min | Custo medio | Std | Tempo medio (s) |
|--------|--------|-----------|-------------|-----|------------------|
| NN | P1k3 | **609,90** | 611,30 | 1,28 | 3,24 |
| NN | A2 | 649,41 | 649,41 | 0,00 | 6,25 |
| NN | A4 | 649,41 | 649,41 | 0,00 | 4,20 |
| CW | A2 | 654,08 | 654,08 | 0,00 | 5,30 |
| CW | A4 | 654,08 | 654,08 | 0,00 | 4,90 |
| CW | P1k3 | 655,58 | 655,58 | 0,00 | 0,77 |

A configuracao vencedora (NN+P1k3) e a unica com variancia entre seeds — sinal de exploracao mais ampla do espaco. Todas as outras configuracoes convergem deterministicamente.

## Tarefa 13: a estrategia da Sprint controlada vale para C5?

A estrategia da Equipe 2 na Sprint controlada (double-bridge + estrita, sem Swap, 100 iter, seed 42), aplicada na C5, entrega **R$ 684,96** — R$ 75,06 acima da solucao entregue (−10,96%). A configuracao definida no slide 21 da Aula 11 nao e otima para esta instancia.

Tres ajustes simultaneos foram necessarios:

1. Trocar a perturbacao para `relocate_random` com k=3 (a double-bridge ficou presa em R$ 649,41 com qualquer seed da trilha NN).
2. Habilitar Swap na busca local intra-ILS.
3. Ampliar o orcamento para 300 iteracoes (a melhor solucao foi encontrada na iteracao 207).

Mensagem para o relatorio final da Sprint 3: a configuracao definida pela tabela do slide 21 e uma boa premissa inicial para o experimento controlado, mas a Tarefa 12 mostra empiricamente que a calibracao por instancia faz diferenca real.

## Estrutura de arquivos

```
Aulas/11/Aula11_ILS_C5/
├── notebook.ipynb                       # notebook completo da Tarefa 12
├── README.md                             # este arquivo
├── images/
│   ├── convergencia_c5_tarefa12.png      # vencedora + 5 seeds NN+P1k3
│   └── solucao_final_c5.png              # rotas finais entregues
└── files/
    ├── solucao_competicao_c5.json        # entrega para a competicao
    ├── matriz_experimentos_c5.csv        # 30 execucoes do experimento fatorial
    └── history_NN_P1k3_seed42.csv        # historico da execucao vencedora
```
