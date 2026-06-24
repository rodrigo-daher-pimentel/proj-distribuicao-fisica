<!-- converted from relatorio_sprint2.docx -->

Relatório Parcial #1 — Sprint 1
Projeto Integrado VI: Distribuição Física (CVRP — Prolog Transporte e Logística)

Disciplina: ENG 4560 — Projeto Integrado VI: Distribuição Física
Professor: Marcello Congro — Departamento de Engenharia Industrial, PUC-Rio
Empresa parceira: Prolog Transporte e Logística

Grupo 2
Bernardo Caula
João Felipe Leal
Lucas Campos
Lucas Terzi
Rodrigo Pimentel

Período da Sprint 1: 12/03/2026 a 16/04/2026
Data de entrega: 18/04/2026

Rio de Janeiro — 2026

# Resumo
Este relatório apresenta os resultados da Sprint 1 do projeto de distribuição física desenvolvido em parceria com a Prolog Transporte e Logística. O problema tratado é o Capacitated Vehicle Routing Problem (CVRP), aplicado à roteirização de entregas do centro de distribuição da empresa em Duque de Caxias para hospitais, clínicas e farmácias no Rio de Janeiro. O trabalho da sprint concentrou-se em três frentes: revisão conceitual sobre VRP e métodos exatos, formulação de um modelo de Programação Linear Inteira Mista (MILP) com restrições de eliminação de subtours no estilo Miller, Tucker e Zemlin (1960), e implementação computacional em Pyomo com o solver Gurobi 13.0.1. Foram conduzidos experimentos em quatro instâncias aninhadas (C1 a C4, com 10 a 60 clientes), avaliando o impacto das restrições MTZ, a sensibilidade ao limite de tempo, o desempenho relativo de Gurobi e HiGHS, e a sensibilidade dos parâmetros de frota. Os resultados indicam otimalidade comprovada até 25 clientes em menos de 65 segundos e gap persistente de 3,56% e 4,37% para 40 e 60 clientes após 300 segundos, evidenciando os limites práticos do método exato e motivando a adoção de heurísticas e metaheurísticas nas próximas sprints.
Palavras-chave: CVRP. Programação linear inteira mista. Branch and Cut. Subtours. Gurobi.

# Lista de Figuras
Figura 1 – Dispersão geográfica dos 581 clientes únicos e do centro de distribuição
Figura 2 – Dispersão espacial da instância C4_60
Figura 3 – Diagnóstico de subtours na instância C1_10 sem MTZ
Figura 4 – Rota ótima da instância C1_10 com MTZ e frota heterogênea
Figura 5 – Comparação lado a lado COM e SEM MTZ na instância C2_25
Figura 6 – Custo incumbente e gap de otimalidade em função do limite de tempo
Figura 7 – Estrutura Analítica do Projeto

# Lista de Tabelas
Tabela 1 – Resultados do Modelo 1 (frota homogênea, sem MTZ)
Tabela 2 – Resultados do Modelo 2 (frota heterogênea, com MTZ)
Tabela 3 – Comparação entre os modelos COM e SEM restrições MTZ
Tabela 4 – Sensibilidade ao limite de tempo (Modelo 2)
Tabela 5 – Comparação entre Gurobi e HiGHS (Modelo 2)
Tabela 6 – Sensibilidade da solução aos parâmetros do VUC (C1_10)

# Lista de Quadros
Quadro 1 – Características das instâncias de teste C1 a C4
Quadro 2 – Parâmetros operacionais do problema
Quadro 3 – Viabilidade do método exato por instância
Quadro 4 – Datas dos entregáveis da Sprint 1
Quadro 5 – Aderência aos requisitos da Aula 5 (Acompanhamento Sprint 1)

# Lista de Siglas e Abreviaturas
ABNT – Associação Brasileira de Normas Técnicas
B&B – Branch and Bound
B&C – Branch and Cut
CD – Centro de Distribuição
CEP – Código de Endereçamento Postal
CVRP – Capacitated Vehicle Routing Problem
EAP – Estrutura Analítica do Projeto
FIO – Fiorino (tipo de veículo)
GA – Genetic Algorithm (Algoritmo Genético)
HiGHS – High performance software for linear optimization
ILS – Iterated Local Search
LB – Lower Bound (limite inferior)
LRP – Location-Routing Problem
MDVRP – Multi-Depot Vehicle Routing Problem
MILP – Mixed-Integer Linear Programming
MIP – Mixed-Integer Programming
MTZ – Miller, Tucker e Zemlin
NP – Non-deterministic Polynomial
OVRP – Open Vehicle Routing Problem
P.O. – Product Owner
PMI – Project Management Institute
PUC-Rio – Pontifícia Universidade Católica do Rio de Janeiro
SA – Simulated Annealing
SEC – Subtour Elimination Constraints
TSP – Traveling Salesman Problem
UB – Upper Bound (limite superior)
VRP – Vehicle Routing Problem
VRPPD – Vehicle Routing Problem with Pickup and Delivery
VRPTW – Vehicle Routing Problem with Time Windows
VUC – Veículo Urbano de Carga

# Sumário
1 Introdução	2
1.1 Contexto e motivação	3
1.2 Objetivos da Sprint 1	3
1.3 Metodologia de trabalho	3
1.4 Estrutura do relatório	3
2 Revisão da Literatura	4
2.1 Distribuição física	4
2.2 Classes de problemas em logística	4
2.3 Otimização combinatória	4
2.4 Complexidade computacional e problemas NP-difíceis	4
2.5 Vehicle Routing Problem (VRP)	5
2.6 Capacitated Vehicle Routing Problem (CVRP)	5
2.7 Formulação MILP do CVRP	5
2.8 Subtours e eliminação de subtours	6
2.9 Métodos exatos: Branch and Bound e Branch and Cut	6
2.10 Solvers MIP: Gurobi, HiGHS e Pyomo	6
2.11 Heurísticas construtivas	7
2.12 Metaheurísticas	7
2.13 Hierarquia dos métodos de solução	7
3 Descrição do Problema e Dados	8
3.1 Empresa parceira e contexto operacional	8
3.2 Base de dados bruta	8
3.3 Pré-processamento e agregação por CEP	8
3.4 Geocodificação e cálculo de distâncias	8
3.5 Geração das instâncias de teste C1 a C4	9
3.6 Parâmetros operacionais	10
4 Formulação Matemática do Modelo MILP	11
4.1 Conjuntos, parâmetros e variáveis de decisão	11
4.2 Função objetivo	11
4.3 Modelo 1: frota homogênea sem eliminação de subtours	11
4.4 Modelo 2: frota heterogênea com restrições MTZ	12
4.5 Discussão crítica da formulação	12
5 Implementação Computacional	13
5.1 Ambiente e dependências	13
5.2 Organização dos notebooks	13
5.3 Instanciação do modelo em Pyomo	13
5.4 Execução e coleta de métricas	13
6 Resultados Computacionais	14
6.1 Setup experimental	14
6.2 Modelo 1: frota homogênea sem MTZ	14
6.3 Modelo 2: frota heterogênea com MTZ	15
6.4 Experimento 1: impacto da eliminação de subtours	16
6.5 Experimento 2: sensibilidade ao limite de tempo	17
6.6 Experimento 3: comparação de solvers	18
6.7 Experimento 4: sensibilidade dos parâmetros de frota	19
6.8 Síntese dos resultados	19
6.9 Ponto de inflexão do custo fixo do VUC	19
6.10 Sensibilidade à velocidade média	20
6.11 Sensibilidade ao tempo de serviço	20
6.12 Comparação com outras equipes da turma	20
6.13 Aderência aos requisitos da Aula 5	20
7 Conclusões sobre a Viabilidade do Método Exato	21
7.1 Veredicto por instância	21
7.2 Comparação com a escala real da Prolog	21
7.3 Limitações identificadas	21
7.4 Motivação para as Sprints 2 e 3	22
8 Códigos Python12 Códigos Python	22
8.1 Organização do repositório12.1 Organização do repositório	22
8.2 Notebooks entregues12.2 Notebooks entregues	22
8.3 Reprodutibilidade12.3 Reprodutibilidade	22
9 Ferramentas de Gestão do Projeto13 Ferramentas de Gestão do Projeto	23
9.1 Metodologia SCRUM adaptada13.1 Metodologia SCRUM adaptada	23
9.2 Estrutura Analítica do Projeto13.2 Estrutura Analítica do Projeto	23
9.3 Cronograma13.3 Cronograma	24
9.4 Canvas de Projeto13.4 Canvas de Projeto	24
9.5 Matriz É / Não É – Faz / Não Faz13.5 Matriz É / Não É – Faz / Não Faz	24
9.6 Gestão via Trello13.6 Gestão via Trello	25
9.7 Papéis da equipe13.7 Papéis da equipe	25
10 Considerações Finais14 Considerações Finais	25
Referências Bibliográficas	25
Anexos	26
# 1 Introdução
# Contexto e motivação

O transporte rodoviário responde por cerca de 60% do custo logístico total das empresas brasileiras (BALLOU, 2006). Em operações de last mile, a composição entre custo variável (dependente da distância percorrida) e custo fixo (dependente da frota alocada) determina a margem obtida em cada entrega. A Prolog Transporte e Logística, parceira deste projeto, opera diariamente a partir do centro de distribuição localizado em Duque de Caxias (CEP 25251-560), atendendo hospitais, clínicas e farmácias na Região Metropolitana do Rio de Janeiro.
A base de dados fornecida pela empresa contempla 1.021 registros de entregas realizadas no dia 03/06/2025, que, após agregação por CEP, resultam em 581 pontos de entrega únicos e 25.324 kg de demanda total no dia. O planejamento atual das rotas é conduzido com apoio limitado de métodos quantitativos, o que abre espaço para ganhos expressivos com a adoção de modelos de otimização. Este projeto propõe uma abordagem quantitativa estruturada, construída em três etapas progressivas: métodos exatos, heurísticas construtivas e metaheurísticas.
Os desafios operacionais enfrentados pela Prolog refletem a complexidade do last mile em uma metrópole de geografia recortada. O Rio de Janeiro impõe congestionamento crônico, restrições de circulação em áreas centrais, barreiras físicas como maçico do Tijuca e baía de Guanabara, além de janelas restritas de recebimento em hospitais e clínicas. Soma-se a esses fatores a heterogeneidade da demanda: pedidos variam de poucos quilos a centenas de quilos por ponto, o que torna a escolha entre Fiorino (650 kg) e VUC (3.000 kg) decisão sensível ao perfil diário. A jornada legal de oito horas e o tempo médio de quinze minutos por atendimento limitam ainda mais o conjunto de rotas viáveis, fazendo com que decisões tomadas por experiência do operador convivam com risco recorrente de hora extra, atrasos contratuais e subutilização de veículos.
Do ponto de vista gerencial, o problema combina três alavancas de valor relevantes para a Prolog. A primeira é financeira: como o transporte concentra a maior parcela do custo logístico, reduções percentuais na distância total ou na frota ativada traduzem-se em ganho direto de margem em cada entrega. A segunda é comercial: roteiros bem dimensionados sustentam o cumprimento das janelas combinadas com hospitais e farmácias, fator decisivo para retenção de clientes em um mercado com baixo custo de troca de operador logístico. A terceira é organizacional: a substituição do planejamento intuitivo por uma rotina baseada em modelos cria padrão reprodutível, reduz dependência de pessoas-chave e permite simular cenários de expansão, variação de demanda e mudança de frota antes de executá-los. Essas três dimensões justificam o esforço analítico desta sprint e dirigem as decisões de modelagem detalhadas nas seções seguintes.
## Objetivos da Sprint 1

A Sprint 1 concentrou-se na etapa exata do projeto. Os objetivos acordados na Sprint Planning são a revisão conceitual sobre VRP e CVRP, a formulação matemática do modelo MILP em duas versões incrementais (frota homogênea sem MTZ e frota heterogênea com MTZ), a implementação em Python com Pyomo e Gurobi, a condução dos experimentos computacionais nas instâncias C1 a C4 e a análise crítica da viabilidade do método exato frente à escala real da operação da Prolog.
Os entregáveis previstos para o encerramento da sprint são este relatório parcial, a apresentação da Sprint Review #1, a ata da Sprint Retrospective 1 e os códigos-fonte dos notebooks utilizados. O conjunto dessas entregas mapeia-se aos itens 1.1, 1.2, 1.3.1, 1.4.1, 1.5.1 e 1.5.2 da Estrutura Analítica do Projeto apresentada na seção 9.


## Metodologia de trabalho

O grupo adota uma adaptação do SCRUM em três sprints de aproximadamente vinte dias: Sprint 1 de 12/03 a 16/04, Sprint 2 de 30/04 a 21/05 e Sprint 3 de 28/05 a 09/07 (PROJECT MANAGEMENT INSTITUTE, 2021). Cada sprint encerra-se com uma Sprint Review, na qual os entregáveis são apresentados ao professor, e uma Sprint Retrospective interna, documentada em ata individual. O papel de Product Owner é rotativo: cada integrante exerce a função em uma das três sprints, o que distribui a responsabilidade pela gestão do backlog e pelo diálogo com a empresa parceira.
O controle operacional das tarefas ocorre no Trello, com cinco listas (Product Backlog, Sprint Backlog, Em Andamento, Em Revisão e Finalizado). Cada cartão corresponde a um entregável do nível 3 da EAP, o que permite acompanhar simultaneamente o progresso técnico e o cumprimento do cronograma.
## Estrutura do relatório

O restante do documento organiza-se em dez seções. A seção 2 apresenta a revisão da literatura, percorrendo os conceitos de distribuição física, VRP, CVRP, formulação MILP, eliminação de subtours e métodos exatos. A seção 3 descreve a base de dados da Prolog e a geração das instâncias de teste. A seção 4 formaliza o modelo matemático. A seção 5 detalha a implementação em Pyomo. A seção 6 apresenta os resultados dos quatro experimentos computacionais. A seção 7 discute a viabilidade do método exato. As seções 8 e 9 tratam dos códigos Python e das ferramentas de gestão do projeto. A seção 10 traz as considerações finais, seguida pelas referências.

# 2 Revisão da Literatura
## 2.1 Distribuição física

A distribuição física é o segmento da logística responsável pelo planejamento, implementação e controle do fluxo físico de produtos acabados do ponto de origem ao ponto de consumo, ao menor custo total compatível com o nível de serviço desejado (BALLOU, 2006). Suas atividades centrais abrangem planejamento de rotas, dimensionamento e alocação de frota, gestão de estoques de distribuição, processamento de pedidos e sequenciamento de entregas (NOVAES, 2007).
O transporte é o componente de maior peso financeiro, correspondendo a cerca de 60% do custo logístico total no Brasil. Em operações urbanas de last mile, caso da Prolog, essa proporção tende a ser ainda mais elevada em função da fragmentação das entregas e da baixa consolidação de cargas. Otimizar a roteirização é, portanto, a alavanca de maior retorno para reduzir o custo da operação.
## 2.2 Classes de problemas em logística

Os problemas de otimização aplicados à logística agrupam-se em três grandes classes: localização de instalações, roteirização e sequenciamento, e alocação e dimensionamento de recursos (DREZNER, 1995; TOTH; VIGO, 2014). Os problemas de localização definem onde instalar centros de distribuição, fábricas ou hubs, buscando minimizar custos fixos e de transporte ou maximizar cobertura. Os problemas de roteirização decidem as rotas e a ordem de atendimento de clientes dispersos geograficamente. Os problemas de alocação tratam do uso dos recursos disponíveis, como capacidade de armazenagem, escala de motoristas e composição de frota.
Essas classes combinam-se em problemas integrados, como o Location-Routing Problem (LRP), que decide simultaneamente a localização dos depósitos e as rotas. Este projeto concentra-se na classe de roteirização, tomando o centro de distribuição da Prolog em Duque de Caxias como fixo.
## 2.3 Otimização combinatória

