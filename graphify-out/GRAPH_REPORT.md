# Graph Report - .  (2026-04-15)

## Corpus Check
- 41 files · ~95,830 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 188 nodes · 240 edges · 21 communities detected
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 43 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Aula 3 — Modelagem MILP Parte 1 (frota homogenea, sem MTZ)` - 14 edges
2. `Projeto Distribuicao Fisica (ENG 4560)` - 11 edges
3. `1.5 DocumentaÃ§Ã£o e ApresentaÃ§Ãµes` - 8 edges
4. `Gurobi (solver MIP comercial)` - 7 edges
5. `Aula 4 — Modelagem MILP Parte 2 (frota heterogenea + MTZ)` - 7 edges
6. `Notebook Aula 4 — Grupo 2 (MILP Parte 2 + Experimentos)` - 7 edges
7. `Analise de Sensibilidade - Limite de Tempo` - 7 edges
8. `Rotas com MTZ + Frota Heterogenea (Visualizacao)` - 7 edges
9. `Notebook Aula 2 — Preparação de Dados (Grupo 2)` - 5 edges
10. `Projeto DistribuiÃ§Ã£o FÃ­sica (EAP)` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Projeto Distribuicao Fisica (ENG 4560)` --references--> `PUC-Rio (Departamento de Engenharia Industrial)`  [EXTRACTED]
  CLAUDE.md → Aulas/1/ENG 4560 - Aula 1 - Introdução e apresentação.md
- `Notebook Aula 4 — Grupo 2 (MILP Parte 2 + Experimentos)` --shares_data_with--> `Base de Dados Prolog (entregas reais)`  [INFERRED]
  Aulas/4/Aula4_Modelagem_MILP_Parte2/notebook.md → graphify-out/converted/Base de Dados_9e84c929.md
- `Base de Dados Prolog (entregas reais)` --shares_data_with--> `Instancias C1-C4 (10, 25, 40, 60 clientes)`  [INFERRED]
  graphify-out/converted/Base de Dados_9e84c929.md → Aulas/3/README.md
- `Projeto Distribuicao Fisica (ENG 4560)` --references--> `Cronograma do Projeto`  [EXTRACTED]
  CLAUDE.md → Cronograma_bc2cdaac.md
- `Capacitated Vehicle Routing Problem (CVRP)` --conceptually_related_to--> `Otimizacao Combinatoria`  [EXTRACTED]
  CLAUDE.md → Aulas/1/ENG 4560 - Aula 1 - Introdução e apresentação.md

## Hyperedges (group relationships)
- **Sprint 1 Deliverables** — eap_relatorio_parcial1, eap_apresentacao_sprint1, eap_modelo_exato, eap_resultados_exato [INFERRED 0.80]
- **Sprint 2 Deliverables** — eap_relatorio_consolidado, eap_apresentacao_sprint2, eap_heuristicas_construtivas, eap_busca_local, eap_relatorio_comparativo [INFERRED 0.80]
- **Sprint 3 Deliverables** — eap_relatorio_final, eap_apresentacao_sprint3, eap_apresentacao_banca, eap_metaheuristicas_eap, eap_analise_final [INFERRED 0.80]
- **EAP Level 2 Areas** — eap_gestao_projeto, eap_pesquisa_modelagem, eap_implementacao, eap_analise_resultados, eap_documentacao [EXTRACTED 1.00]
- **InstÃ¢ncia GeogrÃ¡fica do CVRP â€” DepÃ³sito e Clientes no RJ** — nb18_deposito_dc, nb18_clientes_hospitais, nb18_municipio_rj, nb18_map_rio [INFERRED 0.85]
- **VisualizaÃ§Ã£o em TrÃªs PainÃ©is do CVRP** — nb19_three_panel, nb19_rotas_reconstruidas, nb19_subtour_diag [EXTRACTED 1.00]
- **SoluÃ§Ã£o CVRP com MTZ e Frota HeterogÃªnea na InstÃ¢ncia C1_10** — nb18_mtz_form, nb18_frota_het, nb18_c1_10, nb18_mtz_route_viz [EXTRACTED 0.95]
- **Formulacao MILP do CVRP (variaveis, objetivo, restricoes)** — aula3_xij, aula3_funcao_objetivo, aula3_restricao_visita_unica, aula3_restricao_conservacao_fluxo, aula3_restricao_deposito, aula3_restricao_capacidade_agregada [EXTRACTED 1.00]
- **Pipeline Sprint 1: Dados → MILP → Solver → Resultados** — base_dados, instancias_c1_c4, aula3_mip, aula3_gurobi, aula4_mtz, aula4_resultados_com_mtz [INFERRED 0.85]
- **Tres Classes de Metodos de Solucao para CVRP** — aula1_metodos_exatos, aula1_heuristicas, aula1_metaheuristicas [EXTRACTED 1.00]

## Communities

