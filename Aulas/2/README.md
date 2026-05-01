# Aula 2 — Preparacao de Dados e Instancias CVRP

## Base de dados

Fonte: `Base de Dados.xlsx` (Prolog Transporte e Logística).

- 1021 registros brutos de entregas (dia unico de operacao, 03/06/2025)
- 243 CEPs repetidos (multiplos pedidos para o mesmo ponto)
- Apos agregacao por CEP: **581 clientes unicos**
- Demanda total no dia: **25.324 kg**
- Campos utilizados: CEP de entrega, quantidade de volumes, peso real (kg), valor da mercadoria (R$)

## Parametros operacionais

| Parametro                   | Valor                          |
| --------------------------- | ------------------------------ |
| Deposito (CD)               | CEP 25251-560, Duque de Caxias |
| Custo variavel (g)          | R$ 1,50/km                     |
| Velocidade media (v)        | 40 km/h                        |
| Tempo de atendimento (s)    | 15 min/cliente                 |
| Jornada maxima (H)          | 8 h                            |
| Fiorino — capacidade        | 650 kg                         |
| Fiorino — custo fixo diario | R$ 250                         |
| VUC — capacidade            | 3.000 kg                       |
| VUC — custo fixo diario     | R$ 550                         |

## Instancias da Equipe 2

Geradas com seed fixa (42), segundo bloco de 60 clientes (EQUIPE_ID = 2). As instancias sao aninhadas: C1 ⊂ C2 ⊂ C3 ⊂ C4.

| Instancia | Clientes | Demanda total (kg) | Media (kg/cliente) | Min. Fiorinos | Min. VUCs |
| --------- | -------- | ------------------ | ------------------ | ------------- | --------- |
| C1_10     | 10       | 141,6              | 14,2               | 1             | 1         |
| C2_25     | 25       | 754,5              | 30,2               | 2             | 1         |
| C3_40     | 40       | 1.295,3            | 32,4               | 2             | 1         |
| C4_60     | 60       | 1.958,1            | 32,6               | 4             | 1         |

A media global da base e 43,6 kg/cliente. A Equipe 2 ficou abaixo da media (32,6 kg/cliente na C4), o que e esperado por se tratar de uma amostra aleatoria.

## Distancias

As coordenadas sao derivadas deterministicamente do CEP (mapeamento para bounding box do RJ), e as distancias calculadas por Haversine. Nao representam distancias viarias reais — sao uma aproximacao geometrica adequada para os fins didaticos do projeto.

- Distancia maxima deposito-cliente (C4): ~67 km
- Distancia media deposito-cliente (C4): ~17 km
- Coerente com a regiao metropolitana do RJ

## Insights para proximas aulas

### Para a modelagem MILP (Aula 3)

- **C1 e C2 sao instancias leves.** C1 cabe em um unico VUC (141,6 kg << 3.000 kg) e C2 tambem (754,5 kg). A restricao de capacidade so vai "apertar" de verdade com Fiorinos ou nas instancias maiores.
- **A restricao de jornada pode ser mais limitante que a de capacidade.** Com 15 min de atendimento por cliente e velocidade de 40 km/h, a jornada de 8h e consumida rapido. Na C4, so o tempo de atendimento dos 60 clientes soma 15 horas — muito acima de uma jornada. O solver vai precisar de multiplos veiculos mesmo quando a carga total caberia em poucos.
- **As matrizes sao densas (582x582 na base completa, 61x61 na C4).** Para o solver, a C4 ja pode exigir tempo computacional significativo por ser NP-Hard.

### Para heuristicas construtivas (aulas futuras)

- **A dispersao geografica e moderada** (raio de ~67 km), o que favorece heuristicas como Clarke & Wright que exploram proximidade entre clientes.
- **A demanda e heterogenea.** Alguns clientes tem menos de 1 kg, outros passam de 100 kg. Heuristicas construtivas precisam considerar isso ao montar rotas.
- **As instancias aninhadas permitem comparacao direta** de escalabilidade entre metodos exatos e heuristicos.

### Para metaheuristicas (aulas futuras)

- **O gap entre solucao exata e heuristica nas instancias menores (C1, C2)** servira como referencia para calibrar metaheuristicas.
- **Na C4, se o solver exato nao convergir em tempo razoavel**, a metaheuristica sera a unica abordagem viavel — o que reforça sua importancia no projeto.

## Arquivos gerados

```
Aulas/2/
├── Aula2_Preparacao_Dados.ipynb    # notebook completo (Aula 2)
├── README.md                        # este arquivo
└── datasets/
    ├── Equipe_2_C1_10/
    │   ├── nodes.csv                # tabela de nos (deposito + clientes)
    │   ├── D.npy                    # matriz de distancias (km)
    │   ├── Cvar.npy                 # matriz de custos (R$)
    │   ├── Tmov_h.npy               # matriz de tempos (h)
    │   ├── q.npy                    # vetor de demanda (kg)
    │   ├── s.npy                    # vetor de atendimento (h)
    │   └── params.json              # parametros do problema
    ├── Equipe_2_C2_25/
    │   └── (mesma estrutura)
    ├── Equipe_2_C3_40/
    │   └── (mesma estrutura)
    └── Equipe_2_C4_60/
        └── (mesma estrutura)
```
