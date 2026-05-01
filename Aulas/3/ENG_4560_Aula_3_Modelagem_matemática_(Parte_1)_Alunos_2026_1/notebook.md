# **PUC-Rio | Departamento de Engenharia Industrial**
# **ENG 4560: Projeto Integrado VI - Distribuição Física**

---

# **Aula 3 — Modelagem matemática do CVRP (Parte 1)**  
**Prof. Marcello Congro (marcellocongro@puc-rio.br)**

---

## 🎯 Objetivos da Aula

Ao final desta aula, você será capaz de:

1. **Carregar** uma instância preparada na Aula 2 (`nodes.csv`, `D.npy`, `Cvar.npy`, `q.npy`, `s.npy`, `Tmov_h.npy`, `params.json`);
2. **Entender a estrutura** de um modelo de Programação Linear Inteira (PLI/MIP) no Pyomo;
3. Definir variáveis binárias de roteamento $x_{ij}$ e conectar isso a uma interpretação logística;
4. Construir a **função objetivo** com:
   - custo variável proporcional à distância ($c_{ij}$)
   - custo fixo por veículo/rota (aqui: VUC)
5. Implementar restrições fundamentais:
   - visita única (entrada/saída)
   - conservação de fluxo
   - balanço no depósito
   - capacidade **agregada** (via número de rotas)
   - jornada **agregada** (via número de rotas)
6. Resolver o modelo com um solver MIP e **interpretar**:
   - custo total
   - número de veículos (rotas)
   - estrutura das rotas retornadas
7. Diagnosticar **subtours** (ciclos desconectados do depósito), já que nesta etapa **não usamos MTZ**.

O objetivo não é apenas obter uma solução computacional, mas compreender:

- como traduzir um problema operacional em linguagem matemática;
- quais hipóteses estamos assumindo;
- quais limitações surgem quando a formulação ainda não está completa.

⚠️ Atenção: ao final desta aula você perceberá que uma solução ótima do solver nem sempre representa uma solução operacionalmente aceitável.

Essa constatação será fundamental para a Aula 4.

---

## 📌 Contexto

Na Aula 2, estruturamos uma instância contendo:

- Conjunto de nós $$N=\{0,1,\ldots,n\}$$ (0 é o depósito)
- Distâncias (km) $$D_{ij}$$
- Custos variáveis (reais) $$C_{ij}$$
- Tempos de deslocamento (h) $$T_{ij}$$
- Demandas (kg) $$q_i$$
- Tempos de atendimento (h) $$s_i$$

Nesta aula, vamos transformar isso em um **modelo matemático** que o solver consegue resolver.

---

## Como trabalhar neste notebook

Este material foi estruturado como um **estudo guiado**.

Recomenda-se:

1. Ler cada seção antes de executar as células;
2. Discutir em grupo as perguntas indicadas;
3. Anotar observações durante a execução.

Evite executar todas as células de uma vez. O aprendizado ocorre durante a construção do modelo.

# Estrutura da Aula Prática