A otimização combinatória é o ramo da matemática aplicada voltado à busca da melhor solução em um conjunto discreto e finito de alternativas (GOLDBARG; GOLDBARG; LUNA, 2015). Em termos formais, um problema combinatório é definido pela tupla (S, f), em que S é o conjunto finito de soluções viáveis e f: S → ℝ é a função objetivo a ser minimizada ou maximizada (PAPADIMITRIOU; STEIGLITZ, 1982). As decisões típicas envolvem sequências, rotas, agrupamentos, seleções de subconjuntos e associações entre elementos.
A característica distintiva é o crescimento explosivo de |S| com o tamanho da entrada. No VRP, o número de sequências possíveis para n clientes é da ordem de n!, o que significa aproximadamente 3,6 milhões para n = 10, 15 quatrilhões para n = 18 e valores astronomicamente inviáveis para n superior a 20. Essa explosão combinatória inviabiliza a enumeração exaustiva e motiva o desenvolvimento de técnicas específicas: formulações compactas em programação linear, algoritmos de enumeração implícita como Branch and Bound e heurísticas que exploram a estrutura local do problema. Exemplos clássicos em logística incluem o Problema do Caixeiro Viajante, o VRP e suas variantes, o bin packing e o escalonamento de máquinas paralelas.
Esta caracterização se materializa diretamente na operação da Prolog. Para os 581 clientes únicos do dia de referência, o número de sequências possíveis ultrapassa qualquer escala computável, o que torna inviável qualquer tentativa de enumerar manualmente alternativas. Mesmo no recorte aninhado adotado nesta sprint, a instância C4 com 60 clientes já gera espaço de busca incomparável ao planejamento intuitivo praticado hoje, justificando a adoção de formulações matemáticas estruturadas como ponto de partida.
## 2.4 Complexidade computacional e problemas NP-difíceis

A teoria da complexidade computacional classifica problemas de decisão segundo o tempo necessário para sua resolução em função do tamanho da entrada (GAREY; JOHNSON, 1979). A classe P reúne os problemas resolvíveis em tempo polinomial. A classe NP contém os problemas cujas soluções candidatas podem ser verificadas em tempo polinomial, ainda que sua construção seja difícil. Um problema é NP-completo quando pertence à classe NP e é tão difícil quanto qualquer outro problema em NP. Um problema é NP-difícil quando toda instância de qualquer problema de NP pode ser reduzida a ele em tempo polinomial, sem exigência de pertencer à própria classe NP.
O Capacitated Vehicle Routing Problem é NP-difícil por redução direta do Traveling Salesman Problem. Quando todos os clientes apresentam demanda unitária e a capacidade Q é igual ou superior a n, o CVRP degenera-se em um TSP com depósito como vértice inicial e final (LENSTRA; RINNOOY KAN, 1981). Como o TSP é comprovadamente NP-difícil, o CVRP herda a mesma complexidade. A melhor cota superior conhecida para algoritmos exatos do TSP é O(n² · 2ⁿ), obtida pela programação dinâmica de Held e Karp, o que confirma a ordem exponencial.
Na prática, essa caracterização impõe um trade-off central: garantir otimalidade exige tempo que cresce exponencialmente com o número de clientes, enquanto obter soluções rapidamente implica abrir mão dessa garantia. A progressão metodológica do projeto decorre diretamente dessa limitação: métodos exatos operam em instâncias pequenas (até cerca de 25 clientes nas condições testadas), heurísticas escalam até algumas centenas de clientes e metaheurísticas avançam sobre instâncias de milhares de pontos em tempo computacional controlado.
## 2.5 Vehicle Routing Problem (VRP)

O Vehicle Routing Problem consiste em determinar um conjunto de rotas de custo mínimo para uma frota de veículos que atenda um conjunto de clientes geograficamente dispersos, respeitando restrições operacionais (TOTH; VIGO, 2014). O problema foi introduzido por Dantzig e Ramser (1959) sob o nome Truck Dispatching Problem, aplicado ao abastecimento de combustível em postos de gasolina. Desde então, surgiram diversas variantes para tratar restrições típicas de contextos reais, entre elas o CVRP (capacidade), o VRPTW (janelas de tempo), o MDVRP (múltiplos depósitos), o VRPPD (coleta e entrega) e o OVRP (rotas abertas) (LAPORTE, 2009).
A definição da variante adequada depende das restrições do problema prático. Para o caso da Prolog, a principal restrição operacional é a capacidade dos veículos, o que posiciona o CVRP como a variante pertinente. A jornada máxima de oito horas é tratada em pós-processamento e poderá ser incorporada como restrição explícita em sprints futuras.
## 2.6 Capacitated Vehicle Routing Problem (CVRP)

Dado um grafo completo G = (V, A) com V = {0, 1, ..., n}, em que o nó 0 representa o depósito e os nós 1 a n representam clientes, custos c_ij associados a cada arco e demandas q_i para cada cliente, o CVRP busca um conjunto de rotas de custo total mínimo tal que cada cliente seja atendido exatamente uma vez, cada rota inicie e termine no depósito e a soma das demandas atendidas em uma rota não ultrapasse a capacidade Q do veículo (LAPORTE, 1992; TOTH; VIGO, 2014). A instância completa do problema, considerando frota heterogênea e restrições operacionais adicionais, pode ser descrita pela tupla I = (N, D, q, K, Q, g, v, s, H), em que N é o conjunto de clientes, D o depósito, q o vetor de demandas, K o conjunto de tipos de veículo, Q o vetor de capacidades, g o custo variável em R$/km, v a velocidade média, s o tempo de atendimento por cliente e H a jornada máxima.
Aplicações práticas do CVRP incluem operações de distribuição de grandes integradores logísticos como DHL, UPS e FedEx, além de operadores regionais e empresas de last mile especializadas, caso da Prolog.
## 2.7 Formulação MILP do CVRP

A Programação Linear Inteira Mista é uma técnica de otimização em que a função objetivo e as restrições são lineares e um subconjunto das variáveis assume valores inteiros ou binários (WOLSEY, 1998). Na formulação clássica do CVRP, a variável de decisão principal é x_ijk ∈ {0, 1}, indicando se o veículo k percorre o arco (i, j). A função objetivo minimiza o custo total das rotas:
min ∑_k ∑_i ∑_j c_ij · x_ijk
As restrições clássicas são: (i) visita única — cada cliente é atendido por exatamente um veículo; (ii) conservação de fluxo — o grau de entrada iguala o grau de saída em cada nó visitado; (iii) saída do depósito — cada veículo ativado parte do nó 0; e (iv) capacidade — a soma das demandas atendidas por cada veículo não excede Q. A formulação detalhada com frota heterogênea, específica deste projeto, é apresentada na seção 4.
## 2.8 Subtours e eliminação de subtours

Um subtour é um ciclo na solução que não passa pelo depósito, resultando em uma rota desconectada da operação. Na ausência de restrições específicas, o solver encontra subtours como parte da solução ótima da relaxação, já que ciclos fechados entre clientes reduzem o custo total sem violar as restrições clássicas (TOTH; VIGO, 2014). A consequência prática é uma solução matematicamente válida, porém inexequível do ponto de vista operacional.
Duas abordagens são usuais para eliminar subtours. A formulação MTZ, proposta por Miller, Tucker e Zemlin (1960), introduz variáveis auxiliares u_i que representam a carga acumulada ou a ordem de visita em cada nó e impõe:
u_j − u_i ≥ q_j − Q(1 − x_ij),   ∀ i, j ∈ V \ {0}, i ≠ j
q_i ≤ u_i ≤ Q,   ∀ i ∈ V \ {0}
Quando x_ij = 1, a restrição força u_j ≥ u_i + q_j, impedindo ciclos desconectados. A alternativa clássica são as restrições SEC (Subtour Elimination Constraints) de Dantzig, Fulkerson e Johnson (1954), que proíbem explicitamente qualquer subconjunto fechado. As SEC produzem relaxação linear mais forte, mas seu número cresce exponencialmente, exigindo geração dinâmica via lazy constraints. Este trabalho adota a formulação MTZ, alinhada ao material de aula do professor. No contexto da Prolog, a eliminação de subtours é pré-requisito de executável: rotas operacionais precisam partir e retornar ao CD de Duque de Caxias para abastecimento e troca de carga, e ciclos fechados entre clientes simplesmente não se traduzem em itinerários reais de Fiorino ou VUC. O Experimento 1 da seção 6 quantifica o impacto direto dessa decisão de modelagem nas instâncias C1 a C4.
## 2.9 Métodos exatos: Branch and Bound e Branch and Cut

O Branch and Bound é uma técnica de enumeração implícita que percorre uma árvore de subproblemas. Em cada nó, resolve-se a relaxação linear do problema e utiliza-se o valor obtido como limite inferior. Se esse limite for pior do que a melhor solução inteira já encontrada (incumbente), o nó é podado (WOLSEY, 1998). O Branch and Cut estende o B&B com a adição dinâmica de planos de corte, desigualdades válidas para todas as soluções inteiras viáveis porém violadas pela solução fracionária atual, o que aperta a relaxação e acelera a convergência (NEMHAUSER; WOLSEY, 1988).
Três indicadores são centrais na análise de desempenho: o limite inferior LB (valor da relaxação), o limite superior UB (melhor solução inteira encontrada) e o gap de otimalidade, definido como gap = (UB − LB) / UB. Quando o gap atinge zero, a solução incumbente é comprovadamente ótima. Caso o solver atinja o limite de tempo antes disso, a solução obtida é viável, porém sem prova de otimalidade.

## 2.10 Solvers MIP: Gurobi, HiGHS e Pyomo

Um solver MIP implementa Branch and Bound, Branch and Cut e diversas técnicas de pré-processamento (eliminação de variáveis, geração de cortes, heurísticas primais) para resolver modelos de programação linear inteira mista. O Gurobi é o solver comercial de referência, com licença acadêmica gratuita oferecida pela PUC-Rio; destaca-se pela velocidade e robustez em problemas de grande porte. O HiGHS é o solver open source mais competitivo atualmente, desenvolvido pela Universidade de Edimburgo (HUANGFU; HALL, 2018).
O Pyomo é o framework de modelagem algébrica em Python adotado neste projeto (HART et al., 2017). Ele permite formular o modelo uma única vez e resolvê-lo com diferentes solvers, facilitando comparações de desempenho como a realizada no experimento 3 da seção 6. Em problemas NP-difíceis, a diferença de performance entre solvers pode alcançar ordens de magnitude, tornando a escolha do backend decisão relevante de projeto.
## 2.11 Heurísticas construtivas

Heurísticas construtivas são algoritmos que constroem uma solução viável passo a passo, adicionando elementos segundo um critério guloso, em tempo tipicamente polinomial e sem garantia de otimalidade. Para o VRP, dois métodos clássicos são relevantes. O Nearest Neighbor inicia no depósito e, a cada iteração, insere na rota o cliente viável mais próximo, encerrando a rota quando a capacidade se esgota. O algoritmo de economias, proposto por Clarke e Wright (1964), parte de uma configuração trivial com uma rota dedicada por cliente e funde progressivamente pares de rotas de maior economia de distância, respeitando as restrições de capacidade.
Essas heurísticas serão implementadas na Sprint 2 deste projeto, complementadas por buscas locais como 2-opt, relocate e exchange (TOTH; VIGO, 2014).
## 2.12 Metaheurísticas

Metaheurísticas são estruturas algorítmicas de alto nível que coordenam heurísticas subordinadas para escapar de ótimos locais. O princípio central é o equilíbrio entre diversificação (exploração de novas regiões do espaço de soluções) e intensificação (refinamento em regiões promissoras) (GENDREAU; POTVIN, 2010). Diferentemente das heurísticas construtivas, que encerram ao produzir a primeira solução viável, metaheurísticas iteram por centenas ou milhares de passos, avaliando grandes quantidades de soluções candidatas ao longo de sua execução.
O Simulated Annealing (SA) inspira-se no processo físico de recozimento de metais. A cada iteração, uma solução vizinha é gerada por uma pequena perturbação na solução corrente. Se for melhor, é aceita; se for pior, é aceita com probabilidade P = exp(−ΔE/T), em que ΔE é a piora e T é a temperatura. A temperatura decresce ao longo da execução, de modo que o algoritmo inicia aceitando muitas soluções piores (exploração ampla) e, gradualmente, passa a aceitar apenas melhorias (intensificação). O SA é historicamente uma das metaheurísticas mais estudadas para o VRP.
O Iterated Local Search (ILS) alterna entre perturbações controladas de uma solução base e a aplicação de uma busca local. Após cada perturbação, a busca local converge para um novo ótimo local, e o melhor entre os ótimos visitados é mantido como solução incumbente. O ILS é eficaz quando o espaço de soluções apresenta muitos ótimos locais de qualidade similar, característica frequente em problemas de roteirização.
Algoritmos Genéticos (GA) mantêm uma população de soluções candidatas que evolui ao longo das iterações. Operadores de seleção escolhem pais da população atual, operadores de crossover combinam pares de pais para gerar filhos, e operadores de mutação introduzem variações aleatórias. A pressão seletiva favorece indivíduos de maior qualidade, e a população converge lentamente para regiões promissoras do espaço. A força dos GAs está na capacidade de manter diversidade ao longo da busca, reduzindo o risco de convergência prematura (GOLDBARG; GOLDBARG; LUNA, 2015).
A Sprint 3 do projeto implementará essas metaheurísticas e realizará a análise comparativa final entre todas as abordagens.
## 2.13 Hierarquia dos métodos de solução

Os três grupos de métodos posicionam-se em uma hierarquia clara quanto ao trade-off entre qualidade da solução e tempo computacional. Métodos exatos, objeto da Sprint 1, garantem otimalidade, porém seu tempo de execução cresce exponencialmente e torna-se proibitivo em instâncias grandes. Heurísticas construtivas produzem uma solução viável em tempo polinomial, sem garantia de otimalidade, e serão tratadas na Sprint 2. Metaheurísticas, abordadas na Sprint 3, partem de soluções heurísticas e aplicam mecanismos de busca sofisticados para aproximar-se do ótimo em tempo controlado.
Essa progressão fundamenta o desenho metodológico do projeto: a Sprint 1 estabelece o benchmark de otimalidade comprovada em instâncias pequenas; as Sprints 2 e 3 desenvolvem métodos escaláveis cuja qualidade será avaliada em relação a esse benchmark.

# 3 Descrição do Problema e Dados
## 3.1 Empresa parceira e contexto operacional

A Prolog Transporte e Logística é uma empresa brasileira de transporte rodoviário de cargas e logística last mile, com operações B2B, B2C e B2D. A operação relevante para este projeto parte do centro de distribuição localizado em Duque de Caxias (CEP 25251-560) e direciona-se a hospitais, clínicas e farmácias distribuídos pela Região Metropolitana do Rio de Janeiro. A frota disponível para o recorte considerado é composta por dois tipos de veículos: Fiorino, com capacidade de 650 kg e custo fixo diário de R$ 250, e VUC (Veículo Urbano de Carga), com capacidade de 3.000 kg e custo fixo diário de R$ 550.
## 3.2 Base de dados bruta

A base recebida contém 1.021 registros de entregas realizadas em 03/06/2025. Cada registro carrega o CEP de destino, a quantidade de volumes, o peso real em quilogramas e o valor da mercadoria em reais. O arquivo original encontra-se na raiz do repositório como Base de Dados.xlsx e foi preservado sem modificações diretas; todas as transformações ocorrem nos notebooks de preparação.
## 3.3 Pré-processamento e agregação por CEP

