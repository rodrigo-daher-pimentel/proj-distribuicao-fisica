# Prompt: Pesquisa de Fundamentacao Teorica para Apresentacao Sprint Review #1

Voce e um agente de pesquisa. Sua tarefa e buscar na web definicoes, conceitos e referencias academicas sobre os topicos listados abaixo. O conteudo sera usado para compor a secao de fundamentacao teorica de uma apresentacao academica sobre o Capacitated Vehicle Routing Problem (CVRP).

## Instrucoes de saida

Para cada topico, produza:
- Uma definicao concisa (2-4 frases), adequada para um slide de apresentacao de graduacao em Engenharia de Producao.
- A referencia bibliografica da fonte (autor, titulo, ano, editora/journal). Priorizar fontes academicas: livros-texto, artigos de survey, capitulos de handbook.
- Se houver uma formulacao matematica classica associada, incluir.
- Idioma: portugues do Brasil. Se a fonte for em ingles, traduzir a definicao.

Salve o resultado em um unico arquivo `Aulas/5/FUNDAMENTACAO.md` com uma secao para cada topico, no formato:

```
## [Nome do topico]

[Definicao concisa]

**Referencia:** [citacao completa]

[Formulacao matematica, se aplicavel]
```

Nao adicionar comentarios, analises ou opinioes. Apenas definicoes factuais e referencias.

---

## TOPICOS A PESQUISAR

### 1. Distribuicao fisica

O que e distribuicao fisica no contexto de logistica e cadeia de suprimentos. Atividades envolvidas (planejamento de rotas, dimensionamento de frota, localizacao de estoques, sequenciamento de entregas). Relevancia do custo de transporte no custo logistico total.

Fontes sugeridas: Ballou (2006) "Gerenciamento da Cadeia de Suprimentos/Logistica Empresarial", Novaes (2007) "Logistica e Gerenciamento da Cadeia de Distribuicao".

### 2. Classes de problemas em logistica

As tres grandes classes: problemas de localizacao (onde instalar CDs), problemas de roteirizacao/sequenciamento (definir rotas e ordem de atendimento), problemas de alocacao/dimensionamento (como usar os recursos disponiveis). O projeto foca na roteirizacao.

Fontes sugeridas: Drezner (1995) "Facility Location", Toth & Vigo (2014).

### 3. Otimizacao combinatoria

Definicao: problemas com decisoes discretas (sequencias, rotas, agrupamentos). O espaco de solucoes e finito mas cresce exponencialmente com o tamanho da instancia, tornando forca bruta inviavel. Exemplos tipicos em logistica: roteirizacao, escalonamento, alocacao.

Fontes sugeridas: Goldbarg, Goldbarg & Luna (2015) "Otimizacao Combinatoria e Metaheuristicas", Papadimitriou & Steiglitz (1982).

### 4. Problemas NP-dificeis e complexidade computacional

O que significa um problema ser NP-dificil. Implicacao pratica: nao se conhecem algoritmos que resolvam em tempo polinomial. O CVRP e NP-dificil. Trade-off central: solucao otima com custo computacional alto vs. solucao boa obtida rapidamente.

Fontes sugeridas: Garey & Johnson (1979) "Computers and Intractability", Toth & Vigo (2014) capitulo 1.

### 5. Vehicle Routing Problem (VRP)

Definicao do VRP generico: determinar rotas para uma frota de veiculos que atendam um conjunto de clientes a custo minimo, respeitando restricoes operacionais. Origens historicas (Dantzig & Ramser, 1959). Principais variantes: CVRP, VRPTW, MDVRP, DVRP, VRPB, VRPPD. O diagrama de variantes e suas restricoes adicionais (capacidade, janelas de tempo, multiplos depositos, etc.).

Fontes sugeridas: Toth & Vigo (2014) "Vehicle Routing: Problems, Methods, and Applications" (2nd edition, SIAM), Laporte (2009) "Fifty Years of Vehicle Routing", Golden et al. (2008).

### 6. Capacitated Vehicle Routing Problem (CVRP)

Definicao formal do CVRP: dado um conjunto de clientes com demandas conhecidas, um deposito e uma frota de veiculos com capacidade maxima, encontrar rotas de custo minimo tal que (1) cada cliente e atendido exatamente uma vez, (2) cada rota comeca e termina no deposito, (3) a capacidade do veiculo nao e excedida em nenhuma rota. Definicao formal de instancia: I = (N, D, q, K, Q, g, v, s, H). Aplicacoes praticas: Amazon, DHL, UPS, operadores logisticos regionais.

Fontes sugeridas: Toth & Vigo (2014) capitulo sobre CVRP, Laporte (1992) "The Vehicle Routing Problem: An overview of exact and approximate algorithms".

