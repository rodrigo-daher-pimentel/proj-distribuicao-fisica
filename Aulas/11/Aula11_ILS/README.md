# Aula 11 — Iterated Local Search (ILS) para o CVRP com Frota Heterogenea

## Objetivo

Aplicar a metaheuristica Iterated Local Search (Equipe 2: double-bridge + estrita) sobre as oito solucoes pos-busca-local da Sprint 2 e quantificar o ganho operacional obtido em relacao a busca local standalone (Baseline 1) para as quatro instancias C1-C4.

## Configuracao da equipe

Conforme Sprint Planning #3 (Aula 11A, slide 8) — Equipe 2 (3VA e 3VB):

- Perturbacao: double-bridge (P3)
- Criterio de aceitacao: estrito (so aceita custo estritamente menor)
- Busca local intra-ILS: 2-opt + Relocate (fixada para toda a turma, slide 14 da Aula 11)
- Iteracoes: 100
- Seed: 42

## Resultados — pipeline completo

| Heur. | Inst. | Custo inicial | Custo BL | Custo ILS | Ganho ILS vs BL | n_rotas | fio/vuc | iter_melhor | n_melh. | Tempo ILS (s) |
|-------|-------|---------------|----------|-----------|------------------|---------|---------|-------------|---------|---------------|
| NN | C1 | 422,38 | 422,38 | 422,38 | 0,00% | 1 | 1/0 | 0 | 0 | 0,19 |
| NN | C2 | 712,49 | 710,47 | 710,47 | 0,00% | 2 | 2/0 | 0 | 0 | 1,52 |
| NN | C3 | 1.043,69 | 779,76 | **775,01** | **0,61%** | 2 | 2/0 | 5 | 3 | 3,43 |
| NN | C4 | 1.410,00 | 1.387,98 | **1.384,65** | **0,24%** | 4 | 4/0 | 91 | 4 | 8,51 |
| CW | C1 | 422,38 | 422,38 | 422,38 | 0,00% | 1 | 1/0 | 0 | 0 | 0,08 |
| CW | C2 | 712,05 | 712,05 | **710,47** | **0,22%** | 2 | 2/0 | 3 | 1 | 0,82 |
| CW | C3 | 1.047,99 | 1.047,99 | **1.046,74** | **0,12%** | 2 | 1/1 | 29 | 2 | 1,38 |
| CW | C4 | 1.410,21 | 1.410,21 | **1.403,12** | **0,50%** | 3 | 2/1 | 34 | 4 | 4,20 |

Zero violacoes de capacidade ou jornada em qualquer execucao. Ganho medio do ILS sobre o Baseline 1: 0,21% (geral).

## Trilha vencedora por instancia (ILS final)

| Inst. | ILS NN | ILS CW | Vencedor | Vantagem | Exato Aula 4 (R$) | Comparavel? |
|-------|--------|--------|----------|----------|--------------------|-------------|
| C1 | 422,38 | 422,38 | empate | 0,00% | 422,38 (1 FIO) | sim — mesmo regime; ILS atinge o otimo |
| C2 | 710,47 | 710,47 | empate | 0,00% | 754,04 (1 VUC) | nao — regimes de frota distintos |
| C3 | **775,01** | 1.046,74 | **NN** | −26,0% | 769,65 (1 VUC) | nao — solucao exata inviavel (10 h > 8 h) |
| C4 | **1.384,65** | 1.403,12 | **NN** | −1,32% | 858,31 (1 VUC) | nao — solucao exata inviavel (15 h > 8 h) |

## Nota metodologica — comparacao com o metodo exato da Aula 4

O MILP da Aula 4 e o pipeline heuristico das Sprints 2-3 resolvem problemas diferentes; os custos nao sao comparaveis como gap de otimalidade. Tres diferencas de formulacao explicam a divergencia:

1. **Frota** — o MILP trata o conjunto `K` como tipos de veiculo e impoe saida unica por tipo (no maximo uma rota Fiorino e uma rota VUC). A heuristica nao tem esse limite e pode usar varios Fiorinos.
2. **Capacidade** — o MILP usa capacidade agregada (demanda total ≤ soma das capacidades ativadas), sem garantir o limite por veiculo. A heuristica impoe capacidade por rota.
3. **Jornada** — o limite de 8 h nao entra no MILP (validado apenas em pos-processamento). A heuristica impoe 8 h por rota.

Consequencias concretas:

- **C1**: mesmo regime efetivo (1 rota, 1 Fiorino). O ILS atinge R$ 422,38, igual ao otimo exato. Comparacao valida.
- **C2**: o exato consolida tudo num unico VUC (R$ 754,04); a heuristica usa dois Fiorinos (2 × R$ 250 de fixo < R$ 550 do VUC) e chega a R$ 710,47. Nao e "superar o otimo" — e operar num espaco de frota que o MILP proibe.
- **C3 e C4**: a solucao do exato poe 40 e 60 clientes num unico VUC. So o tempo de atendimento (0,25 h/cliente) soma 10 h e 15 h, acima da jornada de 8 h. Sao solucoes operacionalmente inviaveis; nao servem como referencia de custo para o problema real.

O unico gap legitimo contra o exato e o de C1 (0%, otimo atingido). Para C2-C4, a referencia honesta de qualidade e o Baseline 1 (busca local standalone) e, quando houver, um limite inferior de um MILP que imponha capacidade por rota e jornada — nao os valores da Aula 4.