A análise dos registros brutos identificou 243 CEPs com múltiplos pedidos no mesmo dia. Como o CEP delimita uma área geográfica reduzida e o veículo pode entregar todos os pedidos de uma mesma localidade em uma única parada, os registros foram agregados por CEP. Após a agregação, restaram 581 clientes únicos, totalizando 25.324 kg de demanda no dia.
A agregação é operação chave da preparação dos dados: reduz o tamanho efetivo do problema em cerca de 43% sem perder fidelidade à operação real. O pipeline está implementado no notebook Aulas/2/Aula2_Preparacao_Dados/notebook.ipynb e segue uma sequência padronizada de sete etapas, descritas a seguir.
(1) Leitura da base bruta. O arquivo Base de Dados.xlsx é lido com pandas.read_excel, mantendo as colunas originais CEP, volumes, peso real (kg) e valor (R$). Nenhuma transformação destrutiva ocorre no arquivo de origem.
(2) Limpeza de registros inviáveis. São excluídos registros com CEP ausente, CEP fora do formato brasileiro de oito dígitos e peso menor ou igual a zero. Linhas duplicadas exatas são também removidas. O critério adotado é conservador: a entrega só entra no problema se for fisicamente executável e geograficamente identificável.
(3) Padronização do CEP. Os códigos são convertidos para string de oito dígitos, preenchidos com zeros à esquerda quando necessário, e formatados no padrão XXXXX-XXX. Essa normalização garante chaves consistentes para a agregação subsequente e para a geocodificação.
(4) Agregação por CEP. Os registros são agrupados via pandas.DataFrame.groupby('CEP'), com soma de peso e volumes e contagem de pedidos. Esta é a etapa de maior impacto: reduz 1.021 registros brutos a 581 clientes únicos, fundindo 243 CEPs com múltiplos pedidos. A decisão de agregar repousa na hipótese operacional de que um mesmo ponto de entrega é servido em uma única parada do veículo, hipótese validada com a Prolog.
(5) Geocodificação determinística. Cada CEP único é convertido em coordenadas (latitude, longitude) por mapeamento direto sobre tabela auxiliar de CEPs cariocas. A escolha por geocodificação determinística, em vez de chamadas em tempo de execução a APIs externas, assegura reprodutibilidade total entre execuções e independência de conexão de rede.
(6) Construção da matriz de distâncias. Sobre os 582 pontos (581 clientes mais o depósito), calcula-se a matriz Haversine completa, n × n, em quilômetros. A matriz é persistida em pickle para uso direto pelos notebooks da Aula 3 e da Aula 4, evitando recálculos a cada execução do solver.
(7) Amostragem das instâncias C1 a C4. A amostragem aninhada com seed igual a 42 e bloco correspondente ao EQUIPE_ID 2 produz as quatro instâncias de teste descritas na seção 3.5. Cada instância é serializada como dicionário Python contendo coordenadas, demandas e parâmetros operacionais, formato consumido diretamente pelos modelos Pyomo.
Duas decisões transversais merecem registro. Primeiro, todas as operações preservam rastreabilidade: a cada etapa, o pipeline emite contagens (registros lidos, excluídos, agregados) que permitem auditar o resultado e detectar regressões. Segundo, a separação entre preparação e modelagem foi mantida estrita: o notebook da Aula 2 produz artefatos persistentes que os notebooks subsequentes apenas consomem, evitando que mudanças no modelo MILP exijam reexecução do pipeline de dados.


## 3.4 Geocodificação e cálculo de distâncias

Cada CEP é convertido em um par (latitude, longitude) por meio de geocodificação determinística baseada no próprio código postal. As distâncias entre pontos são calculadas pela fórmula de Haversine, que mede a menor distância em uma esfera entre dois pontos dados por coordenadas geográficas. A escolha privilegia simplicidade e reprodutibilidade em detrimento da precisão viária: Haversine subestima distâncias reais em malhas urbanas, especialmente em regiões com barreiras geográficas relevantes, como é o caso do Rio de Janeiro. O impacto dessa aproximação é discutido nas limitações apresentadas na seção 7.
A Figura 1 apresenta a distribuição espacial dos 581 clientes únicos e a localização do centro de distribuição da Prolog.

Figura 1 – Dispersão geográfica dos 581 clientes únicos e do centro de distribuição

Fonte: Elaboração própria a partir de dados da Prolog (03/06/2025).

Os clientes concentram-se em duas faixas densas da Região Metropolitana do Rio de Janeiro. A faixa ao sul, com latitude entre -23,05 e -23,20, cobre a maior extensão longitudinal e concentra o maior volume de entregas. Uma segunda faixa, entre -22,70 e -22,80, reúne clientes no eixo norte-nordeste da região. O centro de distribuição, marcado em vermelho, está posicionado no quadrante leste da área coberta, em coordenadas próximas a (-44,07, -23,05).
## 3.5 Geração das instâncias de teste C1 a C4

Para viabilizar o uso de métodos exatos, a base completa foi reduzida a quatro instâncias de teste aninhadas. A construção seguiu as regras do material da Aula 2: seed fixa igual a 42, bloco de 60 clientes correspondente ao EQUIPE_ID igual a 2 (segundo bloco), e amostras incrementais de 10, 25, 40 e 60 clientes. A propriedade de aninhamento C1 ⊂ C2 ⊂ C3 ⊂ C4 garante que resultados em instâncias maiores podem ser comparados diretamente com as menores. O Quadro 1 apresenta as características das instâncias.

Quadro 1 – Características das instâncias de teste C1 a C4


Fonte: Elaboração própria.

As demandas médias por cliente em C2, C3 e C4 são semelhantes (entre 30 e 33 kg), enquanto C1 apresenta média substancialmente menor (14 kg). Essa diferença tem impacto direto na composição da frota ótima: em C1 a demanda total cabe no Fiorino, enquanto em C2, C3 e C4 ela excede a capacidade do menor veículo, forçando o uso do VUC.
A Figura 2 apresenta a dispersão espacial da maior instância de teste, C4_60.

Figura 2 – Dispersão espacial da instância C4_60

Fonte: Elaboração própria.

## 3.6 Parâmetros operacionais

Os parâmetros da tupla I = (N, D, q, K, Q, g, v, s, H) foram fornecidos pelo professor e aplicam-se uniformemente a todas as instâncias de teste. O Quadro 2 apresenta os valores adotados.

Quadro 2 – Parâmetros operacionais do problema
Fonte: Elaboração própria a partir do material da Aula 4.

# 4 Formulação Matemática do Modelo MILP
## 4.1 Conjuntos, parâmetros e variáveis de decisão
O modelo opera sobre os seguintes conjuntos e parâmetros. O conjunto de nós é V = {0, 1, ..., n}, em que 0 representa o depósito e 1 a n representam os clientes. O conjunto de arcos é A = {(i, j) ∈ V × V : i ≠ j}. O conjunto de tipos de veículo é K = {FIO, VUC}. Os parâmetros são c_ij (custo variável do arco), q_i (demanda do cliente i), Q_k (capacidade do veículo tipo k), f_k (custo fixo diário do veículo tipo k) e M (constante suficientemente grande para a formulação MTZ, tomada como Q_k da maior capacidade).
Três grupos de variáveis de decisão compõem o modelo. A variável binária x_ijk vale 1 se o arco (i, j) é percorrido por um veículo do tipo k. A variável contínua u_i representa a carga acumulada ao chegar no nó i e é o mecanismo da formulação MTZ. A variável binária y_k vale 1 se o tipo de veículo k é ativado na solução.
## 4.2 Função objetivo
A função objetivo minimiza o custo total, composto pela soma dos custos variáveis e dos custos fixos dos veículos ativados:
min Z = ∑_(k ∈ K) ∑_((i,j) ∈ A) c_ij · x_ijk + ∑_(k ∈ K) f_k · y_k
O primeiro termo captura o custo proporcional à distância percorrida e traduz diretamente o custo variável g em R$/km. O segundo termo introduz o custo fixo diário de cada tipo de veículo ativado, penalizando soluções que superdimensionam a frota.

## 4.3 Modelo 1: frota homogênea sem eliminação de subtours

A primeira versão do modelo, desenvolvida na Aula 3, considera apenas um tipo de veículo (frota homogênea) e omite as restrições de eliminação de subtours. Seu propósito é pedagógico: explicitar o efeito dos subtours antes de corrigi-lo na versão completa. As restrições são:
(i) Visita única: cada cliente j ∈ V \ {0} recebe exatamente um arco de entrada e um arco de saída.
∑_(i ∈ V, i ≠ j) x_ij = 1,   ∀ j ∈ V \ {0}
∑_(j ∈ V, j ≠ i) x_ij = 1,   ∀ i ∈ V \ {0}
(ii) Conservação de fluxo: em cada nó visitado, a soma dos arcos de entrada iguala a soma dos arcos de saída.
(iii) Balanço no depósito: o número de saídas do depósito iguala o número de retornos e corresponde ao número m de veículos utilizados.
(iv) Capacidade agregada: a demanda total atendida não ultrapassa m vezes a capacidade Q do veículo.
∑_(i ∈ V \ {0}) q_i ≤ Q · m
Na ausência da restrição (v) apresentada adiante, soluções formadas por ciclos desconectados do depósito tornam-se válidas para o solver, como se detalha na análise do experimento 1 na seção 6.
## 4.4 Modelo 2: frota heterogênea com restrições MTZ

O modelo completo, desenvolvido na Aula 4, incorpora dois elementos em relação ao Modelo 1. Primeiro, distingue os tipos de veículo (Fiorino e VUC), o que torna x_ijk dependente de k e acrescenta a variável y_k para ativação. Segundo, inclui as restrições MTZ, que eliminam subtours e forçam todas as rotas a passarem pelo depósito. As restrições adicionais são:
(v) Eliminação de subtours (MTZ):
u_j − u_i ≥ q_j − Q · (1 − x_ij),   ∀ i, j ∈ V \ {0}, i ≠ j
q_i ≤ u_i ≤ Q,   ∀ i ∈ V \ {0}
(vi) Capacidade por tipo de veículo:
∑_((i,j) ∈ A) q_j · x_ijk ≤ Q_k · y_k,   ∀ k ∈ K
(vii) Ativação de veículo: se x_0jk = 1 para algum j, então y_k = 1. Na prática, a relação é imposta por uma restrição big-M que garante consistência entre o uso dos arcos e a ativação do tipo correspondente.
(viii) Conservação de fluxo por tipo de veículo: em cada nó e para cada k, o grau de entrada iguala o grau de saída.
A jornada máxima H de 8 horas não é imposta como restrição linear no MILP, pois exigiria a inclusão de variáveis contínuas adicionais de tempo acumulado e aumentaria substancialmente a complexidade do modelo. Em vez disso, o cumprimento de H é verificado em pós-processamento, somando o tempo de deslocamento (função de v) e o tempo de atendimento (s) de cada rota e comparando com o limite.
## 4.5 Discussão crítica da formulação

A formulação MTZ foi escolhida por três razões. Primeiro, é compacta: acrescenta um número polinomial de restrições (da ordem de n²) e n − 1 variáveis contínuas, o que a torna implementável sem técnicas avançadas como lazy constraints. Segundo, alinha-se ao material do professor, assegurando paridade pedagógica com os exemplos de aula. Terceiro, produz interpretação operacional direta para u_i como carga acumulada, o que facilita a validação das soluções.
A principal limitação é a relaxação linear mais fraca em comparação às restrições SEC de Dantzig, Fulkerson e Johnson (1954). A relaxação linear de um modelo MILP consiste em substituir as restrições de integralidade x_ijk ∈ {0, 1} pela forma contínua 0 ≤ x_ijk ≤ 1, gerando um problema linear que fornece o limite inferior do ótimo inteiro. Relaxações mais fortes produzem limites mais próximos do ótimo inteiro, reduzindo o tamanho da árvore do Branch and Cut e acelerando a convergência.
Na formulação MTZ, a relaxação linear permite soluções fracionárias das variáveis u_i que não correspondem a rotas válidas, gerando um gap inicial significativo. Já as restrições SEC, por proibirem explicitamente todo subconjunto fechado, produzem uma relaxação mais apertada e, na prática, reduzem o número de nós explorados na árvore de busca. O preço dessa vantagem é que o número de SEC cresce exponencialmente com n (são 2ⁿ − 1 subconjuntos possíveis), o que exige implementação via lazy constraints: o solver começa apenas com uma formação básica e gera as SEC dinamicamente sempre que uma solução inteira corrente contém um subtour.
O efeito prático da opção pelo MTZ é evidenciado no experimento 1 da seção 6: o número de restrições cresce de 49 (Modelo 1, C1) para 3.789 (Modelo 2, C4), e o tempo de resolução sobe de décimos de segundo para 300 segundos. Em instâncias com 60 ou mais clientes, a relaxação fraca combinada com o crescimento quadrático do número de restrições inviabiliza a obtenção de otimalidade no tempo disponível. Para o recorte desta sprint, contudo, a formulação MTZ oferece equilíbrio adequado entre simplicidade de implementação e qualidade das soluções obtidas, alinhando-se ao material didático da disciplina e facilitando o paralelo pedagógico entre os dois modelos testados.

# 5 Implementação Computacional
## 5.1 Ambiente e dependências

A implementação utiliza Python como linguagem principal, Pyomo como framework de modelagem algébrica e Gurobi 13.0.1 como solver padrão (HART et al., 2017). A licença acadêmica do Gurobi é disponibilizada pela PUC-Rio aos alunos da disciplina. O HiGHS foi empregado apenas no experimento 3, como comparativo open source. As bibliotecas auxiliares incluem numpy e pandas para manipulação de dados, matplotlib para visualização, folium para mapas interativos e geopy para geocodificação.
## 5.2 Organização dos notebooks

O código encontra-se organizado por aula, conforme estrutura entregue pelo professor. O notebook Aulas/2/Aula2_Preparacao_Dados/notebook.ipynb trata a base bruta, realiza a agregação por CEP e gera as quatro instâncias de teste. O notebook Aulas/3/Aula3_Modelagem_MILP/notebook.ipynb implementa o Modelo 1 (frota homogênea sem MTZ) e produz o diagnóstico de subtours. O notebook Aulas/4/Aula4_Modelagem_MILP_Parte2/notebook.ipynb reúne o Modelo 2 e todos os experimentos computacionais da Sprint 1.
## 5.3 Instanciação do modelo em Pyomo

O modelo é declarado como um pyomo.environ.ConcreteModel. Os conjuntos V, A e K são definidos a partir dos dados da instância. Os parâmetros c_ij, q_i, Q_k e f_k são carregados como Param indexados. As variáveis x_ijk, u_i e y_k são declaradas como Var binárias ou contínuas, conforme o caso. A função objetivo e cada família de restrição são escritas como funções Python e anexadas ao modelo via Objective e Constraint. A resolução é acionada por SolverFactory('gurobi').solve(model, tee=True, timelimit=300).
A escolha do Pyomo como camada de modelagem permite alternar entre Gurobi e HiGHS pela troca de uma única linha de código, o que foi explorado no experimento 3. O mesmo modelo abstrato pode, em sprints futuras, ser resolvido por qualquer solver compatível com a interface AMPL/NL.
## 5.4 Execução e coleta de métricas

Cada execução do solver produz um conjunto padronizado de métricas: custo total em reais (valor da função objetivo), número de veículos ativados por tipo, número de subtours detectados no pós-processamento, tempo de resolução em segundos, gap de otimalidade percentual e status final do solver (optimal, maxTimeLimit, infeasible). Essas métricas são armazenadas em DataFrames pandas e consolidadas em tabelas resumo usadas na seção 6.
A detecção de subtours, essencial para a análise do Modelo 1, é feita por uma busca em grafo sobre os arcos com x_ij = 1: o algoritmo inicia no depósito, percorre a componente conexa do ponto 0 e verifica se algum cliente ficou fora dessa componente. Os clientes não alcançáveis pertencem a subtours, contados e visualizados como descrito na Figura 3.

# 6 Resultados Computacionais
## 6.1 Setup experimental

Todas as execuções desta seção utilizaram o mesmo ambiente computacional. O solver padrão foi o Gurobi 13.0.1 com limite de tempo de 300 segundos, exceto nos experimentos que variaram esse parâmetro. O cálculo de distâncias seguiu a fórmula de Haversine, e a seed de geração das instâncias foi fixada em 42 para reprodutibilidade. Os experimentos obrigatórios definidos na Aula 5 foram executados integralmente; além desses, o grupo implementou três experimentos opcionais, cobrindo sensibilidade temporal, comparação de solvers e sensibilidade de parâmetros de frota.
## 6.2 Modelo 1: frota homogênea sem MTZ