### Community 0 - "Formulacao MILP"
Cohesion: 0.12
Nodes (21): Metodos Exatos (PLI, B&B, B&C), Branch and Bound (B&B), Branch and Cut (B&C), Fiorino (Q=650kg, f=R$250), Frota Homogenea (somente VUC), Funcao Objetivo CVRP (custo variavel + custo fixo), Programacao Linear Inteira Mista (MIP/MILP), Aula 3 — Modelagem MILP Parte 1 (frota homogenea, sem MTZ) (+13 more)

### Community 1 - "Estrutura Analitica (EAP)"
Cohesion: 0.15
Nodes (19): 1.4.3 RelatÃ³rio de AnÃ¡lise Comparativa Final, 1.4 AnÃ¡lise de Resultados, 1.3.3 CÃ³digo de Busca Local, 1.1.2 Canvas de Projeto, 1.1.3 Cronograma, 1.2.2 Documento de DescriÃ§Ã£o do Problema e Dados, 1.1.1 EAP, 1.1.4 Ã‰-NÃ£o Ã‰ / Faz-NÃ£o Faz (+11 more)

### Community 2 - "Experimentos e Resultados"
Cohesion: 0.15
Nodes (18): Gap de Otimalidade (UB-LB)/UB, Limite Inferior (Lower Bound), Rationale: Modelo sem MTZ para evidenciar importancia da eliminacao de subtours, Resultados Sem MTZ (C1-C4 com subtours), Subtours (ciclos desconectados do deposito), Limite Superior (Upper Bound / Incumbente), Experimento: Comparacao Com/Sem MTZ, Experimento: Gap vs Time Limit (30s, 60s, 300s) (+10 more)

### Community 3 - "Contexto do Projeto"
Cohesion: 0.15
Nodes (16): Distribuicao Fisica (conceito), Problemas de Alocacao/Dimensionamento, Problemas de Localizacao, Problemas de Roteirizacao/Sequenciamento, Vehicle Routing Problem (VRP), Aula 3B — EAP e Cronograma (gestao), Canvas de Projeto, E/Nao E/Faz/Nao Faz (+8 more)

### Community 4 - "Ferramentas e Dados"
Cohesion: 0.18
Nodes (15): Datasets Exportados (nodes.csv, D.npy, Cvar.npy, Tmov_h.npy, q.npy, s.npy, params.json), Fórmula de Haversine (cálculo de distâncias), Definição Formal de Instância CVRP: I = (N, D, q, K, Q, g, v, s, H), Instâncias C1-C4 (Equipe 2), Matrizes Logísticas: D_ij, c_ij, t_ij, Notebook Aula 2 — Preparação de Dados (Grupo 2), Notebook Aula 2 — Template do Professor, Aula 2 README — Preparação de Dados e Instâncias CVRP (+7 more)

### Community 5 - "Analise de Sensibilidade"
Cohesion: 0.16
Nodes (15): CVRP (Capacitated Vehicle Routing Problem), C1_10 atinge otimalidade em todos os limites de tempo, C2_25 atinge gap proximo de 0% a partir de 60s, C3_40 e C4_60 reduzem gap mas nao fecham, Instancia C1_10, Instancia C2_25, Instancia C3_40, Instancia C4_60 (+7 more)

### Community 6 - "Visualizacao de Rotas"
Cohesion: 0.2
Nodes (15): CVRP (Capacitated Vehicle Routing Problem), Clientes de Entrega, Deposito (Duque de Caxias), Deposito (Centro de Distribuicao), Frota Heterogenea, Instancia C2 (25 clientes), Modelagem MILP Parte 2, Restricoes MTZ (Miller-Tucker-Zemlin) (+7 more)

### Community 7 - "Metodos de Solucao"
Cohesion: 0.21
Nodes (13): 2-opt (busca local), Algoritmos Geneticos (GA), Clarke & Wright (heuristica construtiva), Heuristicas (conceito geral), Iterated Local Search (ILS), Metaheuristicas (SA, ILS, GA), Nearest Neighbor (heuristica construtiva), Problemas NP-dificeis (+5 more)

### Community 8 - "Curso e Referencias"
Cohesion: 0.2
Nodes (10): Aula 1 — Introducao e Apresentacao, Goldbarg et al. (2015) — Otimizacao Combinatoria e Metaheuristicas, PMBOK (2021) — Project Management, Toth & Vigo (2014) — Vehicle Routing, Metodologia SCRUM, Product Owner (P.O.), Aula 2A — Sprint Planning #1, Gerenciamento de Tarefas no Trello (+2 more)

### Community 9 - "Entregaveis e Documentacao"
Cohesion: 0.36
Nodes (8): 1.5.7 ApresentaÃ§Ã£o Final para Banca, 1.5.2 ApresentaÃ§Ã£o Sprint Review #1, 1.5.4 ApresentaÃ§Ã£o Sprint Review #2, 1.5.6 ApresentaÃ§Ã£o Sprint Review #3, 1.5 DocumentaÃ§Ã£o e ApresentaÃ§Ãµes, 1.5.3 RelatÃ³rio Consolidado G1, 1.5.5 RelatÃ³rio Final, 1.5.1 RelatÃ³rio Parcial #1