## Achado metodologico — Baseline 1 nao e idempotente sobre NN

Re-aplicar 2-opt + Relocate sobre as solucoes pos-busca-local da Aula 8 (que usaram 2-opt + Relocate + Swap) **derrubou os custos da trilha NN**: NN-C2 caiu R$ 2,02; NN-C3 caiu R$ 263,93 (−25,3%); NN-C4 caiu R$ 22,02. A trilha CW e idempotente. A razao e estrutural: o Swap aplicado por ultimo na Aula 8 reorganizou clientes entre rotas, abrindo novas oportunidades para 2-opt e Relocate que so se materializam quando os tres operadores sao re-aplicados em ordem diferente. O Baseline 1 captura esse efeito e e a referencia correta para medir o ganho do ILS.

## Rodada calibrada (regime livre) — teto de qualidade

A configuracao controlada (double-bridge + estrita, sem Swap, 100 iteracoes, seed 42) e imposta pelo slide 21 para permitir comparacao justa entre equipes, nao para otimizar. Para medir quanto essa receita deixa sobre a mesa, rodamos um ILS de regime livre (script `calibrado_c1_c4.py`): multi-restart aleatorio, busca local enriquecida (2-opt + Relocate + Or-opt + Swap + criacao de rota), reotimizacao do tipo de veiculo por rota e perturbacao mista. As restricoes do problema real sao preservadas (capacidade por rota e jornada de 8 h por rota).

| Inst. | ILS controlado (R$) | ILS calibrado (R$) | Ganho | n_restarts |
|-------|---------------------|--------------------|-------|------------|
| C1 | 422,38 | 422,38 | 0,00% | 86 |
| C2 | 710,47 | 710,47 | 0,00% | 14 |
| C3 | 775,01 | **745,52** | **+3,81%** | 15 |
| C4 | 1.384,65 | **1.369,06** | **+1,13%** | 7 |

C1 e C2 nao tem folga: o valor controlado ja e o melhor (C1 e o otimo provado; C2 e robusto em 14 restarts). C3 e C4 mostram folga real — coerente com a Tarefa 12 (C5), onde a config calibrada superou a controlada em ~11%. A licao para o relatorio: a config do slide 21 e uma boa premissa de comparacao, mas a calibracao por instancia (Swap, multi-seed, mais iteracoes) gera ganho operacional adicional nas instancias maiores.

## Recomendacao para a Prolog

- Pipeline padrao: Nearest Neighbor + busca local (2-opt + Relocate + Swap, como na Aula 8).
- Ativar ILS double-bridge + estrita quando a instancia tiver mais de 25 clientes ou quando houver janela de tempo computacional na operacao (custo: 3-9 s extras em C3-C4).
- Para instancias com ate 25 clientes (C1, C2), a busca local standalone basta: o ILS nao adiciona ganho.
- Para instancias maiores (40+ clientes), calibrar por instancia: habilitar Swap na busca local intra-ILS, rodar varias seeds e ampliar o orcamento de iteracoes (200-500). O ganho medido foi +3,81% em C3 e +1,13% em C4 sobre a config controlada — NN-C4 ainda melhorava na iter. 91 de 100.

## Estrutura de arquivos

```
Aulas/11/Aula11_ILS/
├── notebook.ipynb                          # notebook completo (experimento controlado)
├── README.md                                # este arquivo
├── calibrado_c1_c4.py                       # rodada de regime livre (teto de qualidade)
├── calibrado_c1_c4_resultado.json           # resultado da rodada calibrada
├── images/
│   ├── convergencia_ils_equipe2.png         # curvas current_cost x best_cost por instancia
│   ├── comparacao_tripla_equipe2.png        # solucao inicial vs Baseline 1 vs ILS
│   └── rotas_finais_ils_nn.png              # mapa das rotas finais (trilha vencedora)
└── files/                                   # 16 artefatos
    ├── solution_ils_equipe2_{nn,cw}_C{1..4}.json   # 8 solucoes finais ILS
    └── history_ils_equipe2_{nn,cw}_C{1..4}.csv     # 8 historicos de convergencia
```

Formato do JSON de solucao (entrada para Aula 12 — analise de sensibilidade):

```json
{
  "equipe": "Equipe 2 (Grupo 2)",
  "heuristic_initial": "NN" | "CW",
  "instance": "C1" | "C2" | "C3" | "C4",
  "perturbation_type": "double_bridge",
  "accept_criterion": "strict",
  "tolerance_pct": 0.0,
  "use_2opt": true, "use_relocate": true, "use_swap": false,
  "n_iterations": 100,
  "seed": 42,
  "solution": [{"route_id": 1, "vehicle": "FIO" | "VUC", "route": [0, ..., 0]}],
  "metrics": {...},
  "elapsed_sec": float,
  "iter_best": int,
  "n_melhorias": int
}
```

## Pendencias para a Sprint 3

- Aula 12 (Analise de Sensibilidade ILS) — usar estes 16 artefatos como entrada.
- Tarefa 12 (instancia secreta C5) — desafio aberto separado, dependente da liberacao do protocolo pelo professor.
- Comparacao com as configuracoes A1, A3, A4 (turma) na Tarefa 8 — depende dos resultados das outras equipes.
