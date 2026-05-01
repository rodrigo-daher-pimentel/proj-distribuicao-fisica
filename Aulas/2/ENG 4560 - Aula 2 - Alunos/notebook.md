# **PUC-Rio | Departamento de Engenharia Industrial**
# **ENG 4560: Projeto Integrado VI - Distribuição Física**

---

## **Aula 2 — Preparação, tratamento e estruturação da base de dados**

**Prof. Marcello Congro (marcellocongro@puc-rio.br)**

---

## Objetivos da Aula

Ao final desta aula, você será capaz de:

1. Transformar uma base operacional real em uma estrutura de dados adequada para modelagem do **CVRP**;
2. Construir as principais entradas do modelo matemático:
   - conjunto de nós (depósito + clientes),
   - vetor de demanda,
   - matriz de distâncias,
   - matriz de custos,
   - matriz de tempos;
3. Gerar **instâncias** com diferentes tamanhos (C1–C4) para analisar **escalabilidade computacional**;
4. Exportar datasets completos e consistentes para a **Aula 3**, onde implementaremos a solução exata via **Programação Linear Inteira (PLI)**.

---

## Definição: o que é uma instância?

Nesta disciplina, uma **instância** do CVRP será representada por:

$$
\mathcal{I} = (N, D, q, \mathcal{K}, Q, g, v, s, H)
$$

onde:

- $N = \{0,1,\dots,n\}$ é o conjunto de nós (0 = depósito, demais = clientes);
- $D_{ij}$ é a matriz de distâncias entre nós $i$ e $j$;
- $q_i$ é a demanda do cliente $i$ (nesta aula: $q_i$ = peso em kg);
- $\mathcal{K}$ é o conjunto de tipos de veículos (Fiorino, VUC);
- $Q_k$ é a capacidade do veículo do tipo $k$;
- $g$ é o custo variável por km;
- $v$ é a velocidade média operacional;
- $s$ é o tempo de atendimento por cliente;
- $H$ é a jornada máxima.

Ao selecionar um subconjunto de clientes, criamos uma nova instância com menor cardinalidade de $N$.  
Essa estratégia permite comparar esforço computacional e qualidade de solução à medida que o problema cresce.

---

## Por que precisamos estruturar nossos dados?

Na Aula 3, resolveremos o seguinte problema (forma conceitual):

$$
\min \sum_{i \in N} \sum_{j \in N} c_{ij} \, x_{ij}
$$

onde:

- $x_{ij}$ indica se o arco $(i,j)$ é percorrido por algum veículo;
- $c_{ij}$ é o custo do arco, calculado nesta aula como:

$$
c_{ij} = g \cdot D_{ij}
$$

Logo, a principal missão da Aula 2 é transformar a planilha operacional em:

- $D_{ij}$ (matriz de distâncias),
- $c_{ij}$ (matriz de custos),
- $q_i$ (vetor de demandas),
- $t_{ij}$ (matriz de tempos),

de forma estruturada, reprodutível e consistente.

---

## Observação importante sobre distância

Nesta aula, calcularemos distâncias a partir de coordenadas determinísticas derivadas do CEP.

Essa abordagem:

- não representa a distância viária real;
- é uma aproximação geométrica;
- garante reprodutibilidade e controle total do experimento computacional.

Nosso objetivo não é modelar o trânsito real, mas estruturar corretamente os parâmetros do modelo matemático.

Em aplicações reais, utilizaríamos distâncias viárias obtidas via APIs e serviços como:

- OSRM,
- HERE,
- Google Maps Platform.

Entretanto, para os fins didáticos desta disciplina, a aproximação geométrica é metodologicamente adequada e suficiente.

###**Configuração logística do problema (parâmetros)**

Nesta célula definimos os parâmetros operacionais que serão usados
na construção das entradas do modelo:

- Depósito (CEP do CD)
- Frota (tipos, capacidades, custos fixos)
- Custo variável por km (g)
- Velocidade média (v)
- Tempo de atendimento por cliente (s)
- Jornada máxima (H)

Esses parâmetros aparecem explicitamente nas equações do problema.

---

## 1. Leitura da base operacional

A planilha contém dados reais para um dia único de operação.

