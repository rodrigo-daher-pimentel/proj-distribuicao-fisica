<!-- converted from relatorio_base.docx -->

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
8 Códigos Python	22
8.1 Organização do repositório	22
8.2 Notebooks entregues	22
8.3 Reprodutibilidade	22
9 Ferramentas de Gestão do Projeto	23
9.1 Metodologia SCRUM adaptada	23
9.2 Estrutura Analítica do Projeto	23
9.3 Cronograma	24
9.4 Canvas de Projeto	24
9.5 Matriz É / Não É – Faz / Não Faz	24
9.6 Gestão via Trello	25
9.7 Papéis da equipe	25
10 Considerações Finais	25
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

# 8 Códigos Python
## 8.1 Organização do repositório

O repositório do projeto organiza-se a partir da raiz Proj. Distribuição Fisica/. A base de dados original mantém-se como Base de Dados.xlsx, sem alterações. A pasta Aulas/ abriga os notebooks, slides e templates do professor, subdivididos por aula (1 a 5). A pasta Modelos de Arquivos/ contém referências para formatação de entregas acadêmicas. A pasta graphify-out/ hospeda o grafo de conhecimento gerado para consulta rápida ao escopo e à arquitetura do projeto. Os arquivos EAP.jpg e Cronograma.xlsx registram, respectivamente, a Estrutura Analítica do Projeto e o cronograma consolidado.
## 8.2 Notebooks entregues

Três notebooks concentram a implementação da Sprint 1. O notebook Aulas/2/Aula2_Preparacao_Dados/notebook.ipynb lê a base bruta, limpa os campos, agrega por CEP, realiza a geocodificação e produz as quatro instâncias de teste, salvando-as em arquivos pickle reutilizáveis nos notebooks seguintes. O notebook Aulas/3/Aula3_Modelagem_MILP/notebook.ipynb apresenta a formulação MILP Parte 1 (frota homogênea, sem MTZ), resolve as quatro instâncias e gera o diagnóstico de subtours usado neste relatório. O notebook Aulas/4/Aula4_Modelagem_MILP_Parte2/notebook.ipynb evolui para a Parte 2 (frota heterogênea, com MTZ) e concentra todos os quatro experimentos computacionais apresentados na seção 6.
## 8.3 Reprodutibilidade

A reprodutibilidade dos resultados depende de três condições. A seed de amostragem das instâncias foi fixada em 42, conforme especificado no material de aula. A versão do solver utilizada foi Gurobi 13.0.1 sob licença acadêmica da PUC-Rio. As versões dos demais pacotes Python estão registradas no cabeçalho de cada notebook. Dado esse ambiente, qualquer integrante do grupo ou avaliador externo pode reexecutar o notebook da Aula 4 e reproduzir integralmente as Tabelas 1 a 6 e as Figuras 1 a 6.

# 9 Ferramentas de Gestão do Projeto
## 9.1 Metodologia SCRUM adaptada

A gestão do projeto segue uma adaptação de SCRUM orientada ao calendário acadêmico. O ciclo completo contempla três sprints, cada uma encerrada por uma Sprint Review pública (apresentação ao professor) e uma Sprint Retrospective interna (ata individual). O Product Owner é rotativo: cada um dos cinco integrantes assume o papel em uma das sprints, com responsabilidade pela priorização do backlog, intermediação com o professor e consolidação dos entregáveis. Essa rotação distribui a exposição à gestão e reduz dependências individuais.
## 9.2 Estrutura Analítica do Projeto

A Estrutura Analítica do Projeto (EAP) está orientada a entregáveis, não a atividades (PROJECT MANAGEMENT INSTITUTE, 2021). Organiza-se em cinco áreas no nível 2 e 21 entregáveis no nível 3. As áreas são Gestão de Projeto (1.1), Pesquisa e Modelagem (1.2), Implementação Computacional (1.3), Análise de Resultados (1.4) e Documentação e Apresentações (1.5). A Figura 7 apresenta o diagrama completo.

Figura 7 – Estrutura Analítica do Projeto

Fonte: Elaboração própria.

## 9.3 Cronograma

O cronograma oficial está registrado no arquivo Cronograma.xlsx, na raiz do repositório, e mapeia os 21 entregáveis da EAP às datas de início e término previstas. O Quadro 4 resume as datas dos entregáveis ativos na Sprint 1.
Quadro 4 – Datas dos entregáveis da Sprint 1


Fonte: Elaboração própria.

## 9.4 Canvas de Projeto
O Canvas de Projeto estrutura a proposta em cinco blocos principais. O problema identificado é a tomada de decisão baseada em intuição, que gera rotas ineficientes, custos elevados e baixo aproveitamento da frota. O objetivo é desenvolver um modelo CVRP para minimizar distância percorrida e número de veículos, respeitando restrições operacionais. O funcionamento da solução compreende cinco etapas: preparação dos dados, construção da matriz de custos, modelo exato, heurísticas e comparação.
Os benefícios previstos são redução de custos logísticos, melhor uso da capacidade dos veículos e método replicável para planejamento de rotas. O diferencial da proposta é o sistema híbrido que combina a precisão dos modelos exatos com a eficiência das heurísticas, viabilizando aplicação em escala real. Os stakeholders são a Prolog (empresa parceira), a equipe do projeto, a coordenação acadêmica da PUC-Rio e os clientes finais atendidos pela operação.
## 9.5 Matriz É / Não É – Faz / Não Faz
A matriz É / Não É – Faz / Não Faz delimita o escopo do projeto. O projeto é um trabalho de CVRP voltado a minimizar custo total respeitando restrições operacionais; é uma aplicação acadêmica de otimização combinatória a um caso real; é um exercício de modelagem MIP com programação linear inteira estruturada; e é um experimento computacional testado em múltiplas instâncias. O projeto não é um estudo de localização de centros de distribuição, não é um modelo estocástico, não é uma solução baseada em intuição e não é software comercial.
Em relação ao que o projeto faz: resolve roteirização com métodos exatos e heurísticos, escala para cenários reais com metaheurísticas, equilibra custo logístico com restrições operacionais e transforma dados em planos de rota executáveis. Em relação ao que o projeto não faz: não se limita a uma única técnica de solução, não ignora restrições reais como jornada de trabalho, não realiza monitoramento em tempo real (não é GPS) e não trata a execução das rotas, apenas o planejamento prévio.
## 9.6 Gestão via Trello
O Trello é a ferramenta de acompanhamento operacional das tarefas. O board do projeto adota cinco listas: Product Backlog (tarefas ainda não selecionadas), Sprint Backlog (tarefas da sprint atual), Em Andamento (tarefas em execução), Em Revisão (tarefas aguardando validação) e Finalizado (tarefas aprovadas). Cada cartão corresponde a um entregável do nível 3 da EAP ou a uma subtarefa técnica. A movimentação entre listas ocorre continuamente ao longo da sprint, refletindo o estado real do trabalho.
## 9.7 Papéis da equipe
O Grupo 2 é formado por cinco integrantes: Bernardo Caula, João Felipe Leal, Lucas Campos, Lucas Terzi e Rodrigo Pimentel. Os cinco atuam nas frentes técnicas (modelagem, implementação, análise) e de documentação (relatórios e apresentações). O papel de Product Owner é rotativo entre as três sprints, assegurando que todos os integrantes exerçam a função ao menos uma vez durante o projeto.

# 10 Considerações Finais
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