### Community 10 - "Mapa de Clientes RJ"
Cohesion: 0.67
Nodes (4): Clientes â€” Pontos de Entrega (Hospitais, ClÃ­nicas, FarmÃ¡cias), DepÃ³sito Central â€” Duque de Caxias, Mapa de LocalizaÃ§Ã£o das Entregas no Rio de Janeiro, MunicÃ­pio do Rio de Janeiro

### Community 11 - "Instancia C2 (25 clientes)"
Cohesion: 0.83
Nodes (4): Clientes (Pontos de Entrega), Coordenadas GeogrÃ¡ficas (Latitude/Longitude), DepÃ³sito (Ponto de Origem), InstÃ¢ncia C2_25 (25 clientes)

### Community 12 - "Visualizacao Folium"
Cohesion: 0.5
Nodes (4): Centro de DistribuiÃ§Ã£o (DepÃ³sito), Pontos de Entrega (Clientes), Folium Map (Biblioteca de VisualizaÃ§Ã£o), Mapa de Pontos de Entrega no Rio de Janeiro (Folium)

### Community 13 - "Instancia C4 (60 clientes)"
Cohesion: 0.67
Nodes (4): Clientes (60 pontos de entrega), DepÃ³sito (Centro de DistribuiÃ§Ã£o), InstÃ¢ncia C4_60 â€” Mapa com 60 Clientes e DepÃ³sito, RegiÃ£o GeogrÃ¡fica â€” Rio de Janeiro

### Community 14 - "Rotas de Veiculos"
Cohesion: 0.83
Nodes (4): Delivery Nodes (Hospitals/Clinics/Pharmacies) â€” Template, Depot (Duque de Caxias) â€” Template, CVRP Solution Map â€” Rio de Janeiro (Template Professor), Vehicle Routes â€” CVRP Template

### Community 15 - "Diagnostico de Subtours"
Cohesion: 0.67
Nodes (4): Rotas ReconstruÃ­das â€” VisualizaÃ§Ã£o de Rotas, DiagnÃ³stico Visual de Subtours, ViolaÃ§Ã£o de Subtour (MTZ/SEC), VisualizaÃ§Ã£o em TrÃªs PainÃ©is do CVRP (Aula 3)

### Community 16 - "MTZ e Frota Heterogenea"
Cohesion: 0.67
Nodes (4): InstÃ¢ncia C1_10 (Equipe 2), Frota HeterogÃªnea â€” VisualizaÃ§Ã£o, FormulaÃ§Ã£o MTZ â€” VisualizaÃ§Ã£o de Rotas, Rotas com MTZ + Frota HeterogÃªnea â€” C1_10 (Grupo 2)

### Community 17 - "Matriz de Distancias"
Cohesion: 0.67
Nodes (3): NÃ³s de Entrega (clientes + depÃ³sito), Matriz de DistÃ¢ncias D_s, Heatmap de Matriz SimÃ©trica

### Community 18 - "Preparacao de Dados (prof)"
Cohesion: 1.0
Nodes (3): Clientes (Pontos de Entrega) â€” Aula 2 Prep, DepÃ³sito (Centro de DistribuiÃ§Ã£o) â€” Aula 2 Prep, Mapa de NÃ³s do Problema â€” PreparaÃ§Ã£o de Dados

### Community 19 - "Preparacao de Dados (alunos)"
Cohesion: 1.0
Nodes (3): NÃ³s Clientes (Hospitais, ClÃ­nicas e FarmÃ¡cias) â€” Template, DepÃ³sito (Duque de Caxias) â€” Template, NÃ³s do Problema â€” Clientes e DepÃ³sito (Template Professor)

### Community 20 - "README Aula 3"
Cohesion: 1.0
Nodes (1): README Aula 3

## Knowledge Gaps
- **52 isolated node(s):** `Matrizes Logísticas: D_ij, c_ij, t_ij`, `Rationale: Uso de Haversine em vez de distâncias viárias reais`, `1.1.1 EAP`, `1.1.2 Canvas de Projeto`, `1.1.3 Cronograma` (+47 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `README Aula 3`** (1 nodes): `README Aula 3`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Projeto Distribuicao Fisica (ENG 4560)` connect `Contexto do Projeto` to `Formulacao MILP`, `Curso e Referencias`, `Metodos de Solucao`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Why does `Aula 3 — Modelagem MILP Parte 1 (frota homogenea, sem MTZ)` connect `Formulacao MILP` to `Experimentos e Resultados`, `Ferramentas e Dados`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `Notebook Aula 4 — Grupo 2 (MILP Parte 2 + Experimentos)` connect `Experimentos e Resultados` to `Formulacao MILP`, `Contexto do Projeto`, `Ferramentas e Dados`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Gurobi (solver MIP comercial)` (e.g. with `CBC (solver MIP open-source)` and `HiGHS (solver MIP)`) actually correct?**
  _`Gurobi (solver MIP comercial)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Matrizes Logísticas: D_ij, c_ij, t_ij`, `Rationale: Uso de Haversine em vez de distâncias viárias reais`, `1.1.1 EAP` to the rest of the system?**
  _52 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Formulacao MILP` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._