Cada linha representa uma agregação (por CEP) ou um registro que pode repetir CEP.

Do ponto de vista logístico, queremos construir o conjunto de clientes $N$ onde cada cliente aparece **uma única vez**.
Se um CEP aparece múltiplas vezes, isso significa múltiplos pedidos para o mesmo ponto, e precisamos **agregar**.


    Faça upload do arquivo xlsx
    



     <input type="file" id="files-60e59628-a182-4585-aee3-5afb35463990" name="files[]" multiple disabled
        style="border:none" />
     <output id="result-60e59628-a182-4585-aee3-5afb35463990">
      Upload widget is only available when the cell has been executed in the
      current browser session. Please rerun this cell to enable.
      </output>
      <script>// Copyright 2017 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Helpers for google.colab Python module.
 */
(function(scope) {
function span(text, styleAttributes = {}) {
  const element = document.createElement('span');
  element.textContent = text;
  for (const key of Object.keys(styleAttributes)) {
    element.style[key] = styleAttributes[key];
  }
  return element;
}

// Max number of bytes which will be uploaded at a time.
const MAX_PAYLOAD_SIZE = 100 * 1024;

function _uploadFiles(inputId, outputId) {
  const steps = uploadFilesStep(inputId, outputId);
  const outputElement = document.getElementById(outputId);
  // Cache steps on the outputElement to make it available for the next call
  // to uploadFilesContinue from Python.
  outputElement.steps = steps;

  return _uploadFilesContinue(outputId);
}

// This is roughly an async generator (not supported in the browser yet),
// where there are multiple asynchronous steps and the Python side is going
// to poll for completion of each step.
// This uses a Promise to block the python side on completion of each step,
// then passes the result of the previous step as the input to the next step.
function _uploadFilesContinue(outputId) {
  const outputElement = document.getElementById(outputId);
  const steps = outputElement.steps;

  const next = steps.next(outputElement.lastPromiseValue);
  return Promise.resolve(next.value.promise).then((value) => {
    // Cache the last promise value to make it available to the next
    // step of the generator.
    outputElement.lastPromiseValue = value;
    return next.value.response;
  });
}

/**
 * Generator function which is called between each async step of the upload
 * process.
 * @param {string} inputId Element ID of the input file picker element.
 * @param {string} outputId Element ID of the output display.
 * @return {!Iterable<!Object>} Iterable of next steps.
 */
function* uploadFilesStep(inputId, outputId) {
  const inputElement = document.getElementById(inputId);
  inputElement.disabled = false;

  const outputElement = document.getElementById(outputId);
  outputElement.innerHTML = '';

  const pickedPromise = new Promise((resolve) => {
    inputElement.addEventListener('change', (e) => {
      resolve(e.target.files);
    });
  });

  const cancel = document.createElement('button');
  inputElement.parentElement.appendChild(cancel);
  cancel.textContent = 'Cancel upload';
  const cancelPromise = new Promise((resolve) => {
    cancel.onclick = () => {
      resolve(null);
    };
  });

  // Wait for the user to pick the files.
  const files = yield {
    promise: Promise.race([pickedPromise, cancelPromise]),
    response: {
      action: 'starting',
    }
  };

  cancel.remove();

  // Disable the input element since further picks are not allowed.
  inputElement.disabled = true;

  if (!files) {
    return {
      response: {
        action: 'complete',
      }
    };
  }

  for (const file of files) {
    const li = document.createElement('li');
    li.append(span(file.name, {fontWeight: 'bold'}));
    li.append(span(
        `(${file.type || 'n/a'}) - ${file.size} bytes, ` +
        `last modified: ${
            file.lastModifiedDate ? file.lastModifiedDate.toLocaleDateString() :
                                    'n/a'} - `));
    const percent = span('0% done');
    li.appendChild(percent);

    outputElement.appendChild(li);

    const fileDataPromise = new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        resolve(e.target.result);
      };
      reader.readAsArrayBuffer(file);
    });
    // Wait for the data to be ready.
    let fileData = yield {
      promise: fileDataPromise,
      response: {
        action: 'continue',
      }
    };

    // Use a chunked sending to avoid message size limits. See b/62115660.
    let position = 0;
    do {
      const length = Math.min(fileData.byteLength - position, MAX_PAYLOAD_SIZE);
      const chunk = new Uint8Array(fileData, position, length);
      position += length;

      const base64 = btoa(String.fromCharCode.apply(null, chunk));
      yield {
        response: {
          action: 'append',
          file: file.name,
          data: base64,
        },
      };

      let percentDone = fileData.byteLength === 0 ?
          100 :
          Math.round((position / fileData.byteLength) * 100);
      percent.textContent = `${percentDone}% done`;

    } while (position < fileData.byteLength);
  }

  // All done.
  yield {
    response: {
      action: 'complete',
    }
  };
}

