# Fundamentacao Teorica — Sprint Review #1

## 1. Distribuicao fisica

Distribuicao fisica e o ramo da logistica que trata do planejamento, implementacao e controle do fluxo fisico de materiais e produtos acabados desde o ponto de origem ate o ponto de consumo, com o objetivo de atender as necessidades do cliente ao menor custo total. As atividades envolvidas incluem planejamento de rotas, dimensionamento de frota, gestao de estoques, armazenagem, processamento de pedidos e sequenciamento de entregas. O transporte e a atividade logistica de maior peso economico, representando cerca de 60% a dois tercos do custo logistico total das empresas — no Brasil, os custos logisticos correspondem a aproximadamente 12% do faturamento bruto, com 63,5% desse valor concentrado em transporte de longa distancia e distribuicao urbana.

**Referencia:** Ballou, R. H. **Gerenciamento da Cadeia de Suprimentos / Logistica Empresarial**. 5. ed. Porto Alegre: Bookman, 2006.

**Referencia complementar:** Novaes, A. G. **Logistica e Gerenciamento da Cadeia de Distribuicao: Estrategia, Operacao e Avaliacao**. 3. ed. rev. Rio de Janeiro: Elsevier, 2007.

## 2. Classes de problemas em logistica

Os problemas de otimizacao em logistica podem ser agrupados em tres grandes classes: (1) **problemas de localizacao**, que determinam onde instalar centros de distribuicao, fabricas ou depositos de modo a minimizar custos ou maximizar cobertura; (2) **problemas de roteirizacao e sequenciamento**, que definem as rotas dos veiculos e a ordem de atendimento dos clientes; e (3) **problemas de alocacao e dimensionamento**, que decidem como utilizar os recursos disponiveis (veiculos, equipes, capacidade de armazenagem). Essas classes frequentemente se combinam em problemas integrados, como o Location-Routing Problem (LRP). O presente projeto foca na classe de roteirizacao.

**Referencia:** Drezner, Z. (Ed.). **Facility Location: A Survey of Applications and Methods**. Springer Series in Operations Research. New York: Springer-Verlag, 1995.

**Referencia complementar:** Toth, P.; Vigo, D. **Vehicle Routing: Problems, Methods, and Applications**. MOS-SIAM Series on Optimization, v. 18, 2nd ed. Philadelphia: SIAM, 2014.

## 3. Otimizacao combinatoria

Otimizacao combinatoria e a area da matematica aplicada que busca a melhor solucao dentre um conjunto finito — mas tipicamente muito grande — de solucoes candidatas, envolvendo decisoes discretas como sequencias, agrupamentos e rotas. O espaco de solucoes cresce exponencialmente com o tamanho da instancia, tornando a enumeracao exaustiva inviavel para problemas reais. Exemplos classicos em logistica incluem roteirizacao de veiculos, escalonamento de producao e problemas de alocacao.

**Referencia:** Goldbarg, M.; Goldbarg, E.; Luna, H. **Otimizacao Combinatoria e Metaheuristicas: Algoritmos e Aplicacoes**. Rio de Janeiro: GEN/LTC, 2015.

**Referencia complementar:** Papadimitriou, C. H.; Steiglitz, K. **Combinatorial Optimization: Algorithms and Complexity**. Englewood Cliffs: Prentice-Hall, 1982.

## 4. Problemas NP-dificeis e complexidade computacional

Um problema e classificado como NP-dificil quando nao se conhece nenhum algoritmo capaz de resolve-lo em tempo polinomial para todas as instancias. Na pratica, isso significa que o tempo de resolucao cresce de forma exponencial com o tamanho do problema, inviabilizando solucoes exatas para instancias grandes. O CVRP e NP-dificil, pois contem o Problema do Caixeiro Viajante (TSP) como caso particular. Essa complexidade impoe um trade-off central: obter a solucao otima com custo computacional elevado ou aceitar uma boa solucao obtida rapidamente por heuristicas e metaheuristicas.

**Referencia:** Garey, M. R.; Johnson, D. S. **Computers and Intractability: A Guide to the Theory of NP-Completeness**. San Francisco: W. H. Freeman, 1979.

**Referencia complementar:** Lenstra, J. K.; Rinnooy Kan, A. H. G. Complexity of Vehicle Routing and Scheduling Problems. **Networks**, v. 11, n. 2, p. 221-227, 1981.

## 5. Vehicle Routing Problem (VRP)

O Vehicle Routing Problem (VRP) consiste em determinar um conjunto de rotas de custo minimo para uma frota de veiculos que deve atender um conjunto de clientes geograficamente dispersos, respeitando restricoes operacionais. Cada rota inicia e termina em um deposito central. O problema foi introduzido por Dantzig e Ramser em 1959, sob o nome "Truck Dispatching Problem", aplicado a entregas de combustivel. As principais variantes incluem:

- **CVRP** — restricao de capacidade dos veiculos
- **VRPTW** — janelas de tempo para atendimento
- **MDVRP** — multiplos depositos
- **DVRP** — demandas dinamicas / estocasticas
- **VRPB** — coleta apos entrega (backhaul)
- **VRPPD** — coleta e entrega simultaneas (pickup and delivery)
- **OVRP** — rotas abertas (veiculo nao retorna ao deposito)

**Referencia:** Toth, P.; Vigo, D. **Vehicle Routing: Problems, Methods, and Applications**. MOS-SIAM Series on Optimization, v. 18, 2nd ed. Philadelphia: SIAM, 2014.

**Referencia complementar:** Dantzig, G. B.; Ramser, J. H. The Truck Dispatching Problem. **Management Science**, v. 6, n. 1, p. 80-91, 1959.

**Referencia complementar:** Laporte, G. Fifty Years of Vehicle Routing. **Transportation Science**, v. 43, n. 4, p. 408-416, 2009.

## 6. Capacitated Vehicle Routing Problem (CVRP)

O CVRP e definido formalmente como: dado um grafo completo $G = (V, A)$ onde $V = \{0, 1, \ldots, n\}$ e o conjunto de nos (o no 0 representa o deposito e os nos $1, \ldots, n$ representam os clientes), um conjunto de custos $c_{ij}$ associados a cada arco $(i,j) \in A$, demandas conhecidas $q_i$ para cada cliente $i$, e uma frota de $K$ veiculos identicos com capacidade maxima $Q$, encontrar um conjunto de rotas de custo total minimo tal que:

1. Cada cliente e atendido exatamente uma vez por exatamente um veiculo.
2. Cada rota comeca e termina no deposito.
3. A soma das demandas dos clientes em cada rota nao excede a capacidade $Q$ do veiculo.

Uma instancia do CVRP pode ser descrita pela tupla $I = (N, D, q, K, Q, c)$, onde $N$ e o conjunto de clientes, $D$ e o deposito, $q$ e o vetor de demandas, $K$ e o numero de veiculos, $Q$ e a capacidade, e $c$ e a matriz de custos. Aplicacoes praticas incluem operadores logisticos como DHL, UPS e empresas regionais de transporte.

**Referencia:** Toth, P.; Vigo, D. **Vehicle Routing: Problems, Methods, and Applications**. MOS-SIAM Series on Optimization, v. 18, 2nd ed. Philadelphia: SIAM, 2014.

**Referencia complementar:** Laporte, G. The Vehicle Routing Problem: An Overview of Exact and Approximate Algorithms. **European Journal of Operational Research**, v. 59, n. 3, p. 345-358, 1992.

## 7. Formulacao MILP para o CVRP

Programacao Linear Inteira Mista (Mixed-Integer Linear Programming, MILP) e uma tecnica de otimizacao na qual a funcao objetivo e as restricoes sao lineares, mas algumas variaveis sao restritas a valores inteiros (ou binarios). No CVRP, a variavel de decisao principal e $x_{ijk} \in \{0, 1\}$, que vale 1 se o veiculo $k$ percorre o arco de $i$ a $j$, e 0 caso contrario.

**Funcao objetivo:**

$$\min \sum_{k=1}^{K} \sum_{i=0}^{n} \sum_{j=0}^{n} c_{ij} \cdot x_{ijk}$$

**Restricoes classicas:**

- **Visita unica:** $\displaystyle\sum_{k=1}^{K} \sum_{i=0}^{n} x_{ijk} = 1, \quad \forall\, j \in \{1, \ldots, n\}$

- **Conservacao de fluxo:** $\displaystyle\sum_{i=0}^{n} x_{ijk} = \sum_{i=0}^{n} x_{jik}, \quad \forall\, j \in V,\; \forall\, k$

- **Saida do deposito:** $\displaystyle\sum_{j=1}^{n} x_{0jk} = 1, \quad \forall\, k$

- **Capacidade:** $\displaystyle\sum_{i=0}^{n} \sum_{j=1}^{n} q_j \cdot x_{ijk} \leq Q, \quad \forall\, k$

**Referencia:** Wolsey, L. A. **Integer Programming**. New York: Wiley-Interscience, 1998.

**Referencia complementar:** Toth, P.; Vigo, D. **Vehicle Routing: Problems, Methods, and Applications**. MOS-SIAM Series on Optimization, v. 18, 2nd ed. Philadelphia: SIAM, 2014.