### 7. Formulacao MILP para o CVRP

O que e Programacao Linear Inteira Mista (MILP/MIP). Variavel de decisao x_ij (binaria). Funcao objetivo: minimizar custo variavel + custo fixo. Restricoes classicas: visita unica, conservacao de fluxo, balanco no deposito, capacidade.

Fontes sugeridas: Toth & Vigo (2014), Wolsey (1998) "Integer Programming".

### 8. Subtours e eliminacao de subtours

O que e um subtour: ciclo que nao passa pelo deposito, resultando em rota inviavel. Por que surgem: na ausencia de restricoes especificas, o solver encontra ciclos desconectados como solucao otima. A formulacao MTZ (Miller, Tucker & Zemlin, 1960): variaveis auxiliares u_i que representam a ordem de visita, forcando conectividade. Formulacao: u_i - u_j + (n-1) * x_ij <= n-2. Alternativa: restricoes SEC (Subtour Elimination Constraints) de Dantzig, Fulkerson & Johnson (1954).

Fontes sugeridas: Miller, Tucker & Zemlin (1960) "Integer Programming Formulation of Traveling Salesman Problems", Dantzig, Fulkerson & Johnson (1954).

### 9. Metodos exatos: Branch and Bound e Branch and Cut

Branch and Bound: tecnica que explora uma arvore de solucoes, usando limites inferiores (relaxacao linear) para podar ramos que nao podem conter a solucao otima. Branch and Cut: extensao que adiciona cortes (planos de corte) dinamicamente durante a exploracao para apertar os limites. Conceitos associados: limite inferior (lower bound), limite superior (upper bound / incumbente), gap de otimalidade = (UB - LB) / UB.

Fontes sugeridas: Wolsey (1998), Nemhauser & Wolsey (1988) "Integer and Combinatorial Optimization".

### 10. Solvers MIP: Gurobi e HiGHS

O que e um solver MIP. Gurobi: solver comercial de referencia, amplamente usado em pesquisa e industria, com licenca academica gratuita. HiGHS: solver open-source de alta performance (Edinburgh). Pyomo: framework de modelagem em Python que permite usar ambos os solvers com o mesmo modelo. Por que a escolha de solver importa: performance pode variar ordens de magnitude para problemas NP-dificeis.

Fontes sugeridas: documentacao oficial do Gurobi, Huangfu & Hall (2018) para HiGHS, Hart et al. (2017) para Pyomo.

### 11. Heuristicas construtivas para VRP (contexto futuro)

Definicao breve: metodos que constroem uma solucao viavel passo a passo, sem garantia de otimalidade, mas com tempo computacional rapido. Exemplos classicos: Nearest Neighbor, Clarke & Wright (1964) savings algorithm. Serao implementadas na Sprint 2.

Fontes sugeridas: Clarke & Wright (1964) "Scheduling of Vehicles from a Central Depot to a Number of Delivery Points", Toth & Vigo (2014) capitulos de heuristicas.

### 12. Metaheuristicas (contexto futuro)

Definicao breve: estruturas algoritmicas de alto nivel que guiam heuristicas na exploracao do espaco de solucoes, combinando busca em novas regioes (diversificacao) com intensificacao em regioes promissoras. Exemplos: Simulated Annealing, Iterated Local Search (ILS), Algoritmos Geneticos. Serao implementadas na Sprint 3.

Fontes sugeridas: Goldbarg, Goldbarg & Luna (2015), Gendreau & Potvin (2010) "Handbook of Metaheuristics".

---

## REFERENCIAS OBRIGATORIAS A INCLUIR

As referencias abaixo foram citadas pelo professor da disciplina. Incluir na secao final do arquivo, mesmo que ja aparecam nas secoes individuais:

1. Toth, P.; Vigo, D. **Vehicle Routing: Problems, Methods, and Applications**. MOS-SIAM Series on Optimization, v. 18, 2nd edition. Philadelphia: SIAM, 2014.
2. Goldbarg, M.; Goldbarg, E.; Luna, H. **Otimizacao Combinatoria e Metaheuristicas: Algoritmos e Aplicacoes**. Rio de Janeiro: GEN/LTC, 2015.
3. Drezner, Z. **Facility Location: A Survey of Applications and Methods**. New York: Springer-Verlag, 1995.
4. Project Management Institute. **A Guide to the Project Management Body of Knowledge (PMBOK Guide)**. 7th edition. PMI, 2021.

Buscar tambem e incluir:
5. Dantzig, G.B.; Ramser, J.H. (1959) -- artigo original do VRP.
6. Miller, Tucker & Zemlin (1960) -- formulacao MTZ.
7. Clarke, G.; Wright, J.W. (1964) -- savings algorithm.
8. Laporte, G. (1992 ou 2009) -- survey de VRP.