scope.google = scope.google || {};
scope.google.colab = scope.google.colab || {};
scope.google.colab._files = {
  _uploadFiles,
  _uploadFilesContinue,
};
})(self);
</script> 


    Saving Base de Dados.xlsx to Base de Dados (5).xlsx
    



  <div id="df-cfdd7706-a1b3-4661-a99d-9d15ea981433" class="colab-df-container">
    <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DataEmissao</th>
      <th>CEP Entrega</th>
      <th>Qtd volumes</th>
      <th>Peso real (kg)</th>
      <th>Valor da mercadoria (R$)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2025-06-03</td>
      <td>26383060</td>
      <td>5</td>
      <td>20.424</td>
      <td>724.23</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2025-06-03</td>
      <td>26383080</td>
      <td>3</td>
      <td>9.336</td>
      <td>797.38</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2025-06-03</td>
      <td>26383060</td>
      <td>1</td>
      <td>1.180</td>
      <td>24.46</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2025-06-03</td>
      <td>26325282</td>
      <td>1</td>
      <td>3.174</td>
      <td>595.71</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2025-06-03</td>
      <td>26311110</td>
      <td>14</td>
      <td>120.802</td>
      <td>3600.79</td>
    </tr>
  </tbody>
</table>
</div>
    <div class="colab-df-buttons">

  <div class="colab-df-container">
    <button class="colab-df-convert" onclick="convertToInteractive('df-cfdd7706-a1b3-4661-a99d-9d15ea981433')"
            title="Convert this dataframe to an interactive table."
            style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
    <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
  </svg>
    </button>

  <style>
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

    <script>
      const buttonEl =
        document.querySelector('#df-cfdd7706-a1b3-4661-a99d-9d15ea981433 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-cfdd7706-a1b3-4661-a99d-9d15ea981433');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    </script>
  </div>


    </div>
  </div>



    Dimensões da base bruta: (1021, 5)
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1021 entries, 0 to 1020
    Data columns (total 5 columns):
     #   Column                    Non-Null Count  Dtype         
    ---  ------                    --------------  -----         
     0   DataEmissao               1021 non-null   datetime64[ns]
     1   CEP Entrega               1021 non-null   int64         
     2   Qtd volumes               1021 non-null   int64         
     3   Peso real (kg)            1021 non-null   float64       
     4   Valor da mercadoria (R$)  1021 non-null   float64       
    dtypes: datetime64[ns](1), float64(2), int64(2)
    memory usage: 40.0 KB
    

## 2. Padronização e agregação por cliente (CEP)

### Por que agregamos?
No CVRP, cada cliente $i$ deve ser um nó único.  
Se o mesmo CEP aparece várias vezes, o veículo não “visita” várias vezes a mesma localização; o correto é somar as demandas e atributos.

Matematicamente, para um CEP que aparece em várias linhas:

$$q_i = \sum_{\ell \in \text{linhas do CEP}} q_\ell$$



