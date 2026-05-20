# Graph Report - .  (2026-05-20)

## Corpus Check
- 34 files · ~55,578 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 219 nodes · 256 edges · 22 communities (10 shown, 12 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Instancias C1-C4 e Solvers|Instancias C1-C4 e Solvers]]
- [[_COMMUNITY_Modelagem MILP Parte 2 (Heterogenea)|Modelagem MILP Parte 2 (Heterogenea)]]
- [[_COMMUNITY_EAP e Entregaveis do Projeto|EAP e Entregaveis do Projeto]]
- [[_COMMUNITY_Metodos de Otimizacao e Gestao SCRUM|Metodos de Otimizacao e Gestao SCRUM]]
- [[_COMMUNITY_Fundamentacao Teorica e Sprint Review 1|Fundamentacao Teorica e Sprint Review 1]]
- [[_COMMUNITY_Heuristicas Construtivas e Busca Local|Heuristicas Construtivas e Busca Local]]
- [[_COMMUNITY_Preparacao de Dados (Matrizes e Atributos)|Preparacao de Dados (Matrizes e Atributos)]]
- [[_COMMUNITY_MILP Parte 1 (Homogenea) e Sprint 1|MILP Parte 1 (Homogenea) e Sprint 1]]
- [[_COMMUNITY_Introducao a CVRP e Bibliografia Geral|Introducao a CVRP e Bibliografia Geral]]
- [[_COMMUNITY_Variantes do VRP (TSP, MDVRP, VRPTW...)|Variantes do VRP (TSP, MDVRP, VRPTW...)]]
- [[_COMMUNITY_Canvas de Projeto|Canvas de Projeto]]
- [[_COMMUNITY_Distribuicao Fisica (Conceito)|Distribuicao Fisica (Conceito)]]
- [[_COMMUNITY_EAP (Conceito de WBS)|EAP (Conceito de WBS)]]
- [[_COMMUNITY_Variavel y_k (Ativacao de Veiculo)|Variavel y_k (Ativacao de Veiculo)]]
- [[_COMMUNITY_Parametro q_i (Demanda)|Parametro q_i (Demanda)]]
- [[_COMMUNITY_Parametro Q (Capacidade do Veiculo)|Parametro Q (Capacidade do Veiculo)]]
- [[_COMMUNITY_Parametro c_ij (Custo do Arco)|Parametro c_ij (Custo do Arco)]]
- [[_COMMUNITY_Parametro f_k (Custo Fixo de Veiculo)|Parametro f_k (Custo Fixo de Veiculo)]]
- [[_COMMUNITY_Parametro H (Jornada Maxima)|Parametro H (Jornada Maxima)]]
- [[_COMMUNITY_Parametro v (Velocidade Media)|Parametro v (Velocidade Media)]]
- [[_COMMUNITY_Parametro s (Tempo de Atendimento)|Parametro s (Tempo de Atendimento)]]
- [[_COMMUNITY_Parametro g (Custo Variavel por km)|Parametro g (Custo Variavel por km)]]

## God Nodes (most connected - your core abstractions)
1. `Fundamentação Teórica — Sprint Review #1` - 22 edges
2. `Aula 3 - Modelagem MILP (Parte 1)` - 18 edges
3. `Aula 4 — Modelagem matemática do CVRP (Parte 2) [Notebook Grupo 2]` - 16 edges
4. `Aula 1 - Introducao da disciplina` - 10 edges
5. `Base de Dados (Prolog)` - 8 edges
6. `Aula 2 - Notebook Grupo 2` - 8 edges
7. `Vehicle Routing Problem (VRP)` - 8 edges
8. `Mixed-Integer Linear Programming (MILP)` - 8 edges
9. `1.5 Documentacao e Apresentacoes` - 8 edges
10. `Formulação MTZ (Miller-Tucker-Zemlin)` - 7 edges

## Surprising Connections (you probably didn't know these)
- `ENG 4560 - Aula 1 - Introdução e apresentação` --references--> `Base de dados Prolog (581 clientes, 25.324 kg, 03/06/2025)`  [INFERRED]
  Aulas/1/ENG 4560 - Aula 1 - Introdução e apresentação.pdf → Aulas/5/APRESENTACAO.md
- `Metaheurística: Simulated Annealing` --semantically_similar_to--> `Busca local: 2-opt`  [INFERRED] [semantically similar]
  Aulas/5/FUNDAMENTACAO.md → Aulas/8/ENG 4560 - Aula 8 - Heurísticas de busca local.pdf