1. Carregar e validar instância
2. Definir parâmetros logísticos
3. Construir modelo matemático em Pyomo
4. Resolver com solver MIP
5. Interpretar solução
6. Diagnosticar limitações estruturais

    0% [Working]            Hit:1 https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/ InRelease
    Get:2 https://cli.github.com/packages stable InRelease [3,917 B]
    Hit:3 http://security.ubuntu.com/ubuntu jammy-security InRelease
    Hit:4 http://archive.ubuntu.com/ubuntu jammy InRelease
    Hit:5 http://archive.ubuntu.com/ubuntu jammy-updates InRelease
    Hit:6 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease
    Hit:7 http://archive.ubuntu.com/ubuntu jammy-backports InRelease
    Hit:8 https://ppa.launchpadcontent.net/ubuntugis/ppa/ubuntu jammy InRelease
    Hit:9 https://r2u.stat.illinois.edu/ubuntu jammy InRelease
    Fetched 3,917 B in 3s (1,284 B/s)
    Reading package lists... Done
    W: Skipping acquire of configured file 'main/source/Sources' as repository 'https://r2u.stat.illinois.edu/ubuntu jammy InRelease' does not seem to provide it (sources.list entry misspelt?)
    Reading package lists... Done
    Building dependency tree... Done
    Reading state information... Done
    coinor-cbc is already the newest version (2.10.7+ds1-1).
    0 upgraded, 0 newly installed, 0 to remove and 77 not upgraded.
    

    Requirement already satisfied: gurobipy in /usr/local/lib/python3.12/dist-packages (13.0.1)
    Credenciais WLS configuradas.
    

    Faça upload dos arquivos da instância:
    



     <input type="file" id="files-85e9c533-7620-4599-9d5e-58dbcffd5818" name="files[]" multiple disabled
        style="border:none" />
     <output id="result-85e9c533-7620-4599-9d5e-58dbcffd5818">
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


    Saving Cvar.npy to Cvar.npy
    Saving D.npy to D.npy
    Saving nodes.csv to nodes.csv
    Saving params.json to params.json
    Saving q.npy to q.npy
    Saving s.npy to s.npy
    Saving Tmov_h.npy to Tmov_h.npy
    Arquivos disponíveis:
    ['.config', 'nodes.csv', 'Cvar.npy', 's.npy', 'D.npy', 'q.npy', 'Tmov_h.npy', 'params.json', 'sample_data']
    

    Instância carregada: 60 clientes + depósito
    

    Número aproximado de variáveis binárias: 3660
    Número de clientes: 60
    

    WARNING:pyomo.opt:Failed to create solver with name 'cbc':
      The solver plugin was not registered.
      Please confirm that the 'pyomo.environ' package has been imported.
    Traceback (most recent call last):
      File "/usr/local/lib/python3.12/dist-packages/pyomo/opt/base/solvers.py", line 171, in __call__
        raise RuntimeError(
    RuntimeError:   The solver plugin was not registered.
      Please confirm that the 'pyomo.environ' package has been imported.
    


    ---------------------------------------------------------------------------

    ApplicationError                          Traceback (most recent call last)

    /tmp/ipython-input-2393106956.py in <cell line: 0>()
         21 solver = SolverFactory(SOLVER_NAME)
         22 
    ---> 23 if not solver.available():
         24     raise RuntimeError(f"O solver {SOLVER_NAME} não está disponível.")
         25 
    

    /usr/local/lib/python3.12/dist-packages/pyomo/opt/base/solvers.py in available(self, exception_flag)
         97         """Determine if this optimizer is available."""
         98         if exception_flag:
    ---> 99             raise ApplicationError("Solver (%s) not available" % str(self.name))
        100         return False
        101 
    

    ApplicationError: Solver (cbc) not available


    Resolvendo com solver: gurobi_direct
    


    ---------------------------------------------------------------------------

    GurobiError                               Traceback (most recent call last)

    /tmp/ipython-input-3883668023.py in <cell line: 0>()
          6 
          7 start_time = time.time()
    ----> 8 results = solver.solve(model)
          9 end_time = time.time()
         10 
    

    /usr/local/lib/python3.12/dist-packages/pyomo/solvers/plugins/solvers/direct_solver.py in solve(self, *args, **kwds)
        140                 self._initialize_callbacks(_model)
        141 
    --> 142             _status = self._apply_solver()
        143             if hasattr(self, '_transformation_data'):
        144                 del self._transformation_data
    

    /usr/local/lib/python3.12/dist-packages/pyomo/solvers/plugins/solvers/gurobi_direct.py in _apply_solver(self)
        269                     self._solver_model.setParam(gurobipy.GRB.Param.QCPDual, 1)
        270 
    --> 271         self._solver_model.optimize(self._callback)
        272         self._needs_updated = False
        273 
    

    src/gurobipy/_model.pyx in gurobipy._model.Model.optimize()
    

    GurobiError: Model too large for size-limited license; visit https://gurobi.com/unrestricted for more information


Responda, com base nos resultados obtidos:

1. O solver errou ou seguiu exatamente o que formulamos/pedimos?

2. O modelo matemático representa completamente a operação logística?

3. Qual restrição parece estar faltando?

4. Como poderíamos impedir ciclos desconectados?

5. Neste modelo utilizamos capacidade e jornada agregadas. Na prática, muitas empresas utilizam restrições individuais por veículo. Quais seriam as vantagens e desvantagens dessa modelagem?

Estas perguntas serão retomadas na Aula 4.