Aqui definiremos:
* **$q_i$** = peso total (kg) do cliente $i$
* **Volumes e valor** serão atributos adicionais para análise

    CEPs repetidos (mesmo cliente em múltiplas linhas): 243
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
    </tr>
    <tr>
      <th>CEP</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>22631002</th>
      <td>10</td>
    </tr>
    <tr>
      <th>22451540</th>
      <td>9</td>
    </tr>
    <tr>
      <th>25915000</th>
      <td>6</td>
    </tr>
    <tr>
      <th>22041012</th>
      <td>6</td>
    </tr>
    <tr>
      <th>26155070</th>
      <td>6</td>
    </tr>
    <tr>
      <th>22451350</th>
      <td>6</td>
    </tr>
    <tr>
      <th>22230060</th>
      <td>6</td>
    </tr>
    <tr>
      <th>23890001</th>
      <td>6</td>
    </tr>
    <tr>
      <th>25576011</th>
      <td>6</td>
    </tr>
    <tr>
      <th>23025060</th>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div><br><label><b>dtype:</b> int64</label>


    Base consolidada (um cliente por CEP): (581, 4)
    





  <div id="df-31a02581-973f-4629-9dd5-a3d39b9d2908" class="colab-df-container">
    <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CEP</th>
      <th>volumes</th>
      <th>peso_kg</th>
      <th>valor_rs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20000001</td>
      <td>24</td>
      <td>120.003</td>
      <td>5114.61</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20080003</td>
      <td>4</td>
      <td>3.707</td>
      <td>746.42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20080004</td>
      <td>1</td>
      <td>1.026</td>
      <td>188.91</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20211260</td>
      <td>1</td>
      <td>4.560</td>
      <td>158.05</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20211270</td>
      <td>10</td>
      <td>40.233</td>
      <td>2278.68</td>
    </tr>
  </tbody>
</table>
</div>
    <div class="colab-df-buttons">

  <div class="colab-df-container">
    <button class="colab-df-convert" onclick="convertToInteractive('df-31a02581-973f-4629-9dd5-a3d39b9d2908')"
            title="Convert this dataframe to an interactive table."
            style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
    <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
  </svg>
    </button>

  <style>
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

    <script>
      const buttonEl =
        document.querySelector('#df-31a02581-973f-4629-9dd5-a3d39b9d2908 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-31a02581-973f-4629-9dd5-a3d39b9d2908');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    </script>
  </div>


    </div>
  </div>




## 3. Coordenadas e distâncias

Para calcular $D_{ij}$, precisamos de coordenadas $(lat_i, lon_i)$ para cada nó.

Nesta aula, usaremos um mapeamento determinístico do CEP para coordenadas dentro de uma “caixa” geográfica do RJ. Isso permite obter distâncias coerentes e reprodutíveis, sem depender de serviços externos.

---

### 3.1 Distância geográfica (Haversine)

Para calcular a distância entre dois pontos em uma esfera (como a Terra), usaremos a **fórmula de Haversine**:

$$D_{ij} = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\phi_i-\phi_j}{2}\right) + \cos(\phi_i)\cos(\phi_j)\sin^2\left(\frac{\lambda_i-\lambda_j}{2}\right)}\right)$$



**Onde:**
* $R \approx 6371$ km (raio médio da Terra)
* $\phi$ = latitude em radianos
* $\lambda$ = longitude em radianos





  <div id="df-9b87bce5-a666-42aa-9aea-9995a88453fc" class="colab-df-container">
    <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CEP</th>
      <th>volumes</th>
      <th>peso_kg</th>
      <th>valor_rs</th>
      <th>lat</th>
      <th>lon</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20000001</td>
      <td>24</td>
      <td>120.003</td>
      <td>5114.61</td>
      <td>-23.19991</td>
      <td>-44.16000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20080003</td>
      <td>4</td>
      <td>3.707</td>
      <td>746.42</td>
      <td>-23.19973</td>
      <td>-44.15864</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20080004</td>
      <td>1</td>
      <td>1.026</td>
      <td>188.91</td>
      <td>-23.19964</td>
      <td>-44.15864</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20211260</td>
      <td>1</td>
      <td>4.560</td>
      <td>158.05</td>
      <td>-23.08660</td>
      <td>-44.15643</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20211270</td>
      <td>10</td>
      <td>40.233</td>
      <td>2278.68</td>
      <td>-23.08570</td>
      <td>-44.15643</td>
    </tr>
  </tbody>
</table>
</div>
    <div class="colab-df-buttons">

  <div class="colab-df-container">
    <button class="colab-df-convert" onclick="convertToInteractive('df-9b87bce5-a666-42aa-9aea-9995a88453fc')"
            title="Convert this dataframe to an interactive table."
            style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
    <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
  </svg>
    </button>

  <style>
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

    <script>
      const buttonEl =
        document.querySelector('#df-9b87bce5-a666-42aa-9aea-9995a88453fc button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-9b87bce5-a666-42aa-9aea-9995a88453fc');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    </script>
  </div>


    </div>
  </div>





    