A Tabela 1 apresenta os resultados do Modelo 1 nas quatro instâncias. Em todas, o solver declara status "optimal" e encontra a solução em menos de um segundo. Porém, o número de subtours detectados no pós-processamento cresce monotonicamente com o tamanho da instância.

Tabela 1 – Resultados do Modelo 1 (frota homogênea, sem MTZ)



Fonte: Elaboração própria.

A Figura 3 mostra o diagnóstico visual dos subtours gerados pelo Modelo 1 na instância C1_10.


Figura 3 – Diagnóstico de subtours na instância C1_10 sem MTZ

Fonte: Elaboração própria.

O painel esquerdo apresenta os nós do problema sem qualquer ligação. O painel central reconstrói as rotas produzidas pelo solver: uma rota curta sai do depósito e conecta dois ou três clientes próximos, enquanto os demais formam ciclos fechados sem passar pelo depósito. O painel direito destaca em vermelho os quatro subtours detectados. Do ponto de vista do solver, a solução é "ótima" porque respeita todas as restrições declaradas e minimiza a soma dos custos dos arcos selecionados. Do ponto de vista operacional, é inexequível: nenhum veículo real conseguiria executar ciclos desconectados do depósito sem voltar para se abastecer.
Esse resultado é a evidência empírica mais direta da necessidade das restrições MTZ, motivando a evolução para o Modelo 2.
## 6.3 Modelo 2: frota heterogênea com MTZ

Os resultados do Modelo 2 estão consolidados na Tabela 2. O solver comprova otimalidade em C1 e C2 e atinge o limite de tempo em C3 e C4, encerrando com gap de otimalidade aberto.

Tabela 2 – Resultados do Modelo 2 (frota heterogênea, com MTZ)




Fonte: Elaboração própria.

A seleção da frota segue o perfil de demanda esperado. Em C1, com demanda total de 141,6 kg, o Fiorino é escolhido por ter custo fixo menor (R$ 250 contra R$ 550 do VUC). Nas demais instâncias, a demanda ultrapassa a capacidade do Fiorino, o que força o uso do VUC.
A Figura 4 mostra a rota ótima obtida para C1_10 no Modelo 2.

Figura 4 – Rota ótima da instância C1_10 com MTZ e frota heterogênea

Fonte: Elaboração própria.

A rota é única, conectada e operacionalmente viável: sai do depósito, atende os dez clientes em sequência e retorna ao ponto de partida. O custo de R$ 422,38 reflete o custo fixo do Fiorino (R$ 250) somado ao custo variável da distância total percorrida, aproximadamente 115 km. A comparação direta com a Figura 3, que mostra a mesma instância sem MTZ, evidencia o contraste entre o que o solver entrega com e sem restrições de conectividade.
## 6.4 Experimento 1: impacto da eliminação de subtours

O primeiro experimento mede o impacto quantitativo das restrições MTZ, comparando, para as quatro instâncias, os custos, o número de restrições e o tempo de resolução dos dois modelos. A Tabela 3 reúne os valores.

Tabela 3 – Comparação entre os modelos COM e SEM restrições MTZ



Fonte: Elaboração própria.

Três leituras emergem dos dados. Primeiro, o número de restrições cresce aproximadamente com o quadrado de n, passando de 49 restrições em C1 sem MTZ para 3.789 em C4 com MTZ, confirmando a ordem O(n²) inerente à formulação. Segundo, o tempo de resolução explode: em C4, salta de décimos de segundo (sem MTZ) para o teto de 300 segundos (com MTZ). Terceiro, e mais importante, o custo inferior do modelo sem MTZ é ilusório, porque as rotas produzidas incluem subtours e não podem ser executadas na operação real.
A Figura 5 consolida visualmente o contraste entre as duas formulações na instância C2_25.

Figura 5 – Comparação lado a lado COM e SEM MTZ na instância C2_25

Fonte: Elaboração própria.

O painel esquerdo, COM MTZ, exibe uma rota única que percorre todos os 25 clientes e retorna ao depósito. O painel direito, SEM MTZ, mostra o depósito praticamente isolado: a maioria dos pontos figura em losangos alaranjados, representando os onze ciclos desconectados. O custo declarado para a solução sem MTZ (R$ 666,15) é R$ 88 inferior à solução correta, mas essa diferença não tem correspondente operacional: nenhum caminhão da frota Prolog executaria a rota fragmentada entregue pelo solver.
## 6.5 Experimento 2: sensibilidade ao limite de tempo

O segundo experimento explora como o gap de otimalidade e o custo da solução incumbente evoluem à medida que o limite de tempo cresce. Foram testados três tetos: 30 s, 60 s e 300 s. A Tabela 4 apresenta os resultados.

Tabela 4 – Sensibilidade ao limite de tempo (Modelo 2)



Fonte: Elaboração própria.

C1 e C2 convergem para a solução ótima nos limites de tempo testados. O caso de C2 é instrutivo: a solução incumbente não muda entre 30 s e 300 s, mas o gap cai de 0,45% para 0%, revelando a diferença entre encontrar uma boa solução e provar que ela é ótima. Em C3 e C4, tanto o custo quanto o gap melhoram com mais tempo, porém com retornos decrescentes e sem atingir otimalidade. Mesmo após 300 s, C3 mantém gap de 3,56% e C4 de 4,37%, indicando que a convergência para o ótimo seria lenta e, provavelmente, inviável em escalas de tempo aceitáveis para a operação real.
A Figura 6 ilustra graficamente o comportamento do custo incumbente e do gap em função do limite de tempo.

Figura 6 – Custo incumbente e gap de otimalidade em função do limite de tempo

Fonte: Elaboração própria.

As curvas de C3 e C4 no gráfico de gap cruzam-se entre 60 s e 300 s, com C4 apresentando gap maior que C3 ao final. Esse cruzamento reforça que o tempo computacional não cresce linearmente com a dificuldade da instância, comportamento característico de problemas NP-difíceis.
## 6.6 Experimento 3: comparação de solvers

O terceiro experimento compara o desempenho de Gurobi e HiGHS nas duas menores instâncias. Instâncias maiores não foram testadas porque o tempo esperado do HiGHS seria proibitivo. A Tabela 5 apresenta os resultados.

Tabela 5 – Comparação entre Gurobi e HiGHS (Modelo 2)




Fonte: Elaboração própria.

Em C1_10, ambos os solvers chegam à mesma solução, mas o Gurobi é cerca de onze vezes mais rápido. Em C2_25, a diferença se aprofunda: o Gurobi comprova otimalidade em 77 s, enquanto o HiGHS atinge o teto de 300 s com gap de 6,07% e solução R$ 6,14 mais cara. Em problemas NP-difíceis, essas diferenças tendem a se ampliar com o tamanho da instância, reforçando o Gurobi como opção padrão para o benchmark exato do projeto.
## 6.7 Experimento 4: sensibilidade dos parâmetros de frota

O quarto experimento avalia a sensibilidade da solução a variações nos parâmetros do VUC, aplicadas sobre a instância C1_10. A Tabela 6 apresenta os casos testados.

Tabela 6 – Sensibilidade da solução aos parâmetros do VUC (C1_10)



Fonte: Elaboração própria.

O resultado é degenerado para esta instância: nenhuma variação altera a solução ótima. A razão é estrutural — a demanda total de 141,6 kg já cabe no Fiorino, cujo custo fixo é menor que o do VUC mesmo na configuração base. Tornar o VUC mais caro ou menos capacitado não tem efeito porque o VUC já não é selecionado. Análises desse tipo tornam-se informativas em C2 a C4, onde o VUC é efetivamente usado; esse desdobramento está previsto para sprints posteriores, junto às heurísticas, que permitirão cenários com frota composta.
## 6.8 Síntese dos resultados

Quatro conclusões consolidam a evidência dos experimentos. A restrição MTZ é indispensável: sem ela, o solver produz soluções de custo aparente menor, porém com subtours que inviabilizam a execução. O Gurobi apresenta desempenho superior ao HiGHS em ordens de magnitude nas instâncias testadas, justificando sua adoção como solver padrão. O tempo de resolução cresce rapidamente com o número de clientes e o gap não fecha em 300 s para instâncias de 40 e 60 clientes. A seleção da frota ótima é determinada principalmente pela demanda total, que fixa o tipo mínimo de veículo necessário.
## 6.9 Ponto de inflexão do custo fixo do VUC

O Experimento 4, conduzido sobre C1_10, mostrou que nenhuma variação de parâmetros do VUC altera a solução ótima, pois o Fiorino sempre comporta a demanda. Para responder à pergunta colocada na Aula 5 — em qual ponto o modelo deixa de usar o VUC? — é necessário analisar uma instância em que o VUC é efetivamente utilizado.
A análise analítica para C2_25 elucida o raciocínio. A demanda total de 754,5 kg ultrapassa a capacidade do Fiorino (650 kg), de modo que a alternativa sem VUC exige dois Fiorinos, com custo fixo combinado de 2 × R$ 250 = R$ 500. A solução ótima atual com um VUC custa R$ 754,04, dos quais R$ 550 são custo fixo do VUC e R$ 204,04 correspondem ao custo variável da rota única. A solução alternativa com dois Fiorinos incorreria em custo variável maior, uma vez que duas rotas partindo do depósito tendem a percorrer mais quilômetros que uma única rota otimizada. O ponto de inflexão ocorre quando o custo fixo do VUC excede R$ 500 somado à diferença de custo variável entre as duas configurações.
A formalização numérica do ponto de inflexão decorre da comparação entre as duas configurações competitivas em C2_25. Seja f_VUC o custo fixo do VUC, C_var^VUC = R$ 204,04 o custo variável da rota única observada na solução ótima e C_var^2FIO o custo variável da configuração alternativa com dois Fiorinos. A condição de indiferença entre as duas opções é f_VUC + C_var^VUC = 2 × R$ 250 + C_var^2FIO, o que produz f_VUC^* = R$ 500 + (C_var^2FIO − R$ 204,04). Execuções preliminares com particionamento forçado em dois Fiorinos indicam C_var^2FIO em torno de R$ 245, o que situa o ponto de indiferença entre R$ 540 e R$ 545. Para f_VUC abaixo desse intervalo, a configuração com um VUC permanece ótima; acima, o modelo passa a ativar dois Fiorinos. Como o valor de catálogo praticado pela Prolog (R$ 550) está próximo do limite superior do intervalo, pequenas oscilações no custo diário do VUC bastam para inverter a decisão ótima de frota em C2_25.
A leitura gerencial direta é que C2_25 opera em um regime de fronteira: a vantagem econômica do VUC sobre dois Fiorinos é pequena e sensível tanto a variações no custo fixo quanto à geometria da rota. Em operações em que o custo do VUC sofre pressão (combustível, manutenção, salário do motorista), a Prolog poderia se beneficiar de um plano que articula dois Fiorinos por dia em rotas paralelas, com ganho adicional em flexibilidade operacional. A grade completa de f_VUC entre R$ 250 e R$ 1.500 será resolvida no notebook da Aula 4 na próxima iteração, complementando esta derivação analítica com curvas de custo total e composição de frota por valor de parâmetro.
Uma limitação conceitual da formulação atual precisa ser registrada nesta discussão. A variável y_k é indexada apenas pelo tipo de veículo (FIO ou VUC) e não pelo índice individual da unidade. Isso significa que o modelo decide, para cada tipo, se este será usado ou não, mas não quantos veículos de cada tipo serão ativados. A capacidade efetiva de cada tipo na restrição (vi) acaba implicitamente limitada pelo número de rotas que partem do depósito naquele tipo, o que pode subdimensionar configurações como “dois Fiorinos em paralelo” e induzir a seleção de um VUC quando, na prática, dois Fiorinos seriam viáveis e mais baratos. A correção passa por reindexar y_(k,v) por unidade v de cada tipo k ou substituir y_k por uma variável inteira n_k que contabiliza quantas unidades do tipo k são ativadas, com ajustes nas restrições de capacidade e nos termos de custo fixo. Essa adaptação será incorporada nas próximas sprints, junto às heurísticas que naturalmente operam sobre frotas de múltiplas unidades.
## 6.10 Sensibilidade à velocidade média

A velocidade média v não integra diretamente a função objetivo, que depende apenas das distâncias percorridas e dos custos fixos dos veículos ativados. O parâmetro influencia exclusivamente a validação pós-otimização da jornada máxima H. Reduzir v simula condições de trânsito pesado em ambiente urbano e eleva o tempo total da rota; aumentá-lo simula trechos de rodovia em fluxo livre. Como o modelo MILP é indiferente a v, a análise de sensibilidade nesse parâmetro não altera custo nem composição da frota, mas pode tornar uma rota inicialmente viável em inexequível dentro da jornada de oito horas.
Para a instância C2_25, considerando uma distância total tipicamente abaixo de 150 km, o tempo de deslocamento em v = 40 km/h situa-se em torno de 3,75 h, somado aos 6,25 h de tempo de atendimento (25 clientes × 15 min), resultando em jornada total próxima ou superior a 10 h. Esse comportamento indica que, em variações com v = 25 km/h (trânsito pesado), a rota única deixa de ser executável em um dia de trabalho, demandando o particionamento em duas rotas ou a extensão da jornada em regime de hora extra. A incorporação de H como restrição linear no modelo é recomendação técnica para as próximas sprints.
## 6.11 Sensibilidade ao tempo de serviço

O tempo de atendimento por cliente s também não aparece na função objetivo e afeta somente a validação de H. Cenários como atendimentos em hospitais congestionados ou pontos com longa espera podem ser modelados por aumento de s de 15 minutos para valores entre 20 e 30 minutos. Em uma rota com n_r clientes, o tempo adicional de atendimento escala linearmente por n_r × (s_novo − s_base).
Em C2_25, com 25 clientes, um acréscimo de s para 25 minutos adiciona 25 × 10 = 250 minutos, ou cerca de 4,2 horas, ao tempo total da rota. Essa quantidade agravaria o quadro já limite discutido em 6.10, reforçando a recomendação de particionar rotas grandes e de transformar H em restrição explícita do modelo. O tratamento quantitativo desse cenário será conduzido nas sprints seguintes, aproveitando a maior flexibilidade das heurísticas para explorar configurações com múltiplas rotas por dia.
## 6.12 Comparação com outras equipes da turma

A comparação entre os resultados do Grupo 2 e os dos demais grupos está agendada para ocorrer durante a Sprint Review #1, em 16/04/2026. Como cada equipe utiliza um bloco distinto de clientes da base real (definido pelo parâmetro EQUIPE_ID), os custos absolutos não são comparados em termos estritos. As métricas apropriadas para o cotejo cruzado são o tempo de resolução, o gap de otimalidade ao final dos 300 segundos, a composição da frota escolhida e a evolução do gap com time limits menores. As observações colhidas na sessão de comparação serão registradas na ata da Sprint Retrospective 1.
## 6.13 Aderência aos requisitos da Aula 5

O Quadro 5 consolida o mapeamento entre cada item previsto na Aula 5 de Acompanhamento Sprint 1 e a seção deste relatório que o endereça.

Quadro 5 – Aderência aos requisitos da Aula 5 (Acompanhamento Sprint 1)


Fonte: Elaboração própria.


# 7 Conclusões sobre a Viabilidade do Método Exato
## 7.1 Veredicto por instância

A partir dos experimentos da seção 6, o Quadro 3 consolida o veredicto de viabilidade do método exato para cada instância de teste.

Quadro 3 – Viabilidade do método exato por instância


Fonte: Elaboração própria.

O método exato, implementado com MTZ e resolvido por Gurobi, entrega otimalidade comprovada em instâncias de até 25 clientes em tempos aceitáveis. A partir de 40 clientes, as soluções obtidas são boas em qualidade absoluta, mas não trazem garantia formal de otimalidade dentro do limite de tempo imposto.
## 7.2 Comparação com a escala real da Prolog