- `Aula 4B - Canvas e E/Nao-E` --conceptually_related_to--> `EAP (Estrutura Analitica do Projeto)`  [INFERRED]
  Aulas/4/ENG 4010 - Aula 4B - Canvas e Nao.md → CLAUDE.md
- `ENG 4560 - Aula 1 - Introdução e apresentação` --references--> `Capacitated Vehicle Routing Problem (CVRP)`  [INFERRED]
  Aulas/1/ENG 4560 - Aula 1 - Introdução e apresentação.pdf → Aulas/5/FUNDAMENTACAO.md
- `ENG 4560 - Aula 4 - Modelagem matemática (Parte 2)` --implements--> `Formulação MTZ (Miller-Tucker-Zemlin)`  [EXTRACTED]
  Aulas/4/ENG 4560 - Aula 4 - Modelagem matemática (Parte 2).pdf → Aulas/5/FUNDAMENTACAO.md

## Hyperedges (group relationships)
- **Formulacao MILP do CVRP** — aula3_variavel_xij, aula3_funcao_objetivo, aula3_restricao_visita_unica, aula3_restricao_fluxo, aula3_restricao_capacidade, aula3_mtz [EXTRACTED 1.00]
- **Instancias C1-C4 Equipe 2 (aninhadas)** — aula2_instancia_c1, aula2_instancia_c2, aula2_instancia_c3, aula2_instancia_c4, base_dados_xlsx [EXTRACTED 1.00]
- **Classes de metodos de solucao por sprint** — aula1_metodos_exatos, aula1_heuristicas, aula1_metaheuristicas, claude_md_sprint1, claude_md_sprint2, claude_md_sprint3 [EXTRACTED 1.00]
- **Componentes da formulação MILP do CVRP com MTZ** — concept_cvrp, concept_milp, concept_mtz, var_x_ijk, var_u_i, constraint_capacidade [EXTRACTED 1.00]
- **Pipeline Sprint 1: modelagem exata via Pyomo + Gurobi nas instâncias C1-C4** — sprint1, concept_milp, tool_pyomo, tool_gurobi, instance_C1_10, instance_C4_60 [EXTRACTED 1.00]
- **Hierarquia de métodos para CVRP: exato → heurística construtiva → busca local → metaheurística** — concept_branch_and_cut, heuristic_clarke_wright, ls_2opt, meta_ils [EXTRACTED 1.00]

## Communities (22 total, 12 thin omitted)

### Community 0 - "Instancias C1-C4 e Solvers"
Cohesion: 0.08
Nodes (35): Veiculo Fiorino (Q=650kg, f=R$250), Instancia C1_10 (10 clientes), Instancia C2_25 (25 clientes), Instancia C3_40 (40 clientes), Instancia C4_60 (60 clientes), Instancias C1-C4 (aninhadas, seed 42), Aula 2 - README (Preparacao de Dados), Veiculo VUC (Q=3000kg, f=R$550) (+27 more)

### Community 1 - "Modelagem MILP Parte 2 (Heterogenea)"
Cohesion: 0.11
Nodes (28): Aula 4 — Modelagem matemática do CVRP (Parte 2) [Notebook Grupo 2], Aula 4 — Modelagem matemática do CVRP (Parte 2) [Template Professor], ENG 4560 - Aula 4 - Modelagem matemática (Parte 2), Aula 5 — Acompanhamento Sprint 1, Aula 5 — README, Branch and Bound, Branch and Cut, Frota heterogênea (Fiorino + VUC) (+20 more)

### Community 2 - "EAP e Entregaveis do Projeto"
Cohesion: 0.07
Nodes (27): 1.0 Projeto de Distribuicao Fisica (CVRP - Prolog), 1.1.1 EAP, 1.1.2 Canvas de Projeto, 1.1.3 Cronograma, 1.1.4 Matriz E-Nao E-Faz-Nao Faz, 1.1 Gestao de Projeto, 1.2.1 Documento de Revisao Bibliografica, 1.2.2 Documento de Descricao do Problema e Base de Dados (+19 more)

### Community 3 - "Metodos de Otimizacao e Gestao SCRUM"
Cohesion: 0.09
Nodes (25): Heuristicas, Metaheuristicas (SA, ILS, GA), Metodos Exatos (PLI, B&B, B&C), NP-Hard (complexidade), Product Owner (P.O.), Scrum Master, Aula 2A - Sprint Planning 1 e Trello, Trello (gerenciamento de tarefas) (+17 more)