## 8. Subtours e eliminacao de subtours

Um subtour e um ciclo na solucao que nao passa pelo deposito, resultando em uma rota desconectada e inviavel — por exemplo, um grupo de clientes formando um circuito fechado entre si, sem conexao com o deposito. Subtours surgem porque, na ausencia de restricoes especificas, o solver encontra ciclos desconectados como parte da solucao otima da relaxacao.

A formulacao MTZ (Miller, Tucker & Zemlin, 1960) elimina subtours introduzindo variaveis auxiliares $u_i$ que representam a carga acumulada ou a ordem de visita de cada no. A restricao impoe que, se o veiculo viaja de $i$ a $j$, entao $u_j$ deve ser estritamente maior que $u_i$:

$$u_j - u_i \geq q_j - Q(1 - x_{ij}), \quad \forall\, i, j \in V \setminus \{0\},\; i \neq j$$

$$q_i \leq u_i \leq Q, \quad \forall\, i \in V \setminus \{0\}$$

Quando $x_{ij} = 1$, a restricao se torna $u_j \geq u_i + q_j$, impedindo ciclos que nao passem pelo deposito.

A abordagem alternativa sao as restricoes SEC (Subtour Elimination Constraints) de Dantzig, Fulkerson e Johnson (1954), que proibem explicitamente subconjuntos desconectados. As SEC sao mais fortes (melhor relaxacao linear), mas seu numero cresce exponencialmente, exigindo geracao dinamica (lazy constraints).

**Referencia:** Miller, C. E.; Tucker, A. W.; Zemlin, R. A. Integer Programming Formulation of Traveling Salesman Problems. **Journal of the ACM**, v. 7, n. 4, p. 326-329, 1960.

**Referencia complementar:** Dantzig, G. B.; Fulkerson, D. R.; Johnson, S. M. Solution of a Large-Scale Traveling-Salesman Problem. **Operations Research**, v. 2, n. 4, p. 393-410, 1954.

## 9. Metodos exatos: Branch and Bound e Branch and Cut

**Branch and Bound** e uma tecnica de enumeracao implicita que explora uma arvore de solucoes, dividindo o problema em subproblemas (branching) e calculando limites inferiores via relaxacao linear para podar ramos que nao podem conter a solucao otima (bounding). Quando o limite inferior de um no excede o valor da melhor solucao inteira encontrada ate o momento (incumbente), aquele ramo e descartado (pruning).

**Branch and Cut** e uma extensao do Branch and Bound que adiciona planos de corte (cutting planes) dinamicamente durante a exploracao da arvore. Os cortes sao desigualdades lineares validas para todas as solucoes inteiras viaveis, mas violadas pela solucao fracionaria corrente, apertando a relaxacao e melhorando os limites.

Conceitos associados:

- **Limite inferior (lower bound, LB):** valor da relaxacao linear, que subestima o otimo.
- **Limite superior (upper bound, UB):** valor da melhor solucao viavel inteira encontrada (incumbente).
- **Gap de otimalidade:** $\text{gap} = \frac{UB - LB}{UB} \times 100\%$. Quando gap = 0, a solucao incumbente e comprovadamente otima.

**Referencia:** Wolsey, L. A. **Integer Programming**. New York: Wiley-Interscience, 1998.

**Referencia complementar:** Nemhauser, G. L.; Wolsey, L. A. **Integer and Combinatorial Optimization**. New York: Wiley-Interscience, 1988.

## 10. Solvers MIP: Gurobi e HiGHS

Um solver MIP e um software que implementa algoritmos de Branch and Bound, Branch and Cut e tecnicas de pre-processamento para resolver problemas de Programacao Linear Inteira Mista. **Gurobi** e um solver comercial de referencia, amplamente utilizado em pesquisa e industria, com licenca academica gratuita; destaca-se pela velocidade e robustez em problemas de grande porte. **HiGHS** e um solver open-source de alta performance, desenvolvido pela Universidade de Edimburgo, sendo a alternativa de codigo aberto mais competitiva disponivel. **Pyomo** e um framework de modelagem algebrica em Python que permite formular o modelo uma unica vez e resolve-lo com diferentes solvers (Gurobi, HiGHS, CPLEX, GLPK) sem alterar o codigo. A escolha de solver importa significativamente: para problemas NP-dificeis, a diferenca de desempenho entre solvers pode chegar a ordens de magnitude.

**Referencia:** Huangfu, Q.; Hall, J. A. J. Parallelizing the Dual Revised Simplex Method. **Mathematical Programming Computation**, v. 10, n. 1, p. 119-142, 2018.