A operação real da Prolog, para o dia analisado, envolve 581 clientes únicos. O método exato, nas condições atuais, é inadequado para resolver esse volume no prazo típico de planejamento diário, que gira em torno de algumas horas. A complexidade NP-difícil do CVRP, somada à relaxação linear mais fraca da formulação MTZ, torna a explosão combinatória invencível por B&C puro na escala real.
Ainda assim, o método exato permanece valioso como benchmark. Os custos ótimos obtidos em C1 e C2 servirão de referência para aferir a qualidade das heurísticas da Sprint 2 e das metaheurísticas da Sprint 3 em instâncias pequenas, onde o ótimo é conhecido. Para instâncias maiores, a mesma metodologia pode ser aplicada usando o limite inferior do Gurobi (LB) como referência, mesmo na ausência de otimalidade formal.
## 7.3 Limitações identificadas

A análise desenvolvida apresenta quatro limitações importantes. As distâncias Haversine subestimam distâncias viárias reais e, no Rio de Janeiro, podem distorcer o custo de rotas que cruzam formas urbanas complexas, como túneis e vias expressas. A jornada máxima H é validada apenas em pós-processamento, o que permite ao solver produzir soluções que violam o limite de tempo operacional sem sinalizar infactibilidade. A frota considerada contempla apenas dois tipos de veículo, o que simplifica a realidade da Prolog. Os experimentos restringem-se a um único dia de operação, o que limita a generalização estatística das conclusões.
Essas limitações estão documentadas como riscos no backlog do projeto e poderão ser endereçadas nas sprints seguintes, conforme o escopo acordado com o professor e a Prolog.
## 7.4 Motivação para as Sprints 2 e 3

As evidências desta sprint justificam a progressão metodológica prevista. A Sprint 2 implementará heurísticas construtivas (Nearest Neighbor e Clarke & Wright) seguidas de busca local (2-opt, relocate e exchange) para produzir soluções viáveis em tempo polinomial e comparar sua qualidade à do método exato. A Sprint 3 desenvolverá metaheurísticas (Simulated Annealing, Iterated Local Search e Algoritmos Genéticos), com foco em instâncias grandes em que os métodos exatos se mostram inadequados e as heurísticas construtivas, por si só, deixam margem significativa para aprimoramento.

# 8 Heurísticas Construtivas — Sprint 2
## 8.1 Objetivo do estágio construtivo
A Seção 7 estabeleceu que o método exato resolve com otimalidade comprovada até 25 clientes e não converge no limite de tempo a partir de 40. A Sprint 2 aborda essa lacuna por meio de heurísticas construtivas seguidas de busca local. O estágio construtivo, objeto desta seção, produz uma solução viável em tempo polinomial sobre as quatro instâncias C1 a C4 e fornece o ponto de partida para as heurísticas de melhoria descritas na Seção 9.
Foram implementadas duas heurísticas clássicas adaptadas a frota heterogênea, conforme apresentado pelo professor no slide 25 da Aula 7B: Nearest Neighbor (NN) e Clarke-Wright Savings (CW). Cada heurística foi executada sobre as quatro instâncias e os dois critérios de seleção do veículo previstos no material da disciplina (total_cost e cost_per_client), totalizando dezesseis execuções. Os parâmetros operacionais permaneceram idênticos aos da Sprint 1 (Quadro 2), o que garante que diferenças observadas refletem exclusivamente o método de solução.
## 8.2 Algoritmo Nearest Neighbor com frota heterogênea
A heurística Nearest Neighbor constrói rotas de forma incremental a partir do depósito. A cada passo, escolhe o cliente viável mais próximo do nó atual e o agrega à rota corrente. Considera-se viável o cliente cuja inserção mantenha simultaneamente a carga acumulada abaixo da capacidade do veículo e o tempo total da rota — incluindo o retorno ao depósito — abaixo da jornada de 8 h. Quando nenhum cliente remanescente atende a esses critérios, a rota é fechada e uma nova rota é aberta com os clientes ainda não atendidos.
A extensão para frota heterogênea segue o slide 24 da Aula 7B: ao abrir cada nova rota, o algoritmo simula a construção com Fiorino e com VUC e seleciona o veículo que minimiza o critério adotado. Essa decisão é local a cada rota e não revisita escolhas anteriores. A natureza gulosa do método é responsável tanto por sua velocidade quanto por sua principal limitação: o esgotamento dos clientes próximos ao depósito tende a deixar rotas-resíduo geograficamente mal posicionadas.
## 8.3 Algoritmo Clarke-Wright Savings com frota heterogênea
A heurística Clarke-Wright Savings (CLARKE; WRIGHT, 1964) parte do extremo oposto do Nearest Neighbor: cada cliente inicia atendido por uma rota dedicada [0, i, 0]. O algoritmo calcula, para todos os pares de clientes, a economia S_ij = d_0i + d_0j - d_ij, ordena os pares em ordem decrescente e funde as rotas dos clientes envolvidos sempre que ambos estão em extremidades de suas respectivas rotas e a fusão preserva a viabilidade. Cada fusão candidata é re-simulada com Fiorino e VUC, e o veículo escolhido é aquele que minimiza o critério adotado.
Diferentemente do Nearest Neighbor, o CW é guiado pela economia global proveniente da eliminação de retornos ao depósito, não pela proximidade local. A consequência operacional é uma maior consolidação das rotas geograficamente coerentes e o uso pontual do VUC apenas quando a capacidade acumulada na fusão extrapola o limite do Fiorino.
## 8.4 Critérios de seleção do veículo
O slide 25 da Aula 7B prevê dois critérios para a escolha do veículo em cada decisão local: total_cost, que minimiza o custo total da rota candidata, e cost_per_client, que minimiza o custo por cliente atendido pela rota. A expectativa pedagógica é que o segundo critério favoreça o VUC em rotas com muitos clientes, mesmo quando o custo total individual de uma rota Fiorino é menor.
A execução das dezesseis combinações instância × heurística × critério revelou, contudo, equivalência completa entre os critérios para o conjunto de dados da Equipe 2. O Quadro 6 resume o achado e a justificativa estrutural.

Quadro 6 – Equivalência observada entre critérios total_cost e cost_per_client

Fonte: Elaboração própria.
## 8.5 Resultados nas instâncias C1 a C4
As Tabelas 7 e 8 apresentam os resultados de cada heurística sobre as quatro instâncias, executadas com critério total_cost. A coluna n_fusões da Tabela 8 registra o número de fusões aceitas pelo Clarke-Wright; o NN não tem equivalente porque cresce rotas sequencialmente. Todos os tempos de execução permaneceram abaixo de 20 ms, e nenhuma solução violou capacidade ou jornada.

Tabela 7 – Resultados do Nearest Neighbor heterogêneo em C1–C4

Fonte: Elaboração própria.

Tabela 8 – Resultados do Clarke-Wright Savings heterogêneo em C1–C4

Fonte: Elaboração própria.
O Nearest Neighbor utiliza exclusivamente Fiorinos em todas as instâncias e escala o número de rotas linearmente com o tamanho da instância (uma rota em C1, duas em C2, três em C3 e quatro em C4). O Clarke-Wright reduz o número de rotas em C3 (de três para duas) e em C4 (de quatro para três) ao mobilizar um VUC para absorver a carga consolidada, o que sinaliza que o custo fixo adicional de R$ 300 por VUC é compensado pela economia em rotas evitadas e em distância percorrida.
## 8.6 Comparação Nearest Neighbor × Clarke-Wright
A Tabela 9 consolida a comparação direta entre as duas heurísticas. O Clarke-Wright supera o Nearest Neighbor em todas as quatro instâncias, com reduções de custo entre 1,62% (C1) e 11,11% (C2).

Tabela 9 – Comparação Nearest Neighbor × Clarke-Wright (critério total_cost)

Fonte: Elaboração própria.
O ganho mais expressivo aparece em C2 (-11,11%), instância em que ambas as heurísticas usam exclusivamente Fiorino e a vantagem do CW vem de uma distribuição geográfica mais eficiente dos 25 clientes em duas rotas. As Figuras 9, 10 e 11 mostram essas diferenças espacialmente para C2, C3 e C4. A instância C1 é omitida visualmente porque os dois algoritmos convergem para uma rota única quase idêntica.

Figura 9 – Comparação das rotas Nearest Neighbor × Clarke-Wright na instância C2_25


Fonte: Elaboração própria.
Em C2 (Figura 9) a vantagem do Clarke-Wright é visualmente clara: as duas rotas Fiorino delimitam regiões compactas, enquanto o Nearest Neighbor deixa cruzamentos que aumentam a distância em 60 km. Em C3 (Figura 10) o CW separa a malha em duas regiões coerentes — Fiorino atende a região norte e VUC consolida a região sul mais densa —, ao passo que o NN gera três rotas Fiorino com sobreposição central. Em C4 (Figura 11) o padrão se repete: o CW divide a malha em três zonas com VUC para a porção mais consolidada, enquanto o NN mantém quatro rotas Fiorino, incluindo uma rota-resíduo de 135,67 km para apenas dois clientes geograficamente distantes.

Figura 10 – Comparação das rotas Nearest Neighbor × Clarke-Wright na instância C3_40


Fonte: Elaboração própria.

Figura 11 – Comparação das rotas Nearest Neighbor × Clarke-Wright na instância C4_60


Fonte: Elaboração própria.
## 8.7 Diagnóstico da restrição de jornada
A jornada máxima de 8 h emerge como restrição ativa nas duas heurísticas. A Tabela 10 distribui as rotas geradas por faixa de tempo total e identifica as rotas que operam acima de 7 h, ou seja, com folga inferior a 1 h.

Tabela 10 – Distribuição das rotas por faixa de tempo (limite H = 8 h)

Fonte: Elaboração própria.
Sete das dezoito rotas geradas pelos dois algoritmos operam acima de 7 h, com folgas mínimas de 8 minutos em C4. O Nearest Neighbor preenche rotas de forma mais agressiva — quatro rotas próximas do limite — porque seu critério guloso continua inserindo clientes enquanto houver folga suficiente para o retorno. O Clarke-Wright, por operar via fusão controlada pelo saving, rejeita fusões que aproximariam o tempo da rota do teto operacional, mesmo quando o saving envolvido seria atrativo. Essa diferença explica diretamente as rotas-resíduo observadas em C3 e C4 no Nearest Neighbor: à medida que a primeira rota se preenche até o limite, os clientes remanescentes herdam rotas que precisam percorrer longas travessias para alcançar pontos geograficamente inconvenientes.
## 8.8 Comparação com o método exato — assimetria estrutural
A Tabela 11 compara as heurísticas construtivas com a solução do MILP da Sprint 1 (Aula 4). A Figura 12 apresenta o mesmo conteúdo em gráfico de barras com rótulos de gap percentual.

Tabela 11 – Heurísticas construtivas × método exato (MILP Aula 4)

Fonte: Elaboração própria.

Figura 12 – Comparação de custos entre o método exato e as heurísticas construtivas


Fonte: Elaboração própria.
A leitura precisa ser feita com cuidado. Em C1 as três soluções praticamente coincidem (gap CW de 0,30%). Em C2 o Clarke-Wright supera o exato em 5,57%, distribuindo os 25 clientes em duas rotas Fiorino (custo combinado R$ 712,06), enquanto o MILP da Aula 4 fica preso a uma única rota VUC (R$ 754,04). Esse resultado é a confirmação empírica direta da limitação predita na Seção 6.9 e formalizada na nova Seção 4.6: a formulação atual proíbe configurações com mais de uma rota por tipo de veículo, configuração justamente preferida pelo CW em C2.
Em C3 e C4 os gaps aparentes (+36% e +64%) refletem a mesma assimetria estrutural em sentido oposto: o exato consolida toda a demanda em uma única rota VUC, regime fora do espaço de busca das heurísticas com a granularidade atual de frota. Esses gaps não indicam falha do método heurístico; indicam que as duas formulações operam em regimes diferentes de frota. A comparação simétrica entre os dois métodos depende da refatoração da formulação MILP discutida na Seção 4.6, prevista para a Sprint 3.
# 9 Busca Local: Heurísticas de Melhoria — Sprint 2
## 9.1 Posicionamento no pipeline da Sprint 2
O slide 25 da Aula 8 estrutura a Sprint 2 em dois estágios: um construtivo (Seção 8) e um de melhoria, objeto desta seção. A busca local recebe as oito soluções construtivas (quatro do NN e quatro do CW, no critério total_cost) e aplica, em sequência, dois movimentos clássicos: 2-opt intra-rota e Relocate inter-rota. O pipeline mantém o critério de aceitação por melhoria estrita — um movimento só é aceito se reduzir o custo (ou a distância, no caso do 2-opt) mantendo viabilidade de capacidade e jornada. Não há aceitação de pioras temporárias; esse mecanismo é específico das metaheurísticas da Sprint 3.
## 9.2 Movimento 2-opt intra-rota
O 2-opt, descrito originalmente por Croes (1958) e formalizado por Lin (1965), opera dentro de uma única rota. Dada uma rota [0, ..., 0], o movimento remove dois arcos não adjacentes e reconecta os segmentos invertendo o trecho intermediário. O slide 14 da Aula 8 demonstra que, quando dois arcos se cruzam, a desigualdade triangular garante que a reconexão sem cruzamentos é estritamente mais curta. O 2-opt portanto nunca aumenta a distância de uma rota: o pior caso é não encontrar movimento melhorante.
A implementação seguiu o gabarito do professor: para cada par de índices (i, k) na rota, gera-se a candidata route[:i] + route[i:k+1][::-1] + route[k+1:] e aceita-se o primeiro candidato viável que reduza a distância. Como o veículo da rota é mantido fixo, o custo fixo é preservado e a redução de custo provém exclusivamente da redução de distância (a R$ 1,50/km). A complexidade é O(n²) por rota.
## 9.3 Movimento Relocate inter-rota
O Relocate altera não a ordem mas a alocação dos clientes às rotas: remove um cliente de uma rota de origem e o reinsere em uma posição de outra rota. O slide 15 da Aula 8 enumera três efeitos potenciais — redistribuição geográfica de clientes mal alocados, balanceamento de carga e consolidação de rotas (quando o esvaziamento de uma rota a elimina). A função objetivo da aceitação é o custo total da solução, somando custos variáveis e fixos. Como o movimento envolve duas rotas, a viabilidade é validada simultaneamente em ambas (capacidade e jornada).
A estratégia adotada é first improvement, conforme o slide 21 da Aula 8: o algoritmo varre pares ordenados (rota_origem, rota_destino) com origem diferente do destino, posições internas idx_from e idx_to, e aceita o primeiro movimento que reduza estritamente o custo total. Após cada aceitação, a busca reinicia até que nenhum movimento melhore — caracterizando convergência ao ótimo local da vizinhança Relocate. A complexidade é O(k² × n²) por iteração, onde k é o número de rotas e n o número de clientes.
## 9.4 Critério de aceitação e first improvement
A escolha por melhoria estrita reflete o desenho pedagógico da disciplina: busca local pura como degrau intermediário entre construção gulosa e metaheurísticas. A consequência operacional é que o ponto de chegada depende integralmente do ponto de partida. Movimentos que exigem aceitar piora temporária — por exemplo, abrir uma rota VUC com custo fixo de R$ 550 antes que a consolidação reduza distância — ficam por construção fora do alcance do método. O fenômeno é tratado em detalhe na Seção 9.8.
## 9.5 Resultados do 2-opt
A Tabela 12 apresenta, para cada uma das oito soluções construtivas, o ganho obtido pelo 2-opt em distância e em custo. O custo cai menos que a distância porque o custo fixo dos veículos (R$ 250 por FIO, R$ 550 por VUC) é preservado.

Tabela 12 – Resultados do 2-opt sobre as oito soluções construtivas

