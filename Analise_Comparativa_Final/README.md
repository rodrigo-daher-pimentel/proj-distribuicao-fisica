# Análise Comparativa Final — Exato, Construtivo, Busca Local e ILS

## Objetivo

Consolidar, numa única comparação, as quatro famílias de método desenvolvidas ao longo das Sprints 1 e 2 para o CVRP da Prolog e responder à pergunta da Sprint 3: qual abordagem é mais adequada para cada tamanho de instância, em custo, tempo e qualidade. Entregável da EAP 1.4.3 (Relatório de Análise Comparativa Final) e do card "Experimentos Computacionais Finais".

Métodos comparados nas instâncias C1–C4 (10, 25, 40 e 60 clientes):

- Exato — MILP com MTZ e frota heterogênea, Gurobi com limite de 300 s (Aula 4).
- Construtivo — Nearest Neighbor (Aula 7).
- Busca local — 2-opt + Relocate + Swap (Aula 8).
- Metaheurística — Iterated Local Search, configuração da Equipe 2: double-bridge, critério estrito, `k = 2`, 100 iterações, semente 42 (Aulas 11 e 12).

## Decisões metodológicas

Dois problemas de comparabilidade que os notebooks isolados não resolviam orientam a consolidação:

- **Tempo.** Medições feitas em sessões distintas não são comparáveis, porque o relógio depende da carga da máquina. As etapas de custo computacional não desprezível — busca local e ILS — são reexecutadas aqui numa única sessão; o exato e a construtiva têm tempos citados de suas aulas (o exato não é reexecutado por custar até 300 s; a construtiva por rodar em frações de segundo). O custo de toda solução é reavaliado pela mesma função objetivo unificada.
- **Gap de otimalidade.** O MILP da Aula 4 resolve uma formulação relaxada (frota como tipo único por veículo, capacidade agregada, sem jornada de 8 h). Suas soluções para C2–C4 violam a jornada e são inviáveis no problema real. O gap contra o exato só é legítimo onde os regimes coincidem — apenas em C1. Para C2–C4, a referência de qualidade é a melhor solução viável encontrada (o ILS). Essa restrição foi estabelecida na Aula 11.

## Resultados principais

| Método | C1 (10) | C2 (25) | C3 (40) | C4 (60) |
| ------ | ------- | ------- | ------- | ------- |
| Exato (MILP) | **422,38** (0,27 s, ótimo) | 754,04 (52,7 s, inviável) | 769,65 (300 s, inviável) | 858,31 (300 s, inviável) |
| Construtiva (NN) | 430,60 | 801,08 | 1.084,86 | 1.527,56 |
| Busca local | 422,38 | 712,49 | 1.043,69 | 1.410,00 |
| ILS | 422,38 | **710,47** | **775,01** | **1.383,14** |

Custos em R$. O exato é viável apenas em C1. Em negrito, a melhor solução viável por instância.

Leitura por faixa de tamanho:

- **C1 (10 clientes):** o exato prova o ótimo de R$ 422,38 em 0,27 s; busca local e ILS alcançam o mesmo valor. O exato é a ferramenta certa, mas as heurísticas o igualam em tempo igualmente desprezível.
- **C2 (25 clientes):** o exato já gasta 52,7 s e devolve uma solução inviável e mais cara (R$ 754,04) que a heurística (R$ 710,47), porque sua formulação obriga um único VUC. Ponto de virada da intratabilidade.
- **C3 e C4 (40 e 60 clientes):** o exato estoura os 300 s sem provar otimalidade e produz rotas de 10 h e 15 h, inexequíveis. O pipeline heurístico é a única via viável.

A divisão de trabalho dentro do pipeline se confirma: a busca local faz o grosso da economia (em C4, leva a construtiva de 10,44% para 1,94% acima do melhor viável) e o ILS apara o restante. A exceção é C3, onde a busca local fica 34,67% acima do ILS — efeito de não idempotência documentado na Aula 12, recuperado pela reaplicação de 2-opt + Relocate na iteração 0 do ILS, não pelas perturbações.

## Recomendação

Para a operação da Prolog, em qualquer porte, o pipeline heurístico: Nearest Neighbor como ponto de partida, busca local 2-opt + Relocate + Swap como base obrigatória (menos de 3 s mesmo em C4) e ILS da Equipe 2 (double-bridge, estrito, `k = 2`, 50 a 100 iterações) como polimento final quando houver janela de cálculo. O exato fica reservado a instâncias muito pequenas, onde resolve em segundos e sua formulação coincide com as restrições reais — nesta base, apenas C1.

## Estrutura de arquivos

```
Analise_Comparativa_Final/
├── notebook.ipynb                    # notebook completo
├── notebook.md                       # export legível (sem código)
├── README.md                         # este arquivo
├── images/
│   └── comparacao_consolidada.png    # painel de custo, tempo, qualidade e escalabilidade
└── files/
    └── comparacao_consolidada.csv    # tabela método x instância x custo x tempo x gap
```

## Como executar

O notebook lê as instâncias de `../Aulas/2/datasets/` e as soluções salvas de cada método em `../Aulas/7/`, `../Aulas/8/` e `../Aulas/11/`. A raiz do projeto é detectada automaticamente, então o notebook roda independentemente do diretório de trabalho. Basta abrir no JupyterLab e executar Restart & Run All; a reexecução do ILS leva cerca de meio minuto, dominada por C4. Os resultados de custo e gap são determinísticos (semente 42); apenas os tempos de relógio de busca local e ILS oscilam alguns por cento entre execuções.