![png](images/notebook_9_0.png)
    


## 4. Construção das matrizes logísticas $D_{ij}$, $c_{ij}$ e $t_{ij}$

### 4.1 Matriz de distâncias

A distância entre cada par de nós $i$ e $j$ é representada por:

$$D_{ij} = \text{distância}(i,j)$$

### 4.2 Matriz de custo variável

Considerando um custo por quilômetro rodado $g$ (em R$/km), o custo de deslocamento entre os nós é:

$$c_{ij} = g \cdot D_{ij}$$

### 4.3 Matriz de tempo de deslocamento

Considerando uma velocidade média $v$ (em km/h), o tempo de viagem entre os nós é dado por:

$$t_{ij} = \frac{D_{ij}}{v}$$



---

O **tempo total de uma rota**, no nível conceitual, será a soma do tempo de deslocamento entre os nós visitados e o tempo de serviço em cada cliente:

$$\text{TempoRota} = \sum t_{ij}x_{ij} + \sum s \cdot y_i$$

**Onde:**
* $s$ = tempo fixo de atendimento (descarga/serviço) em cada parada.
* $y_i$ = variável indicadora que assume 1 se o cliente $i$ for visitado e 0 caso contrário.
* $x_{ij}$ = variável de decisão que assume 1 se o veículo percorre o arco entre $i$ e $j$.

    Dimensões: (582, 582) (582, 582) (582, 582)
    Exemplo D (km) [0:5,0:5]:
     [[0.000e+00 1.808e+01 1.799e+01 1.798e+01 9.260e+00]
     [1.808e+01 0.000e+00 1.400e-01 1.400e-01 1.260e+01]
     [1.799e+01 1.400e-01 0.000e+00 1.000e-02 1.258e+01]
     [1.798e+01 1.400e-01 1.000e-02 0.000e+00 1.257e+01]
     [9.260e+00 1.260e+01 1.258e+01 1.257e+01 0.000e+00]]
    


    
![png](images/notebook_12_0.png)
    


    Distância máxima (km): 90.84171761612939
    

## 5. Vetor de demanda $q_i$ e tempos de atendimento

Nesta aula, definimos a demanda de cada nó baseada no peso total acumulado:

$$q_i = \text{peso\_kg}_i$$



### Capacidade por tipo de veículo ($Q$)
A capacidade máxima de carga varia conforme a frota disponível:
* **Fiorino:** $Q = 650$ kg  
* **VUC:** $Q = 3000$ kg  

### Tempo de atendimento ($s_i$)
Definimos um tempo fixo de parada em cada cliente para carga/descarga:

$$s_i = 0.25 \text{ h} \quad (15\ \text{min})$$

### Jornada máxima ($H$)
O limite de tempo operacional diário para cada veículo/rota:

$$H = 8 \text{ h}$$

---

    Demanda total (kg) no dia: 25324.009
    Tempo de atendimento total (h) se visitar todos: 145.25
    

    ✔️ Nenhum cliente excede a capacidade máxima da frota.
    

## 6. Instâncias C1–C4 (amostragem aleatória reprodutível)

Nesta disciplina, uma **instância** é definida como um subconjunto de clientes selecionados a partir da base total.

* **C1:** 10 clientes  
* **C2:** 25 clientes  
* **C3:** 40 clientes  
* **C4:** 60 clientes  

A seleção aleatória é **reprodutível**, utilizando uma semente fixa (*seed*). Isso é fundamental para que todos os grupos trabalhem sobre os mesmos dados e obtenham resultados comparáveis.

---

### Escalabilidade computacional (por que fazemos isso?)

O CVRP (Capacitated Vehicle Routing Problem) é um problema combinatório de alta complexidade (**NP-Hard**). Em geral, o esforço computacional cresce exponencialmente com o aumento do número de clientes.



**Em termos práticos:**
* **10 clientes:** Tende a ser resolvido instantaneamente (segundos).
* **60 clientes:** Pode exigir um esforço computacional significativamente maior (minutos ou horas), dependendo do modelo e da eficiência do *solver*.