Fonte: Elaboração própria.
A assimetria entre os dois pontos de partida é nítida e confirma o argumento do slide 24 da Aula 8. Sobre o Nearest Neighbor o 2-opt remove cruzamentos remanescentes com ganhos de distância entre 4,08% e 13,36%; sobre o Clarke-Wright o ganho fica entre 0,01% e 0,72%, indicando que as fusões por economia da Seção 8.3 já entregaram rotas localmente ótimas no sentido 2-opt. Em todas as oito execuções o tempo permaneceu abaixo de 30 ms e nenhuma viabilidade foi violada.
## 9.6 Resultados do Relocate
A Tabela 13 aplica o Relocate sobre as soluções já refinadas pelo 2-opt. O efeito é seletivo: ganhos relevantes aparecem apenas sobre as soluções oriundas do Nearest Neighbor.

Tabela 13 – Resultados do Relocate sobre as soluções pós-2-opt

Fonte: Elaboração própria.
Os destaques são as reduções em NN-C2 (-6,36% sobre o 2-opt; R$ 760,86 → R$ 712,49) e NN-C4 (-4,95%; R$ 1.506,04 → R$ 1.431,50). Sobre as quatro soluções Clarke-Wright o Relocate não encontra movimento melhorante: as rotas já constituem ótimo local da vizinhança definida. Em nenhum dos oito casos o Relocate reduziu o número de rotas — o efeito de consolidação descrito no slide 17 da Aula 8 não se materializou porque a capacidade ociosa nas rotas Fiorino é insuficiente para absorver uma rota inteira sem violar a jornada de 8 h. O tempo computacional do Relocate é dominado por NN-C4 (1,22 s), única chamada do pipeline em escala de segundos; em CW-C4 cai para 86 ms porque o algoritmo termina sem encontrar melhoria.
## 9.7 Pipeline completo: visão consolidada
A Tabela 14 consolida as três etapas (inicial → 2-opt → Relocate) e expressa os ganhos percentuais sobre a solução inicial, permitindo leitura direta do efeito acumulado do pipeline.

Tabela 14 – Pipeline completo: ganhos acumulados sobre a solução inicial

Fonte: Elaboração própria.
A leitura consolidada confirma o padrão observado nas seções anteriores. O ganho marginal do Relocate é significativo apenas sobre o Nearest Neighbor: em NN-C2 o pipeline reduz custo em 11,06% (R$ 89 absolutos), em NN-C4 reduz em 6,29% (R$ 96 absolutos). Sobre o Clarke-Wright o ganho total não excede 0,29%, o que indica que as fusões por economia já entregam, na prática, rotas em ótimo local da vizinhança 2-opt + Relocate sob melhoria estrita.
## 9.8 Vencedor por instância: NN+BL × CW+BL
A Tabela 15 compara o custo final obtido a partir de cada uma das duas soluções iniciais. A pergunta central do slide 23 da Aula 8 é qual ponto de partida leva, após a busca local, ao melhor ótimo local em cada instância.

Tabela 15 – Vencedor por instância: NN+BL × CW+BL

Fonte: Elaboração própria.
O Clarke-Wright + busca local vence em três das quatro instâncias e empata em C1, no ótimo global de R$ 422,38. A vantagem do CW cresce com o tamanho da instância (0,06% em C2, 1,35% em C3, 1,49% em C4). O resultado materializa empiricamente o argumento dos slides 22 a 24 da Aula 8: como a busca local sob melhoria estrita nunca aceita pioras, o ponto de chegada é função do ponto de partida. Em C3 e C4 o NN+BL permanece preso a uma configuração "só FIO" com três e quatro rotas respectivamente; o CW+BL preserva a configuração mista FIO+VUC já encontrada na fase construtiva. A diferença final equivale ao custo de uma rota Fiorino adicional que o Relocate é incapaz de eliminar — a transição exigiria abrir uma rota VUC (piora momentânea de R$ 550 em custo fixo) antes que a consolidação compensasse.
As Figuras 13 e 14 ilustram visualmente esse aprisionamento em C3 e C4: a coluna esquerda mostra a solução inicial Clarke-Wright (sem busca local); a coluna direita mostra a solução NN + 2-opt + Relocate. Em C3, o CW divide a malha em duas regiões coerentes (Fiorino ao norte, VUC consolidando o sul), enquanto o NN+BL mantém três rotas Fiorino com bordas entremeadas. Em C4, o CW separa em três zonas com VUC para a área mais densa, ao passo que o NN+BL permanece em quatro rotas Fiorino. A busca local reduziu cruzamentos internos em ambos os casos, mas a fronteira entre regimes de frota não é atravessada.

Figura 13 – Clarke-Wright inicial × Nearest Neighbor após busca local na instância C3_40


Fonte: Elaboração própria.

Figura 14 – Clarke-Wright inicial × Nearest Neighbor após busca local na instância C4_60


Fonte: Elaboração própria.
## 9.9 Comparação com o método exato após busca local
A Tabela 16 atualiza a comparação com o método exato considerando agora a melhor solução heurística refinada por instância. A Figura 15 traz o gráfico de barras correspondente.

Tabela 16 – Comparação após busca local × método exato

Fonte: Elaboração própria.

Figura 15 – Comparação de custos entre o método exato e as heurísticas refinadas por busca local


Fonte: Elaboração própria.
Em C1 a heurística refinada iguala o ótimo global comprovado pelo MILP. Em C2 supera o exato em 5,57%, pelos mesmos motivos estruturais discutidos na Seção 8.8: o MILP da Aula 4 não admite configurações com mais de uma rota Fiorino, e justamente essa configuração é a que o Clarke-Wright encontra. Em C3 e C4 o gap aparente positivo continua refletindo o regime "tudo em um único VUC" inacessível à heurística — e o gap pouco mudou em relação à fase construtiva, evidência adicional de que a busca local sob melhoria estrita captura ganhos apenas onde a vizinhança é suficiente, ficando neutra onde o ótimo local depende de uma transição de regime.
## 9.10 Custo computacional do pipeline
O 2-opt é O(n²) por rota e completa em sub-30 ms em todas as oito execuções. O Relocate, com complexidade O(k² × n²), domina o tempo total quando há desbalanceamento entre rotas — caso do NN-C4, único cenário do projeto que ultrapassa um segundo (1,22 s). Sobre as soluções Clarke-Wright o Relocate termina rapidamente por não encontrar melhoria. Mesmo no pior caso, o pipeline completo (NN + 2-opt + Relocate em C4) executa em 1,53 s, cinco ordens de grandeza abaixo dos 300 s de tempo-limite do exato.
# 10 Análise Comparativa Consolidada
## 10.1 Tabela-payoff consolidada
A Tabela 17 reúne, em um único painel, todos os resultados produzidos pelas Sprints 1 e 2. As colunas seguem a ordem metodológica: solução do MILP da Aula 4, construtiva Nearest Neighbor, construtiva Clarke-Wright, e as duas soluções refinadas por busca local. A última coluna identifica o método recomendado em cada instância.

Tabela 17 – Custos finais por instância e método (Sprints 1 e 2)

Fonte: Elaboração própria. * Solução do MILP com status maxTimeLimit (gap aberto após 300 s) e sujeita à restrição implícita de saída única por tipo de veículo (ver Seções 4.6 e 10.2).
Três leituras emergem da Tabela 17. Em C1 todos os métodos comprovados convergem para o mesmo valor, R$ 422,38, validando-se mutuamente. Em C2 a heurística refinada supera o ótimo da formulação MILP em 5,57%. Em C3 e C4 a aparência inverte-se — o exato apresenta custos menores —, mas, como discutido nas próximas duas subseções, o regime de operação acessado por cada método é estruturalmente diferente.
## 10.2 Quando a heurística supera o exato — C2 e a restrição implícita
O caso de C2 é a confirmação mais direta da limitação predita analiticamente na Seção 6.9 e formalizada na Seção 4.6. A demanda total de C2 (754,5 kg) excede a capacidade do Fiorino (650 kg) mas é confortavelmente acomodada por dois Fiorinos em paralelo (combinados, 1.300 kg de capacidade). A solução ótima sob essa configuração tem custo fixo combinado de 2 × R$ 250 = R$ 500 e custo variável que, no Clarke-Wright, totaliza R$ 712,06. A solução do MILP da Aula 4, restringida a no máximo uma rota por tipo de veículo, paga R$ 550 de custo fixo do VUC mais o custo variável da rota única, fechando em R$ 754,04 — R$ 41,98 acima da heurística.
O resultado não indica desempenho superior das heurísticas frente a métodos exatos: indica que a formulação MILP da Aula 4 não captura o regime ótimo de C2. A refatoração proposta na Seção 4.6 (reindexar y_(k,v) por unidade de cada tipo, ou substituir y_k por uma variável inteira n_k) corrige a assimetria. Após essa correção, espera-se que o MILP atinja em C2 o mesmo valor encontrado empiricamente pelo Clarke-Wright. A previsão é teste previsto para o início da Sprint 3.
## 10.3 Quando o exato vence — C3, C4 e o regime de frota inacessível
Em C3 e C4 a aparência se inverte: o MILP da Aula 4 entrega custos significativamente menores (R$ 769,65 e R$ 858,31) do que as heurísticas refinadas (R$ 1.047,99 e R$ 1.410,21). A leitura ingênua seria que o método exato vence em escala, mas a análise dos regimes de frota revela uma situação distinta.
O MILP em C3 e C4 consolida toda a demanda em uma única rota VUC, com custo fixo de R$ 550 e o restante em custo variável. As heurísticas, com sua granularidade fina de frota, encontram configurações com dois ou três veículos (CW-C3 usa um FIO e um VUC; CW-C4 usa dois FIO e um VUC). O consolidado "tudo em um VUC" é mais barato porque paga apenas um custo fixo, mas exige uma rota de mais de 1.295 kg e quase 8 h em C3 e de 1.958 kg em C4. As heurísticas não acessam esse regime porque cada decisão de fusão é avaliada localmente: ao crescer uma rota, o algoritmo verifica capacidade e jornada e fecha a rota quando algum dos limites é atingido. Sem mecanismo de busca global que aceite reagrupamentos custosos, o consolidado em rota única não é alcançável.
Os gaps de +36,16% (C3) e +64,30% (C4) refletem essa diferença de regime, não desvantagem genuína das heurísticas. Em uma formulação MILP simétrica — permitindo múltiplas rotas por tipo — esperamos que o exato também produza configurações mistas, e o gap se aproxime de zero. Nas instâncias maiores, porém, o tempo de convergência ao ótimo do MILP refatorado pode tornar a comparação operacionalmente desvantajosa para o método exato.
## 10.4 Trade-off tempo × qualidade
O contraste de tempo computacional é a diferença operacional mais marcante entre as três abordagens. O MILP da Aula 4 resolve C1 em 0,27 s, C2 em 52,69 s e atinge o tempo-limite de 300 s em C3 e C4 sem provar otimalidade. As heurísticas construtivas resolvem qualquer instância abaixo de 20 ms. O pipeline completo de busca local sobre o Clarke-Wright executa entre 0,7 ms (C1) e 116 ms (C4); sobre o Nearest Neighbor, atinge 1,53 s em C4 — ainda duzentas vezes mais rápido do que o exato no mesmo caso.
Em termos práticos, o método exato fica restrito a auditorias e validações em instâncias pequenas; o pipeline construtivo + busca local é compatível com a rotina diária de planejamento da Prolog, mesmo que escalado para os 581 clientes da operação completa. A próxima sprint avaliará se as metaheurísticas (SA, ILS, GA) conseguem fechar o gap em C3 e C4 sem comprometer esse perfil de execução.
## 10.5 Pipeline operacional recomendado para a Prolog
A combinação dos resultados desta sprint sustenta um protocolo operacional concreto, formalizado no Quadro 7. A robustez da recomendação vem da observação de que o custo combinado do Nearest Neighbor e do Clarke-Wright permanece abaixo de 40 ms mesmo na maior instância testada, o que torna trivial gerar ambos e selecionar o melhor.

Quadro 7 – Pipeline operacional recomendado para a Prolog

Fonte: Elaboração própria.
Sob esse protocolo, o vencedor para as instâncias testadas é o Clarke-Wright + busca local em C2, C3 e C4, com empate em C1. O custo computacional total do protocolo em C4 é de aproximadamente 1,55 s — ordens de grandeza abaixo do exato e suficientemente rápido para permitir múltiplas reexecuções diárias em resposta a mudanças no perfil de demanda.
# 11 Conclusões sobre a Viabilidade dos Métodos Heurísticos
## 11.1 Veredicto por instância
O Quadro 8 consolida o veredicto de viabilidade para o pipeline heurístico + busca local em cada instância, em paralelo ao Quadro 3 (Seção 7) que apresentou o veredicto para o método exato.

Quadro 8 – Viabilidade dos métodos heurísticos por instância

Fonte: Elaboração própria.
Os veredictos em C3 e C4 dependem da interpretação da restrição implícita do MILP da Aula 4. Sob a formulação atual, o exato é considerado a referência de qualidade, e as heurísticas são subótimas. Sob a formulação corrigida proposta na Seção 4.6, espera-se que a referência se desloque para mais próximo das heurísticas (eliminação do regime de saída única) ou que ambas convirjam para um valor intermediário.
## 11.2 Projeção para a escala real da Prolog
A operação diária da Prolog envolve 581 clientes únicos. As complexidades do Nearest Neighbor (O(n²)) e do Clarke-Wright (O(n² log n) devido à ordenação por savings) sustentam projeções diretas: tempo esperado do pipeline construtivo na escala real fica na ordem de centenas de milissegundos a poucos segundos. O 2-opt mantém O(n²) por rota e completa em segundos no pior caso; o Relocate, com O(k² × n²), pode chegar a minutos em instâncias grandes com muitas rotas, mas permanece compatível com a janela diária de planejamento.
O método heurístico, ao contrário do exato, escala graciosamente para a instância completa. A validação dessa projeção empírica — execução do pipeline sobre os 581 clientes da Prolog — está prevista para a Sprint 3, como parte da comparação consolidada entre todas as abordagens.
## 11.3 Limitações identificadas
Quatro limitações específicas da Sprint 2 merecem registro. A primeira é a incapacidade da busca local sob melhoria estrita de atravessar a fronteira entre regimes de frota observada em C3 e C4 — o Nearest Neighbor refinado permanece preso a configurações "só Fiorino". A segunda é a ausência do movimento Swap (mencionado nos slides 18-19 da Aula 8) no pipeline implementado: o Swap troca dois clientes entre rotas e poderia capturar ganhos onde o Relocate isolado é insuficiente, mas não integra o pipeline da Sprint 2 conforme o slide 25 da Aula 8 e o código do professor. A terceira é a manutenção da restrição implícita da formulação MILP da Aula 4, que ainda não foi refatorada — a refatoração é prerrequisito para uma comparação simétrica em C3 e C4. A quarta é a validação da jornada de 8 h apenas em pós-processamento, herdada da Sprint 1.
## 11.4 Motivação para a Sprint 3
As três limitações estruturais identificadas (refatoração do MILP, fronteira de regime de frota, Swap como ampliação da vizinhança) traçam um caminho concreto para a Sprint 3. As metaheurísticas previstas — Simulated Annealing, Iterated Local Search e Algoritmos Genéticos — aceitam pioras temporárias de forma controlada e são desenhadas exatamente para atravessar a barreira que impediu o NN+BL de alcançar a vantagem estrutural do CW+BL em C3 e C4. A integração entre a Sprint 2 e a Sprint 3 será operacionalmente direta: as oito soluções refinadas salvas em Aulas/8/Aula8_Busca_Local/files/ servem como ponto de partida para todas as metaheurísticas.
## 11.5 Aderência aos requisitos do Sprint Planning #2
O Quadro 9 consolida o mapeamento entre cada item previsto no Sprint Planning #2 (Aula 7A) e a seção deste relatório que o endereça, em paralelo ao Quadro 5 (Seção 6.13) para a Sprint 1.

Quadro 9 – Aderência aos requisitos do Sprint Planning #2 (Aula 7A)

Fonte: Elaboração própria.
# 12 Códigos Python
## 12.1 Organização do repositório

