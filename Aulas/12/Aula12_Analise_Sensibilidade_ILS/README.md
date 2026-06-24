# Aula 12 — Análise de Comportamento do ILS para o CVRP da Prolog

## Objetivo

Estudar o comportamento do Iterated Local Search (ILS) implementado na Aula 11, não mais a sua viabilidade. A análise responde a três perguntas com impacto direto no relatório da Sprint 3 e na escolha da configuração para a competição: como o resultado muda com os parâmetros `k` e `N` (sensibilidade), quando o algoritmo deixa de melhorar (convergência) e como ele se comporta em instâncias de tamanhos diferentes (escalabilidade).

O notebook adapta o código de referência da Aula 12 do professor para execução local, substituindo o `upload` do Colab pelo carregamento direto das instâncias da Aula 2 e das soluções pós-busca-local da Aula 8.

## Configuração da equipe

Equipe 2 (Grupo 2), conforme Sprint Planning #3:

- Perturbação: double-bridge
- Critério de aceitação: estrito
- Busca local intra-ILS: 2-opt + Relocate
- Semente: 42
- Instância de trabalho das Seções 1 e 2: C4 (60 clientes, trilha Nearest Neighbor)

## Resultados principais

### Seção 1 — Sensibilidade (instância de trabalho C4-NN)

Efeito de `k` (N = 80):

| k   | Custo final (R$) | Ganho total vs baseline | Tempo (s) |
| --- | ---------------- | ----------------------- | --------- |
| 1   | 1.384,25         | 1,83%                   | ~24       |
| 2   | **1.383,14**     | **1,90%**               | ~24       |
| 3   | 1.383,14         | 1,90%                   | ~24       |
| 4   | 1.383,14         | 1,90%                   | ~24       |

Sensibilidade fraca: qualquer `k ≥ 2` empata no melhor custo; `k = 2` é o melhor por margem desprezível.

Efeito de `N` (k = 2):

| N   | Custo final (R$) | Ganho marginal (R$) |
| --- | ---------------- | ------------------- |
| 20  | 1.383,53         | 26,47 (vs baseline) |
| 50  | 1.383,53         | 0,00                |
| 100 | 1.383,14         | 0,39                |
| 150 | 1.383,14         | 0,00                |
| 200 | 1.383,14         | 0,00                |

Retorno decrescente abrupto: N = 20 captura 1,88% dos 1,90% totais; não há melhoria após N = 100.

### Seção 2 — Convergência (C4-NN, k = 2, N = 150)

- Custo baseline (busca local Aula 8): R$ 1.410,00
- Custo na iteração 0 (após 2-opt + Relocate): R$ 1.386,86
- Custo final ILS: R$ 1.383,14
- Ganho metaheurístico puro (iter 0 → fim): 0,27%
- Última melhoria: iteração 51 de 150 (66% de iterações ociosas)
- Critério estrito (R$ 1.383,14) supera tolerância de 3% (R$ 1.383,53)

A regra automática rotula como estagnação, mas o cruzamento com a Seção 1 mostra convergência genuína por volta da iteração 51 — não há ganho ao aumentar `N` ou `k`. A fração ociosa reflete orçamento excessivo, não armadilha de ótimo local.

### Seção 3 — Escalabilidade (trilha NN, k = 2, N = 80)

| Inst. | n_cli | Custo BL | Custo iter 0 | Custo ILS | Ganho total | Ganho metaheurístico | Tempo (s) |
| ----- | ----- | -------- | ------------ | --------- | ----------- | -------------------- | --------- |
| C1    | 10    | 422,38   | 422,38       | 422,38    | 0,00%       | 0,000%               | 0,2       |
| C2    | 25    | 712,49   | 710,47       | 710,47    | 0,28%       | 0,000%               | 2,1       |
| C3    | 40    | 1.043,69 | 779,76       | 775,01    | 25,74%      | 0,609%               | 3,7       |
| C4    | 60    | 1.410,00 | 1.386,86     | 1.383,14  | 1,90%       | 0,268%               | 22,9      |

O ganho metaheurístico não escala com o tamanho (pico em C3, não em C4). O tempo cresce de forma super-linear: o salto C3 → C4 é de ~6× para 1,5× mais clientes.

## Achado central — a busca local faz o trabalho, não a metaheurística

O ganho aparente do ILS contra o baseline carregado mistura dois efeitos. O grande salto vem do 2-opt + Relocate reaplicado na iteração 0 (em C3, derruba o custo de R$ 1.043,69 para R$ 779,76 — o mesmo efeito de não idempotência documentado na Aula 11, agora quantificado). O ganho propriamente metaheurístico das perturbações fica entre 0,00% e 0,61% nas quatro instâncias. O ILS é um polimento final modesto e barato em instâncias pequenas, que se torna caro em instâncias grandes pelo custo do Relocate.

## Recomendação para a Prolog

- Manter o pipeline NN + busca local (2-opt + Relocate + Swap, como na Aula 8) como base.
- Ativar o ILS da Equipe 2 (double-bridge, estrito, k = 2) com orçamento de N = 50 a 100 iterações — faixa que esgota o ganho em poucas dezenas de segundos para até 60 clientes.
- Sob urgência, N = 20 entrega 98,6% do ganho em ~7 s.
- Para instâncias muito maiores (competição), o gargalo é o tempo por iteração; manter `N` baixo e, se preciso, restringir a vizinhança do Relocate, sem trocar o critério estrito (a tolerância não trouxe ganho).

## Estrutura de arquivos

```
Aulas/12/Aula12_Analise_Sensibilidade_ILS/
├── notebook.ipynb                         # notebook completo
├── README.md                              # este arquivo
├── images/
│   ├── sensibilidade_k.png                # convergência e custo final por k
│   ├── sensibilidade_N.png                # custo e ganho marginal por N
│   ├── diagnostico_convergencia.png       # painel de convergência (4 quadros)
│   ├── comparacao_criterios.png           # estrito vs. tolerância
│   └── escalabilidade.png                 # custos, ganho, tempo e convergência por instância
└── files/
    ├── sensibilidade_k_C4.csv             # tabela do experimento de k
    ├── sensibilidade_N_C4.csv             # tabela do experimento de N
    ├── historico_diagnostico_C4.csv       # histórico de convergência (N=150)
    ├── escalabilidade_C1_C4.csv           # resumo da escalabilidade
    └── solution_ils_sens_nn_C{1..4}.json  # soluções finais do ILS por instância
```

## Como executar

O notebook lê as instâncias de `../../2/datasets/Equipe_2_C*/` e as soluções baseline de `../../8/Aula8_Busca_Local/files/`. Basta abrir no JupyterLab (com o diretório de trabalho na pasta do notebook) e executar Restart & Run All. A execução completa leva alguns minutos, dominada pelos experimentos de `N` e pelo Relocate em C4. Reprodutibilidade verificada com kernel limpo via `nbconvert --execute`.