### Community 4 - "Fundamentacao Teorica e Sprint Review 1"
Cohesion: 0.09
Nodes (23): Apresentação Sprint Review #1 (prompt), Fundamentação Teórica — Sprint Review #1, Pesquisa de Fundamentação Teórica (prompt), Formulação MTZ (Miller-Tucker-Zemlin), SEC — Subtour Elimination Constraints, Subtour (ciclo desconectado do depósito), Ballou, R. H. (2006) — Gerenciamento da Cadeia de Suprimentos, Dantzig, Fulkerson & Johnson (1954) — Large-Scale TSP (+15 more)

### Community 5 - "Heuristicas Construtivas e Busca Local"
Cohesion: 0.19
Nodes (16): ENG 4560 - Aula 7A - Sprint Planning 2, ENG 4560 - Aula 7B - Heurísticas construtivas, ENG 4560 - Aula 8 - Heurísticas de busca local, Problemas NP-difíceis, Otimização combinatória, Heurística construtiva: Clarke & Wright Savings, Heurística construtiva: Nearest Neighbor, Busca local: 2-opt (+8 more)

### Community 6 - "Preparacao de Dados (Matrizes e Atributos)"
Cohesion: 0.15
Nodes (14): Distancia Haversine, Matriz de custos c_ij = g * D_ij, Matriz de distancias D_ij (km), Matriz de tempos t_ij = D_ij / v, Aula 2 - Notebook Grupo 2, Aula 2 - Notebook Template (Alunos), Vetor de demanda q_i (kg), Vetor de atendimento s_i (h) (+6 more)

### Community 7 - "MILP Parte 1 (Homogenea) e Sprint 1"
Cohesion: 0.15
Nodes (13): ENG 4560 - Aula 2A - Sprint Planning 1 e Trello, ENG 4560 - Aula 3 - Modelagem matemática (Parte 1), ENG 4560 - Aula 5 - Acompanhamento Sprint 1 (PDF), Frota homogênea (somente VUC), Mixed-Integer Linear Programming (MILP), Restrição de capacidade, Restrição de conservação de fluxo, Restrição de saída do depósito (+5 more)

### Community 8 - "Introducao a CVRP e Bibliografia Geral"
Cohesion: 0.2
Nodes (12): Capacitated Vehicle Routing Problem (CVRP), Aula 1 - Introducao da disciplina, Otimizacao Combinatoria, Prof. Marcello Congro, Drezner - Facility Location 1995, Goldbarg - Otimizacao Combinatoria e Metaheuristicas 2015, PMI - PMBOK 2021, Royce 1970 - Modelo Cascata (+4 more)

### Community 9 - "Variantes do VRP (TSP, MDVRP, VRPTW...)"
Cohesion: 0.18
Nodes (11): ENG 4560 - Aula 1 - Introdução e apresentação, Capacitated Vehicle Routing Problem (CVRP), Traveling Salesman Problem (TSP), Vehicle Routing Problem (VRP), Dantzig & Ramser (1959) — The Truck Dispatching Problem, VRP variant: DVRP (demandas dinâmicas/estocásticas), VRP variant: MDVRP (múltiplos depósitos), VRP variant: OVRP (open routes) (+3 more)

## Knowledge Gaps
- **119 isolated node(s):** `Rodrigo Pimentel`, `Bernardo Caula`, `Joao Felipe Leal`, `Lucas Campos`, `Lucas Terzi` (+114 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Base de Dados (Prolog)` connect `Preparacao de Dados (Matrizes e Atributos)` to `Instancias C1-C4 e Solvers`, `Metodos de Otimizacao e Gestao SCRUM`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `Aula 4 — Modelagem matemática do CVRP (Parte 2) [Notebook Grupo 2]` connect `Modelagem MILP Parte 2 (Heterogenea)` to `Variantes do VRP (TSP, MDVRP, VRPTW...)`, `Fundamentacao Teorica e Sprint Review 1`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **What connects `Rodrigo Pimentel`, `Bernardo Caula`, `Joao Felipe Leal` to the rest of the system?**
  _119 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Instancias C1-C4 e Solvers` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Modelagem MILP Parte 2 (Heterogenea)` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._
- **Should `EAP e Entregaveis do Projeto` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._
- **Should `Metodos de Otimizacao e Gestao SCRUM` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._