**Referencia complementar:** Hart, W. E.; Laird, C. D.; Watson, J.-P.; Woodruff, D. L.; Hackebeil, G. A.; Nicholson, B. L.; Siirola, J. D. **Pyomo — Optimization Modeling in Python**. 2nd ed. Springer Optimization and Its Applications, v. 67. Cham: Springer, 2017.

## 11. Heuristicas construtivas para VRP (contexto futuro)

Heuristicas construtivas sao metodos que constroem uma solucao viavel passo a passo, adicionando elementos a solucao parcial segundo algum criterio guloso, sem garantia de otimalidade, mas com tempo computacional rapido (tipicamente polinomial). Dois exemplos classicos para o VRP sao:

- **Nearest Neighbor (vizinho mais proximo):** a cada passo, o veiculo visita o cliente viavel mais proximo do ultimo cliente atendido.
- **Clarke & Wright Savings (1964):** parte de uma solucao trivial com uma rota dedicada para cada cliente e combina progressivamente pares de rotas cuja fusao gera a maior economia de distancia, respeitando a capacidade.

Essas heuristicas serao implementadas na Sprint 2 do projeto.

**Referencia:** Clarke, G.; Wright, J. W. Scheduling of Vehicles from a Central Depot to a Number of Delivery Points. **Operations Research**, v. 12, n. 4, p. 568-581, 1964.

**Referencia complementar:** Toth, P.; Vigo, D. **Vehicle Routing: Problems, Methods, and Applications**. MOS-SIAM Series on Optimization, v. 18, 2nd ed. Philadelphia: SIAM, 2014. (Capitulos sobre heuristicas construtivas.)

## 12. Metaheuristicas (contexto futuro)

Metaheuristicas sao estruturas algoritmicas de alto nivel que guiam heuristicas subordinadas (tipicamente buscas locais) na exploracao do espaco de solucoes, incorporando mecanismos para escapar de otimos locais. O equilibrio entre **diversificacao** (busca em novas regioes do espaco de solucoes) e **intensificacao** (refinamento em regioes promissoras) e o principio central de toda metaheuristica.

Exemplos relevantes para o projeto:

- **Simulated Annealing:** inspirado no recozimento de metais, aceita solucoes piores com probabilidade decrescente ao longo da busca.
- **Iterated Local Search (ILS):** aplica perturbacoes seguidas de busca local para gerar trajetorias no espaco de otimos locais.
- **Algoritmos Geneticos:** manteem uma populacao de solucoes, combinando-as por operadores de crossover e mutacao para gerar novas solucoes.

Essas metaheuristicas serao implementadas na Sprint 3 do projeto.

**Referencia:** Gendreau, M.; Potvin, J.-Y. (Eds.). **Handbook of Metaheuristics**. 2nd ed. International Series in Operations Research & Management Science. New York: Springer, 2010.

**Referencia complementar:** Goldbarg, M.; Goldbarg, E.; Luna, H. **Otimizacao Combinatoria e Metaheuristicas: Algoritmos e Aplicacoes**. Rio de Janeiro: GEN/LTC, 2015.

---

## Referencias Obrigatorias

1. Toth, P.; Vigo, D. **Vehicle Routing: Problems, Methods, and Applications**. MOS-SIAM Series on Optimization, v. 18, 2nd ed. Philadelphia: SIAM, 2014.

2. Goldbarg, M.; Goldbarg, E.; Luna, H. **Otimizacao Combinatoria e Metaheuristicas: Algoritmos e Aplicacoes**. Rio de Janeiro: GEN/LTC, 2015.

3. Drezner, Z. (Ed.). **Facility Location: A Survey of Applications and Methods**. Springer Series in Operations Research. New York: Springer-Verlag, 1995.

4. Project Management Institute. **A Guide to the Project Management Body of Knowledge (PMBOK Guide)**. 7th ed. PMI, 2021.

5. Dantzig, G. B.; Ramser, J. H. The Truck Dispatching Problem. **Management Science**, v. 6, n. 1, p. 80-91, 1959.

6. Miller, C. E.; Tucker, A. W.; Zemlin, R. A. Integer Programming Formulation of Traveling Salesman Problems. **Journal of the ACM**, v. 7, n. 4, p. 326-329, 1960.

7. Clarke, G.; Wright, J. W. Scheduling of Vehicles from a Central Depot to a Number of Delivery Points. **Operations Research**, v. 12, n. 4, p. 568-581, 1964.

8. Laporte, G. The Vehicle Routing Problem: An Overview of Exact and Approximate Algorithms. **European Journal of Operational Research**, v. 59, n. 3, p. 345-358, 1992.

9. Laporte, G. Fifty Years of Vehicle Routing. **Transportation Science**, v. 43, n. 4, p. 408-416, 2009.