O repositório do projeto organiza-se a partir da raiz Proj. Distribuição Fisica/. A base de dados original mantém-se como Base de Dados.xlsx, sem alterações. A pasta Aulas/ abriga os notebooks, slides e templates do professor, subdivididos por aula (1 a 5). A pasta Modelos de Arquivos/ contém referências para formatação de entregas acadêmicas. A pasta graphify-out/ hospeda o grafo de conhecimento gerado para consulta rápida ao escopo e à arquitetura do projeto. Os arquivos EAP.jpg e Cronograma.xlsx registram, respectivamente, a Estrutura Analítica do Projeto e o cronograma consolidado.
## 12.2 Notebooks entregues

Três notebooks concentram a implementação da Sprint 1. O notebook Aulas/2/Aula2_Preparacao_Dados/notebook.ipynb lê a base bruta, limpa os campos, agrega por CEP, realiza a geocodificação e produz as quatro instâncias de teste, salvando-as em arquivos pickle reutilizáveis nos notebooks seguintes. O notebook Aulas/3/Aula3_Modelagem_MILP/notebook.ipynb apresenta a formulação MILP Parte 1 (frota homogênea, sem MTZ), resolve as quatro instâncias e gera o diagnóstico de subtours usado neste relatório. O notebook Aulas/4/Aula4_Modelagem_MILP_Parte2/notebook.ipynb evolui para a Parte 2 (frota heterogênea, com MTZ) e concentra todos os quatro experimentos computacionais apresentados na seção 6.
## 12.3 Reprodutibilidade

A reprodutibilidade dos resultados depende de três condições. A seed de amostragem das instâncias foi fixada em 42, conforme especificado no material de aula. A versão do solver utilizada foi Gurobi 13.0.1 sob licença acadêmica da PUC-Rio. As versões dos demais pacotes Python estão registradas no cabeçalho de cada notebook. Dado esse ambiente, qualquer integrante do grupo ou avaliador externo pode reexecutar o notebook da Aula 4 e reproduzir integralmente as Tabelas 1 a 6 e as Figuras 1 a 6.

# 13 Ferramentas de Gestão do Projeto
## 13.1 Metodologia SCRUM adaptada

A gestão do projeto segue uma adaptação de SCRUM orientada ao calendário acadêmico. O ciclo completo contempla três sprints, cada uma encerrada por uma Sprint Review pública (apresentação ao professor) e uma Sprint Retrospective interna (ata individual). O Product Owner é rotativo: cada um dos cinco integrantes assume o papel em uma das sprints, com responsabilidade pela priorização do backlog, intermediação com o professor e consolidação dos entregáveis. Essa rotação distribui a exposição à gestão e reduz dependências individuais.
## 13.2 Estrutura Analítica do Projeto

A Estrutura Analítica do Projeto (EAP) está orientada a entregáveis, não a atividades (PROJECT MANAGEMENT INSTITUTE, 2021). Organiza-se em cinco áreas no nível 2 e 21 entregáveis no nível 3. As áreas são Gestão de Projeto (1.1), Pesquisa e Modelagem (1.2), Implementação Computacional (1.3), Análise de Resultados (1.4) e Documentação e Apresentações (1.5). A Figura 7 apresenta o diagrama completo.

Figura 7 – Estrutura Analítica do Projeto

Fonte: Elaboração própria.

## 13.3 Cronograma

O cronograma oficial está registrado no arquivo Cronograma.xlsx, na raiz do repositório, e mapeia os 21 entregáveis da EAP às datas de início e término previstas. O Quadro 4 resume as datas dos entregáveis ativos na Sprint 1.
Quadro 4 – Datas dos entregáveis da Sprint 1


Fonte: Elaboração própria.

## 13.4 Canvas de Projeto
O Canvas de Projeto estrutura a proposta em cinco blocos principais. O problema identificado é a tomada de decisão baseada em intuição, que gera rotas ineficientes, custos elevados e baixo aproveitamento da frota. O objetivo é desenvolver um modelo CVRP para minimizar distância percorrida e número de veículos, respeitando restrições operacionais. O funcionamento da solução compreende cinco etapas: preparação dos dados, construção da matriz de custos, modelo exato, heurísticas e comparação.
Os benefícios previstos são redução de custos logísticos, melhor uso da capacidade dos veículos e método replicável para planejamento de rotas. O diferencial da proposta é o sistema híbrido que combina a precisão dos modelos exatos com a eficiência das heurísticas, viabilizando aplicação em escala real. Os stakeholders são a Prolog (empresa parceira), a equipe do projeto, a coordenação acadêmica da PUC-Rio e os clientes finais atendidos pela operação.
## 13.5 Matriz É / Não É – Faz / Não Faz
A matriz É / Não É – Faz / Não Faz delimita o escopo do projeto. O projeto é um trabalho de CVRP voltado a minimizar custo total respeitando restrições operacionais; é uma aplicação acadêmica de otimização combinatória a um caso real; é um exercício de modelagem MIP com programação linear inteira estruturada; e é um experimento computacional testado em múltiplas instâncias. O projeto não é um estudo de localização de centros de distribuição, não é um modelo estocástico, não é uma solução baseada em intuição e não é software comercial.
Em relação ao que o projeto faz: resolve roteirização com métodos exatos e heurísticos, escala para cenários reais com metaheurísticas, equilibra custo logístico com restrições operacionais e transforma dados em planos de rota executáveis. Em relação ao que o projeto não faz: não se limita a uma única técnica de solução, não ignora restrições reais como jornada de trabalho, não realiza monitoramento em tempo real (não é GPS) e não trata a execução das rotas, apenas o planejamento prévio.
## 13.6 Gestão via Trello
O Trello é a ferramenta de acompanhamento operacional das tarefas. O board do projeto adota cinco listas: Product Backlog (tarefas ainda não selecionadas), Sprint Backlog (tarefas da sprint atual), Em Andamento (tarefas em execução), Em Revisão (tarefas aguardando validação) e Finalizado (tarefas aprovadas). Cada cartão corresponde a um entregável do nível 3 da EAP ou a uma subtarefa técnica. A movimentação entre listas ocorre continuamente ao longo da sprint, refletindo o estado real do trabalho.
## 13.7 Papéis da equipe
O Grupo 2 é formado por cinco integrantes: Bernardo Caula, João Felipe Leal, Lucas Campos, Lucas Terzi e Rodrigo Pimentel. Os cinco atuam nas frentes técnicas (modelagem, implementação, análise) e de documentação (relatórios e apresentações). O papel de Product Owner é rotativo entre as três sprints, assegurando que todos os integrantes exerçam a função ao menos uma vez durante o projeto.

# 14 Considerações Finais
A Sprint 1 concluiu os onze entregáveis previstos no seu escopo, cobrindo pesquisa, modelagem, implementação, experimentação e documentação. O modelo exato MILP com restrições MTZ e frota heterogênea está operacional, com resultados reprodutíveis para as quatro instâncias de teste. A análise de viabilidade indica que a abordagem exata resolve com otimalidade comprovada até 25 clientes em tempo aceitável e perde eficiência a partir de 40 clientes, o que justifica a progressão planejada para as próximas sprints.
A contribuição central desta sprint não está em resolver a operação real da Prolog, mas em estabelecer três fundamentos que sustentarão as sprints seguintes. O primeiro é o domínio da formulação matemática completa do problema, com todas as restrições necessárias para soluções operacionalmente executáveis. O segundo é um benchmark de otimalidade comprovada em instâncias pequenas, que permitirá aferir a qualidade absoluta das heurísticas e metaheurísticas a serem desenvolvidas. O terceiro é o entendimento quantitativo dos limites práticos do método exato no contexto específico do projeto, o que fundamenta a decisão metodológica de avançar para abordagens aproximadas.
A Sprint 2, com início em 30/04/2026, abordará as heurísticas construtivas (Nearest Neighbor e Clarke & Wright) e as buscas locais clássicas (2-opt, relocate e exchange). O objetivo é produzir soluções de qualidade alta em tempo polinomial para instâncias grandes, comparando-as ao benchmark exato estabelecido nesta sprint. A Sprint 3, iniciada em 28/05/2026, encerrará o ciclo com metaheurísticas (Simulated Annealing, Iterated Local Search e Algoritmos Genéticos) e a análise comparativa final entre todas as abordagens. A expectativa é que, ao final do ciclo, o projeto entregue um plano de roteirização reprodutível, aderente às restrições reais da Prolog e escalável ao volume diário de 581 clientes.
Os riscos identificados — aproximação Haversine, jornada em pós-processamento, frota de apenas dois tipos e amostra de um único dia — foram registrados como itens de backlog para tratamento nas sprints seguintes ou em eventual extensão do projeto.

# Referências Bibliográficas
BALLOU, R. H. Gerenciamento da cadeia de suprimentos / logística empresarial. 5. ed. Porto Alegre: Bookman, 2006.
CLARKE, G.; WRIGHT, J. W. Scheduling of vehicles from a central depot to a number of delivery points. Operations Research, v. 12, n. 4, p. 568-581, 1964.
DANTZIG, G. B.; FULKERSON, D. R.; JOHNSON, S. M. Solution of a large-scale traveling-salesman problem. Operations Research, v. 2, n. 4, p. 393-410, 1954.
DANTZIG, G. B.; RAMSER, J. H. The truck dispatching problem. Management Science, v. 6, n. 1, p. 80-91, 1959.
DREZNER, Z. (Ed.). Facility location: a survey of applications and methods. New York: Springer-Verlag, 1995.
GAREY, M. R.; JOHNSON, D. S. Computers and intractability: a guide to the theory of NP-completeness. San Francisco: W. H. Freeman, 1979.
GENDREAU, M.; POTVIN, J.-Y. (Eds.). Handbook of metaheuristics. 2. ed. New York: Springer, 2010.
GOLDBARG, M.; GOLDBARG, E.; LUNA, H. Otimização combinatória e metaheurísticas: algoritmos e aplicações. Rio de Janeiro: GEN/LTC, 2015.
HART, W. E. et al. Pyomo: optimization modeling in Python. 2. ed. Cham: Springer, 2017.
HUANGFU, Q.; HALL, J. A. J. Parallelizing the dual revised simplex method. Mathematical Programming Computation, v. 10, n. 1, p. 119-142, 2018.
LAPORTE, G. The vehicle routing problem: an overview of exact and approximate algorithms. European Journal of Operational Research, v. 59, n. 3, p. 345-358, 1992.
LAPORTE, G. Fifty years of vehicle routing. Transportation Science, v. 43, n. 4, p. 408-416, 2009.
LENSTRA, J. K.; RINNOOY KAN, A. H. G. Complexity of vehicle routing and scheduling problems. Networks, v. 11, n. 2, p. 221-227, 1981.
MILLER, C. E.; TUCKER, A. W.; ZEMLIN, R. A. Integer programming formulation of traveling salesman problems. Journal of the ACM, v. 7, n. 4, p. 326-329, 1960.
NEMHAUSER, G. L.; WOLSEY, L. A. Integer and combinatorial optimization. New York: Wiley-Interscience, 1988.
NOVAES, A. G. Logística e gerenciamento da cadeia de distribuição: estratégia, operação e avaliação. 3. ed. Rio de Janeiro: Elsevier, 2007.
PAPADIMITRIOU, C. H.; STEIGLITZ, K. Combinatorial optimization: algorithms and complexity. Englewood Cliffs: Prentice-Hall, 1982.
PROJECT MANAGEMENT INSTITUTE. A guide to the project management body of knowledge (PMBOK guide). 7. ed. Newtown Square: PMI, 2021.
TOTH, P.; VIGO, D. Vehicle routing: problems, methods, and applications. 2. ed. Philadelphia: SIAM, 2014.
WOLSEY, L. A. Integer programming. New York: Wiley-Interscience, 1998.