Por isso, criamos essas diferentes instâncias: para medir o impacto do tamanho do problema na performance da solução exata.

    Instâncias geradas para Equipe 1
    

## 7. Checagens rápidas de viabilidade (capacidade e jornada)

Antes de iniciar a modelagem matemática, é uma boa prática realizar checagens de ordens de grandeza para validar a viabilidade operacional.

### 7.1 Capacidade (no nível de análise)

Para qualquer instância selecionada, a demanda agregada total é:

$$Q_{\text{tot}} = \sum_{i \in N \setminus \{0\}} q_i$$

Embora o CVRP distribua essa carga em vários veículos, esse cálculo ajuda a entender a escala da operação:
* **Fiorinos "equivalentes":** $\lceil Q_{\text{tot}} / 650 \rceil$
* **VUCs "equivalentes":** $\lceil Q_{\text{tot}} / 3000 \rceil$



### 7.2 Jornada (no nível de análise)

A viabilidade temporal é o recurso mais escasso na última milha (*last mile*). Cada visita consome um tempo fixo de atendimento $s$.

O tempo total de deslocamento depende da matriz $t_{ij}$. Nesta etapa, embora ainda não tenhamos as rotas otimizadas, podemos estimar limites inferiores (como o tempo fixo total de serviço $\sum s_i$) para verificar se a jornada $H$ é compatível com o número de clientes planejado por veículo.

    
    Instância C1_10 — 10 clientes
    Demanda total (kg): 2562.8
    Mínimo teórico de Fiorinos (capacidade): 4
    Mínimo teórico de VUCs (capacidade): 1
    
    Instância C2_25 — 25 clientes
    Demanda total (kg): 2952.4
    Mínimo teórico de Fiorinos (capacidade): 5
    Mínimo teórico de VUCs (capacidade): 1
    
    Instância C3_40 — 40 clientes
    Demanda total (kg): 3717.5
    Mínimo teórico de Fiorinos (capacidade): 6
    Mínimo teórico de VUCs (capacidade): 2
    
    Instância C4_60 — 60 clientes
    Demanda total (kg): 4602.4
    Mínimo teórico de Fiorinos (capacidade): 8
    Mínimo teórico de VUCs (capacidade): 2
    

## 8. Construção e exportação dos datasets por instância

Para garantir a portabilidade e facilitar a modelagem, exportaremos os dados de cada instância de forma estruturada.

Para cada instância (C1 a C4), teremos os seguintes arquivos:

- `nodes.csv`: tabela de nós com coordenadas e demanda  
- `D.npy`: matriz $D_{ij}$ (km)  
- `Cvar.npy`: matriz $c_{ij} = g \cdot D_{ij}$ (R$)  

- `Tmov.npy`: matriz $t_{ij} = \frac{D_{ij}}{v}$ (h)
- `q.npy`: vetor de demanda (kg)  
- `s.npy`: vetor de atendimento (h)  
- `params.json`: parâmetros fixos do problema



---

### Por que exportar dessa forma?
Essa abordagem de **desacoplamento** permite que comecemos a próxima aula diretamente com a construção das restrições do modelo de Programação Linear Inteira (PLI), sem a necessidade de repetir o pré-processamento de dados ou depender de cálculos geográficos em tempo de execução.

    Datasets exportados em: /content/datasets
    

## 9. Checklist de consistência (sanity check)

Antes de encerrar, validamos:

- depósito é o nó 0
- matrizes são quadradas e compatíveis com o número de nós
- diagonal das matrizes de distância é zero


    Sanity check OK para todas as instâncias.
    

## Próximas etapas

Nesta Aula 2, construímos as entradas fundamentais para o modelo exato (PLI):

- $D_{ij}$: distâncias
- $c_{ij}$: custos ($c_{ij} = g \cdot D_{ij}$)
- $t_{ij}$: tempos ($t_{ij} = \frac{D_{ij}}{v}$)
- $q_i$: demandas
- $s_i$: atendimento
- instâncias C1–C4

Na Aula 3, você usará esses arquivos para definir variáveis $x_{ij}$, escrever a função objetivo e as restrições (grau, capacidade e tempo) e resolver com solvers exatos.