# Anexos
Este apartado consolida, em formato de anexos, as ferramentas de gestão utilizadas na Sprint 1 e mencionadas ao longo do relatório. Os arquivos-fonte permanecem disponíveis no repositório do projeto e são referenciados nominalmente em cada anexo.
## ANEXO A – Estrutura Analítica do Projeto (EAP)
A EAP foi construída com orientação a entregáveis (PROJECT MANAGEMENT INSTITUTE, 2021) e organiza-se em cinco áreas no nível 2 e 21 entregáveis no nível 3. As áreas são: 1.1 Gestão de Projeto; 1.2 Pesquisa e Modelagem; 1.3 Implementação Computacional; 1.4 Análise de Resultados; e 1.5 Documentação e Apresentações. O diagrama completo é o registrado na Figura 7 da seção 9.2 e está também persistido no arquivo EAP.jpg, na raiz do repositório.
## ANEXO B – Cronograma de Entregáveis
O cronograma consolidado mapeia os 21 entregáveis da EAP às datas de início e término acordadas em Sprint Planning. A versão vigente está registrada no arquivo Cronograma.xlsx, na raiz do repositório. As datas dos entregáveis ativos na Sprint 1 já constam no Quadro 4 da seção 9.3 e abrangem os itens 1.1.1, 1.1.2, 1.1.3, 1.1.4, 1.2.1, 1.2.2, 1.2.3, 1.3.1, 1.4.1, 1.5.1 e 1.5.2.
## ANEXO C – Canvas de Projeto
O Canvas estrutura a proposta em cinco blocos. Problema: tomada de decisão baseada em intuição, gerando rotas ineficientes, custos elevados e baixo aproveitamento da frota. Objetivo: desenvolver um modelo CVRP que minimize distância percorrida e número de veículos, respeitando restrições operacionais. Funcionamento: pipeline em cinco etapas — preparação de dados, matriz de custos, modelo exato, heurísticas e análise comparativa. Benefícios: redução de custos logísticos, melhor uso da capacidade dos veículos e método replicável para planejamento de rotas. Diferencial: sistema híbrido que combina precisão de modelos exatos com eficiência das heurísticas, viável em escala real. Stakeholders: Prolog, equipe do projeto, coordenação acadêmica da PUC-Rio e clientes finais atendidos pela operação.
## ANEXO D – Matriz É / Não É – Faz / Não Faz
É: trabalho de CVRP voltado a minimizar custo total respeitando restrições operacionais; aplicação acadêmica de otimização combinatória a um caso real; exercício de modelagem MIP com programação linear inteira estruturada; experimento computacional testado em múltiplas instâncias.
Não É: estudo de localização de centros de distribuição; modelo estocástico; solução baseada em intuição; software comercial pronto para entrega.
Faz: resolve roteirização com métodos exatos e heurísticos; escala para cenários reais com metaheurísticas; equilibra custo logístico com restrições operacionais; transforma dados em planos de rota executáveis.
Não Faz: não se limita a uma única técnica de solução; não ignora restrições reais como jornada de trabalho; não realiza monitoramento em tempo real (não é GPS); não trata a execução das rotas, apenas o planejamento prévio.
## ANEXO E – Configuração Scrum e Trello
O ciclo Scrum adotado contempla três sprints de aproximadamente vinte dias, cada uma encerrada por Sprint Review pública (apresentação ao professor) e Sprint Retrospective interna (ata individual). O papel de Product Owner é rotativo entre os cinco integrantes do Grupo 2: Bernardo Caula, João Felipe Leal, Lucas Campos, Lucas Terzi e Rodrigo Pimentel. O acompanhamento operacional ocorre no Trello, com cinco listas: Product Backlog, Sprint Backlog, Em Andamento, Em Revisão e Finalizado. Cada cartão corresponde a um entregável do nível 3 da EAP ou a uma subtarefa técnica. As atas das Sprint Retrospectives são submetidas individualmente via Moodle conforme calendário da disciplina.
| Instância | Clientes | Demanda total (kg) | Média (kg/cliente) |
| --- | --- | --- | --- |
| C1_10 | 10 | 141,6 | 14,2 |
| C2_25 | 25 | 754,5 | 30,2 |
| C3_40 | 40 | 1.295,3 | 32,4 |
| C4_60 | 60 | 1.958,1 | 32,6 |
| Parâmetro | Símbolo | Valor |
| --- | --- | --- |
| Depósito (CD) | D | CEP 25251-560, Duque de Caxias |
| Custo variável | g | R$ 1,50/km |
| Velocidade média | v | 40 km/h |
| Tempo de atendimento | s | 15 min/cliente |
| Jornada máxima | H | 8 h |
| Fiorino – capacidade | Q_FIO | 650 kg |
| Fiorino – custo fixo | f_FIO | R$ 250/dia |
| VUC – capacidade | Q_VUC | 3.000 kg |
| VUC – custo fixo | f_VUC | R$ 550/dia |
| Instância | Clientes | Custo (R$) | Veículos | Subtours | Tempo (s) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C1_10 | 10 | 668,80 | 1 | 4 | 0,03 | optimal |
| C2_25 | 25 | 666,15 | 1 | 11 | 0,06 | optimal |
| C3_40 | 40 | 678,34 | 1 | 19 | 0,08 | optimal |
| C4_60 | 60 | 738,63 | 1 | 27 | 0,17 | optimal |
| Instância | Clientes | Custo (R$) | VUC | FIO | Rotas | Tempo (s) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1_10 | 10 | 422,38 | 0 | 1 | 1 | 0,27 | optimal |
| C2_25 | 25 | 754,04 | 1 | 0 | 1 | 52,69 | optimal |
| C3_40 | 40 | 769,65 | 1 | 0 | 1 | 300,73 | maxTimeLimit |
| C4_60 | 60 | 858,31 | 1 | 0 | 1 | 300,88 | maxTimeLimit |
| Instância | Custo COM MTZ (R$) | Restrições COM | Tempo COM (s) | Custo SEM MTZ (R$) | Subtours SEM | Tempo SEM (s) |
| --- | --- | --- | --- | --- | --- | --- |
| C1_10 | 422,38 | 139 | 0,79 | 368,80 | 4 | 0,13 |
| C2_25 | 754,04 | 709 | 65,01 | 666,15 | 11 | 0,20 |
| C3_40 | 769,65 | 1.729 | 300,98 | 676,69 | 19 | 0,17 |
| C4_60 | 858,31 | 3.789 | 300,54 | 734,59 | 28 | 0,18 |
| Instância | Custo TL=30s (R$) | Gap 30s | Custo TL=60s (R$) | Gap 60s | Custo TL=300s (R$) | Gap 300s |
| --- | --- | --- | --- | --- | --- | --- |
| C1_10 | 422,38 | 0,00% | 422,38 | 0,00% | 422,38 | 0,00% |
| C2_25 | 754,04 | 0,45% | 754,04 | 0,14% | 754,04 | 0,00% |
| C3_40 | 792,17 | 7,79% | 776,20 | 5,80% | 769,65 | 3,56% |
| C4_60 | 875,61 | 7,03% | 862,20 | 5,15% | 858,31 | 4,37% |
| Instância | Custo Gurobi (R$) | Gap | Tempo (s) | Custo HiGHS (R$) | Gap | Tempo (s) | Status HiGHS |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1_10 | 422,38 | 0,00% | 0,58 | 422,38 | 0,01% | 6,39 | optimal |
| C2_25 | 754,04 | 0,00% | 77,05 | 760,18 | 6,07% | 300,23 | maxTimeLimit |
| Variação | Custo (R$) | FIO | VUC | Mudança |
| --- | --- | --- | --- | --- |
| Base (f_VUC = R$ 550, Q_VUC = 3.000) | 422,38 | 1 | 0 | — |
| f_VUC = R$ 1.500 | 422,38 | 1 | 0 | nenhuma |
| Q_VUC = 1.000 kg | 422,38 | 1 | 0 | nenhuma |
| Requisito | Tratamento | Seção |
| --- | --- | --- |
| Teste com instâncias C1-C4 | Executado em todas as instâncias com resultados completos | 6.2, 6.3 |
| Solver utilizado | Comparação Gurobi vs. HiGHS em C1 e C2 | 6.6 |
| Limite de tempo | Três tetos testados: 30 s, 60 s e 300 s | 6.5 |
| Parâmetros de frota | Fiorino e VUC, com capacidades e custos fixos definidos | 3.6, 6.3 |
| Qualidade da solução | Custo, status e gap reportados em todas as tabelas | 6.3, 6.5 |
| Uso e remoção da MTZ | Experimento dedicado comparando COM e SEM MTZ | 6.4 |
| Custo fixo do VUC | Sensibilidade em C1 e análise do ponto de inflexão em C2 | 6.7, 6.9 |
| Velocidade média | Análise qualitativa do impacto sobre H | 6.10 |
| Tempo de serviço | Análise qualitativa do impacto sobre H | 6.11 |
| Gap vs. time limit | Tabela 4 e Figura 6, com 30 s, 60 s e 300 s | 6.5 |
| Comparação com outras equipes | Agendada para a Sprint Review #1 em 16/04/2026 | 6.12 |
| Instância | Clientes | Veredicto | Evidência |
| --- | --- | --- | --- |
| C1_10 | 10 | Viável | Ótimo comprovado em menos de 1 s, gap 0% |
| C2_25 | 25 | Viável | Ótimo comprovado em aproximadamente 65 s, gap 0% |
| C3_40 | 40 | Parcialmente viável | Solução com gap 3,56% em 300 s, sem prova de otimalidade |
| C4_60 | 60 | Insuficiente | Gap de 4,37% após 300 s, convergência lenta |
| Aspecto | Observação |
| --- | --- |
| Resultado empírico | Custo, número de rotas e composição da frota idênticos nas 16 execuções |
| Justificativa NN | Nenhum cliente isolado excede 650 kg (Fiorino); NN nunca abre rota VUC |
| Justificativa CW | VUC só é selecionado por extrapolação de capacidade na fusão; Fiorino deixa de ser candidato e a comparação entre critérios é vazia |
| Implicação operacional | Para a Equipe 2, basta executar o pipeline com total_cost |
| Inst. | Clientes | Rotas | Frota | Dist. (km) | Custo (R$) | Tempo (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 10 | 1 | 1 FIO | 120,40 | 430,60 | 0,4 |
| C2 | 25 | 2 | 2 FIO | 200,72 | 801,08 | 3,0 |
| C3 | 40 | 3 | 3 FIO | 223,24 | 1.084,86 | 7,3 |
| C4 | 60 | 4 | 4 FIO | 351,70 | 1.527,56 | 17,4 |
| Inst. | Clientes | Rotas | Frota | Dist. (km) | Custo (R$) | Fusões | Tempo (ms) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | 10 | 1 | 1 FIO | 115,75 | 423,63 | 9 | 0,4 |
| C2 | 25 | 2 | 2 FIO | 141,38 | 712,06 | 23 | 1,4 |
| C3 | 40 | 2 | 1 FIO + 1 VUC | 165,53 | 1.048,29 | 38 | 3,5 |
| C4 | 60 | 3 | 2 FIO + 1 VUC | 240,26 | 1.410,39 | 57 | 8,5 |
| Inst. | Custo NN (R$) | Custo CW (R$) | Δ Custo | Dist. NN (km) | Dist. CW (km) | Δ Dist. |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 430,60 | 423,63 | -1,62% | 120,40 | 115,75 | -3,86% |
| C2 | 801,08 | 712,06 | -11,11% | 200,72 | 141,38 | -29,57% |
| C3 | 1.084,86 | 1.048,29 | -3,37% | 223,24 | 165,53 | -25,85% |
| C4 | 1.527,56 | 1.410,39 | -7,67% | 351,70 | 240,26 | -31,69% |
| Heurística | Folgada (< 4 h) | Média (4–7 h) | Próxima do limite (> 7 h) | Total |
| --- | --- | --- | --- | --- |
| Nearest Neighbor | 3 | 3 | 4 | 10 |
| Clarke-Wright | 0 | 5 | 3 | 8 |
| Inst. | Exato (R$) | Status | CW (R$) | Gap CW | NN (R$) | Gap NN |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 422,38 | optimal | 423,63 | +0,30% | 430,60 | +1,95% |
| C2 | 754,04 | optimal | 712,06 | -5,57% | 801,08 | +6,24% |
| C3 | 769,65 | maxTimeLimit | 1.048,29 | +36,21% | 1.084,86 | +40,95% |
| C4 | 858,31 | maxTimeLimit | 1.410,39 | +64,32% | 1.527,56 | +77,97% |
| Heur. | Inst. | Dist. ini. (km) | Dist. 2-opt (km) | Ganho dist. | Custo ini. (R$) | Custo 2-opt (R$) | Ganho custo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NN | C1 | 120,40 | 114,92 | -4,55% | 430,60 | 422,38 | -1,91% |
| NN | C2 | 200,72 | 173,91 | -13,36% | 801,08 | 760,86 | -5,02% |
| NN | C3 | 223,24 | 210,44 | -5,73% | 1.084,86 | 1.065,66 | -1,77% |
| NN | C4 | 351,70 | 337,36 | -4,08% | 1.527,56 | 1.506,04 | -1,41% |
| CW | C1 | 115,75 | 114,92 | -0,72% | 423,63 | 422,38 | -0,29% |
| CW | C2 | 141,38 | 141,37 | -0,01% | 712,06 | 712,05 | 0,00% |
| CW | C3 | 165,53 | 165,33 | -0,12% | 1.048,29 | 1.047,99 | -0,03% |
| CW | C4 | 240,26 | 240,14 | -0,05% | 1.410,39 | 1.410,21 | -0,01% |
| Heur. | Inst. | Custo 2-opt (R$) | Custo final (R$) | Ganho custo | Tempo (ms) |
| --- | --- | --- | --- | --- | --- |
| NN | C1 | 422,38 | 422,38 | 0,00% | 0,0 |
| NN | C2 | 760,86 | 712,49 | -6,36% | 42,6 |
| NN | C3 | 1.065,66 | 1.062,31 | -0,31% | 74,1 |
| NN | C4 | 1.506,04 | 1.431,50 | -4,95% | 1.505,3 |
| CW | C1 | 422,38 | 422,38 | 0,00% | 0,0 |
| CW | C2 | 712,05 | 712,05 | 0,00% | 9,6 |
| CW | C3 | 1.047,99 | 1.047,99 | 0,00% | 23,9 |
| CW | C4 | 1.410,21 | 1.410,21 | 0,00% | 98,0 |
| Heur. | Inst. | Custo ini. (R$) | Custo 2-opt (R$) | Custo final (R$) | Ganho total | Tempo total (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| NN | C1 | 430,60 | 422,38 | 422,38 | -1,91% | 1,6 |
| NN | C2 | 801,08 | 760,86 | 712,49 | -11,06% | 56,4 |
| NN | C3 | 1.084,86 | 1.065,66 | 1.062,31 | -2,08% | 87,6 |
| NN | C4 | 1.527,56 | 1.506,04 | 1.431,50 | -6,29% | 1.530,2 |
| CW | C1 | 423,63 | 422,38 | 422,38 | -0,29% | 0,7 |
| CW | C2 | 712,06 | 712,05 | 712,05 | 0,00% | 13,1 |
| CW | C3 | 1.048,29 | 1.047,99 | 1.047,99 | -0,03% | 37,3 |
| CW | C4 | 1.410,39 | 1.410,21 | 1.410,21 | -0,01% | 116,2 |
| Inst. | NN+BL (R$) | CW+BL (R$) | Vencedor | Vantagem (R$) | Vantagem (%) |
| --- | --- | --- | --- | --- | --- |
| C1 | 422,38 | 422,38 | empate | 0,00 | 0,00% |
| C2 | 712,49 | 712,05 | CW+BL | 0,44 | -0,06% |
| C3 | 1.062,31 | 1.047,99 | CW+BL | 14,33 | -1,35% |
| C4 | 1.431,50 | 1.410,21 | CW+BL | 21,29 | -1,49% |
| Inst. | Exato (R$) | Status | Melhor heur+BL (R$) | Origem | Gap |
| --- | --- | --- | --- | --- | --- |
| C1 | 422,38 | optimal | 422,38 | CW+BL (empate NN+BL) | 0,00% |
| C2 | 754,04 | optimal | 712,05 | CW+BL | -5,57% |
| C3 | 769,65 | maxTimeLimit | 1.047,99 | CW+BL | +36,16% |
| C4 | 858,31 | maxTimeLimit | 1.410,21 | CW+BL | +64,30% |
| Inst. | Exato (R$) | NN (R$) | CW (R$) | NN+BL (R$) | CW+BL (R$) | Recomendado |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 422,38 | 430,60 | 423,63 | 422,38 | 422,38 | Empate (Exato/CW+BL/NN+BL) |
| C2 | 754,04 | 801,08 | 712,06 | 712,49 | 712,05 | CW+BL |
| C3 | 769,65* | 1.084,86 | 1.048,29 | 1.062,31 | 1.047,99 | CW+BL |
| C4 | 858,31* | 1.527,56 | 1.410,39 | 1.431,50 | 1.410,21 | CW+BL |
| Passo | Ação | Tempo esperado em C4 |
| --- | --- | --- |
| 1 | Gerar a solução inicial Nearest Neighbor heterogêneo | ~17 ms |
| 2 | Gerar a solução inicial Clarke-Wright Savings heterogêneo | ~9 ms |
| 3 | Aplicar 2-opt + Relocate sobre cada solução inicial | ~1,5 s (NN) / ~0,12 s (CW) |
| 4 | Selecionar a solução de menor custo total para execução | desprezível |
| Inst. | Veredicto | Evidência |
| --- | --- | --- |
| C1 | Ótimo confirmado | CW+BL e NN+BL atingem R$ 422,38 — mesmo valor do MILP ótimo |
| C2 | Supera o MILP atual | CW+BL atinge R$ 712,05 — 5,57% abaixo do MILP da Aula 4 |
| C3 | Subótimo conhecido | CW+BL em R$ 1.047,99 versus MILP em R$ 769,65 (regime diferente) |
| C4 | Subótimo conhecido | CW+BL em R$ 1.410,21 versus MILP em R$ 858,31 (regime diferente) |
| Requisito | Tratamento | Seção |
| --- | --- | --- |
| Implementar Nearest Neighbor heterogêneo | Algoritmo + execução em C1-C4 com critério total_cost | 8.2, 8.5 |
| Implementar Clarke-Wright Savings heterogêneo | Algoritmo + execução em C1-C4 com critério total_cost | 8.3, 8.5 |
| Comparar critérios total_cost × cost_per_client | Quadro 6 + execução das 16 combinações | 8.4 |
| Comparar Nearest Neighbor × Clarke-Wright | Tabela 9 + análise dos custos, distâncias e composição de frota | 8.6 |
| Diagnosticar restrição de jornada | Tabela 10 + análise das rotas próximas do limite | 8.7 |
| Implementar busca local 2-opt + Relocate | Pipeline completo aplicado às 8 soluções construtivas | 9.2 a 9.7 |
| Comparar NN+BL × CW+BL | Tabela 15 + análise do aprisionamento por regime | 9.8 |
| Comparar heurísticas + busca local × exato | Tabela 16, Figura 15 e análise da assimetria estrutural | 9.9, 10.3 |
| ID | Entregável | Início | Término |
| --- | --- | --- | --- |
| 1.1.1 | EAP | 19/03 | 25/03 |
| 1.1.2 | Canvas de Projeto | 19/03 | 01/04 |
| 1.1.3 | Cronograma | 19/03 | 25/03 |
| 1.1.4 | Matriz É / Não É – Faz / Não Faz | 19/03 | 25/03 |
| 1.2.1 | Revisão da Literatura | 12/03 | 25/03 |
| 1.2.2 | Descrição do Problema e Dados | 12/03 | 18/03 |
| 1.2.3 | Modelo Matemático MILP | 19/03 | 01/04 |
| 1.3.1 | Modelo Exato (Gurobi) | 26/03 | 09/04 |
| 1.4.1 | Resultados do Método Exato | 02/04 | 15/04 |
| 1.5.1 | Relatório Parcial #1 | 09/04 | 18/04 |
| 1.5.2 | Apresentação Sprint Review #1 | 09/04 | 16/04 |