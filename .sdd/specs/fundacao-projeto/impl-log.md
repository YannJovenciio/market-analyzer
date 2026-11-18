# Diário de execução — fundacao-projeto

Registro por tarefa dos comandos executados, da saída observada e das
decisões tomadas durante a implementação. Os inventários produzidos em E0
são insumo direto de E3, E5 e E8.

Ambiente: Windows 11 + PowerShell, raiz `market-analyzer/`.

---

## E0 — Auditoria e congelamento (somente leitura)

### 1.1 — Árvore limpa e preservação do histórico ✅

**Data:** 18/11/2026
**Requisitos:** 1.3, 10.4, 10.5

#### Árvore de trabalho limpa

```
$ git status --porcelain
(saída vazia)
```

Nada havia pendente: as edições de documentação da fase de planejamento já
tinham sido commitadas em `dedb337` ("docs: complete SDD planning for the
foundation spec"). Não foi necessário commit nem stash nesta tarefa.

Histórico no ponto de partida:

```
dedb337 docs: complete SDD planning for the foundation spec
b370f73 docs: add project validation and SDD steering
47d5603 refactor: flatten repository structure
35fdcc9 start repo
```

#### Preservação do histórico (critério 1.3) — **verificado**

```
$ git log --follow --oneline -- README.md
47d5603 refactor: flatten repository structure
35fdcc9 start repo
```

A saída **alcança `35fdcc9`**, como o critério 1.3 exige. O `--name-status`
mostra o motivo:

```
$ git log --follow --name-status --oneline -- README.md
47d5603 refactor: flatten repository structure
R082    o/README.md     README.md
35fdcc9 start repo
A       o/README.md
```

O git registrou `o/README.md → README.md` como **renomeação** (`R`, 82% de
similaridade), não como arquivo novo.

Verificação estendida ao commit inteiro, não só ao `README.md`:

```
$ git show --name-status --find-renames --oneline 47d5603 | contagem por tipo
24 R   (renomeações)
 0 A   (adições)
 0 D   (exclusões)
```

**Todas as 24 mudanças de `47d5603` são renomeações.** Nenhum par
adição + exclusão, que é a assinatura da cópia seguida de exclusão proibida
pelo critério 10.4.

Confirmado de passagem que `o/` não existe (critério 1.2):

```
$ git ls-files | grep -c "^o/"      → 0
$ ls -d o                           → No such file or directory
```

#### Critério 10.4 — cumprido no efeito, não na letra

O critério 10.4 exige que o achatamento tenha sido feito "por operação que
preserve o histórico (`git mv` ou equivalente), e nunca por cópia seguida de
exclusão". O dono do projeto moveu o conteúdo de `o/` para a raiz **fora do
git**, com o gerenciador de arquivos, antes do commit `47d5603`.

A letra do critério — a operação — não foi seguida. **O efeito pretendido —
histórico preservado — está verificado acima**, pela detecção de renomeação
do git em todos os 24 arquivos. Conforme `design.md` §11, A-1: *não há ação
corretiva possível nem necessária*. Fica registrado aqui para não ser lido
como critério silenciosamente ignorado.

A nota de `spec.json` ("a preservação de histórico (critério 1.3) ainda
precisa ser verificada com `git log --follow` após o commit") está, a partir
desta tarefa, **resolvida**.

#### Critério 10.5

A etapa seguinte parte de base verificada: `git status --porcelain` vazio e
histórico íntegro, ambos confirmados por comando objetivo. E0 é somente
leitura — nenhum arquivo do projeto foi alterado por esta tarefa. O único
arquivo criado é este diário, sob `.sdd/specs/fundacao-projeto/`.

**Portão:** sem portão nesta tarefa. Nada bloqueia 1.2, 1.3 e 1.4.

---

### 1.2 — Inventário das chamadas a `str.format()` ✅

**Data:** 18/11/2026
**Requisitos:** 7.1

#### Contagem — **confere com o esperado**

```
$ grep -rn "\.format(" src/ | contagem por arquivo
```

| Arquivo | Esperado | Encontrado |
|---|---|---|
| `cli.py` | 9 | **9** ✅ |
| `ingestion/csv_loader.py` | 3 | **3** ✅ |
| `ingestion/ocr_batch.py` | 5 | **5** ✅ |
| `ingestion/price_ocr.py` | 1 | **1** ✅ |
| `ingestion/video_sampler.py` | 3 | **3** ✅ |
| **Total** | **21 em 5 arquivos** | **21 em 5 arquivos** ✅ |

Nenhuma divergência. A etapa segue.

#### Inventário fechado (arquivo : linha)

Caminhos relativos a `src/market_analyzer/`.

| # | Local | Trecho |
|---|---|---|
| 1 | `cli.py:48` | `print("Item: {}".format(samples[0].item_id))` |
| 2 | `cli.py:49` | `print("Samples: {}".format(stats["count"]))` |
| 3 | `cli.py:50` | `print("Minimum: {}".format(stats["minimum"]))` |
| 4 | `cli.py:51` | `print("Maximum: {}".format(stats["maximum"]))` |
| 5 | `cli.py:52` | `print("Mean: {:.2f}".format(stats["mean"]))` |
| 6 | `cli.py:53` | `print("Median: {:.2f}".format(stats["median"]))` |
| 7 | `cli.py:54` | `print("Simulated trades: {}".format(len(trades)))` |
| 8 | `cli.py:55` | `print("Simulated profit: {:.2f}".format(sum(trade.profit for trade in trades)))` |
| 9 | `cli.py:57` | `print("Open position: {}".format(open_position.average_price))` |
| 10 | `ingestion/csv_loader.py:10` | `raise FileNotFoundError("CSV not found: {}".format(path))` |
| 11 | `ingestion/csv_loader.py:19` | `"Missing CSV columns: {}".format(", ".join(sorted(missing)))` |
| 12 | `ingestion/csv_loader.py:37` | `"Invalid CSV row {}: {}".format(line_number, error)` |
| 13 | `ingestion/ocr_batch.py:16` | `raise ValueError("Invalid sampled frame name: {}".format(path.name))` |
| 14 | `ingestion/ocr_batch.py:30` | `raise FileNotFoundError("No sampled frames found in {}".format(frames_dir))` |
| 15 | `ingestion/ocr_batch.py:46` | `"OCR failed for {}: {}".format(frame.name, error)` |
| 16 | `ingestion/ocr_batch.py:54` | `"observacao": "OCR sample at {:.1f}s".format(seconds),` |
| 17 | `ingestion/ocr_batch.py:94` | `print("Wrote {} OCR samples to {}".format(count, args.output))` |
| 18 | `ingestion/price_ocr.py:17` | `raise ValueError("No price found in OCR text: {!r}".format(text))` |
| 19 | `ingestion/video_sampler.py:18` | `raise FileNotFoundError("Video not found: {}".format(input_path))` |
| 20 | `ingestion/video_sampler.py:40` | `output_path = output_dir / "frame_{:06.1f}s.png".format(timestamp)` |
| 21 | `ingestion/video_sampler.py:74` | `print("Saved {} frames to {}".format(len(frames), args.output))` |

#### Observações que E5 precisa levar em conta

- **Todas as 21 são `str.format()` sobre literal de string**, com argumentos
  simples. Nenhum falso positivo (`.format(` de outro objeto) e nenhuma
  conversão que exija reescrita de lógica. As 21 devem aparecer como `UP032`
  no portão P1.
- As ocorrências 11, 12, 15 e 16 estão em **chamadas quebradas em várias
  linhas**; o número da linha acima é o da linha que contém o literal e o
  `.format(`.
- **Ocorrência 20 (`video_sampler.py:40`) é a formatação do nome do frame** —
  `"frame_{:06.1f}s.png"`. É a contraparte da leitura em
  `ocr_batch.py:16`/`:13`. Esta é a linha que a extração de `frame_naming`
  (tarefa 6.6) toca, e `video_sampler.py` é o arquivo sem rede de teste
  protegido pelo critério 10.3 — **deve ser o último consumidor a ser
  alterado em E5**.
- **Ocorrências 5, 6 e 8 (`cli.py`) produzem a linha de base de regressão**
  (`Mean`, `Median`, `Simulated profit`, duas casas decimais). A conversão
  para f-string precisa preservar `:.2f` exatamente, ou os portões P2, P4 e o
  de E6 acusam diferença.

#### Fora do inventário, verificado de passagem

- `grep -rn "\.format(" --include="*.py"` fora de `src/`: **nenhuma
  ocorrência**. `tests/` está limpo; o Req. 7 não alcança teste nenhum.
- `src/market_analyzer/market_analyser.py` — o shim com o nome errado,
  removido em E4 — **não contém `.format()`**. Remover o shim não altera a
  contagem de 21, e as etapas E4 e E5 não interferem uma na outra por esse
  lado.

---

### 1.3 — Varredura de caminhos obsoletos nos documentos versionados ✅

**Data:** 18/11/2026
**Requisitos:** 1.7, 2.7, 6.4

Varredura sobre os **32 arquivos versionados** (`git grep`), com as quatro
cadeias do enunciado. Para `o/` foi usada a expressão
`(^|[^A-Za-z0-9_.-])o/`, que casa `o/` como **segmento de caminho** e não
dentro de palavra terminada em "o" (`arquivo/`, `mercado/`).

#### Resultado em uma linha

| Onde | Linhas atingidas | Classificação |
|---|---:|---|
| `src/`, `tests/`, `pyproject.toml`, `.gitignore` | **0** | — |
| `README.md` | 1 | **instrução → atualizar** |
| `validacao-inicial.md` | 12 | narrativa de achado → preservar e anotar |
| `.sdd/steering/structure.md` | 4 | narrativa de achado → preservar, dar baixa |
| `.sdd/steering/tech.md`, `product.md`, `analise-inicial.md` | **0** | — |
| `.sdd/specs/fundacao-projeto/` (4 arquivos) | 69 | documento de plano → **não tocar** |

#### A — Código, testes e configuração: nenhuma ocorrência

```
$ git grep -nE 'market_analyser|src/data|initial_data\.csv|(^|[^A-Za-z0-9_.-])o/' \
      -- src tests pyproject.toml .gitignore
(saída vazia)
```

Duas consequências diretas:

- **Metade do Req. 2.7 já está satisfeita.** "Nenhum módulo, teste ou
  documento DEVE referenciar os caminhos antigos" — módulo e teste: zero. O
  que resta do 2.7 é só documental, e está nos blocos B e C abaixo.
- **A tarefa 5.1 é confirmação, não correção.** O Req. 6.4 manda corrigir
  "qualquer referência remanescente a `market_analyser`" **antes** de apagar
  o shim. Não há nenhuma em código nem em teste; o próprio
  `src/market_analyzer/market_analyser.py` não contém a cadeia no corpo. As
  cinco ocorrências de `market_analyser` em documentos são todas narrativa de
  achado (V-19). **Nada a corrigir antes da exclusão** — registrar e seguir.

#### B — Instrução, a ser atualizada (1 ocorrência)

| Arquivo : linha | Texto | Vira |
|---|---|---|
| `README.md:15` | `` - `src/data`: dados locais de desenvolvimento; capturas brutas nao devem ser versionadas. `` | `data/`, com as quatro subpastas |

É a **única** ocorrência da varredura que é instrução pura e aponta para
caminho que deixará de existir. Entra na tarefa 4.4 e é absorvida pela
reescrita do README na tarefa 8.1.

> Duas falsidades vizinhas no mesmo bloco do README **não** entram neste
> inventário (não casam com as quatro cadeias), mas são insumo da tarefa 8.1
> e já constam do V-15: `README.md:12` cita `src/market_analyzer/storage`,
> que não existe, e `README.md:14` aponta os testes para `src/tests` quando
> estão em `tests/`. Some-se `README.md:27`, que afirma que o projeto "ainda
> nao inicializa nem depende de um repositorio Git".

#### C — Narrativa de achado: preservar, anotando a localização atual

Régua do A-2: o caminho fica como evidência e recebe ao lado onde a coisa
está hoje.

**`validacao-inicial.md` — 12 linhas**

| Linha | Achado | Cadeia | Ação em 9.1 / 4.4 |
|---|---|---|---|
| 122, 123 | **V-06** | `initial_data.csv`, `src/data/processed/ocr_samples.csv` | preservar + anotar `data/reference/` nos dois |
| 216, 219 | **V-14** | `o/` | preservar; dar baixa (resolvido) |
| 227 | **V-15** | `src/tests`, `o/tests` | preservar; dar baixa |
| 232, 233 | **V-16** | `initial_data.csv`, `src/data/` | preservar + anotar; dar baixa |
| 239, 240 | **V-17** | `o/data/...`, `o/src/data/processed/` | preservar + anotar; dar baixa |
| 248 | **V-19** | `market_analyser.py` | preservar; dar baixa |
| 322 | tabela-resumo de prioridades | `o/` | preservar; dar baixa de V-14 a V-17 |
| 387 | linha **C-1** da divisão de trabalho | `o/` | preservar; dar baixa |
| 439 | registro de alterações | `o/` | **atualizar o teor**: diz "Preservação de histórico a verificar após o commit"; a tarefa 1.1 verificou |

**`.sdd/steering/structure.md` — 4 linhas**

| Linha | Achado | Cadeia | Ação em 9.2 |
|---|---|---|---|
| 88 | contexto de **V-06** | `initial_data.csv` (nome puro, sem caminho) | nada a fazer — não é caminho obsoleto |
| 104 | **V-14**, tabela de pendências | `o/` | mover para resolvido |
| 105 | **V-16**, tabela de pendências | `initial_data.csv`, `src/data/` | mover para resolvido |
| 107 | **V-19**, tabela de pendências | `market_analyser.py` | mover para resolvido |

> **Confirmação que a tarefa 9.2 pede explicitamente:** a linha 104 é a
> **única** ocorrência de `o/` em todo o `structure.md`, e está na coluna
> "Correção prevista" da tabela de pendências. Nenhum `o/` remanescente no
> steering serve de instrução; o único ajuste pendente ali é mesmo a baixa do
> V-14, como a tarefa antecipava.

`tech.md`, `product.md` e `analise-inicial.md` não contêm nenhuma das quatro
cadeias.

#### D — Documentos de plano: não tocar (69 linhas)

`design.md` (26), `requirements.md` (24), `tasks.md` (18) e `spec.json` (1).
Nestes arquivos os caminhos antigos **são o assunto**: é a spec descrevendo a
migração. Nenhuma tarefa de E8 pede alteração neles e reescrevê-los
destruiria o plano que está sendo executado.

**Duas delas são instrução operacional que precisa continuar apontando para o
caminho antigo**, porque executam *antes* da movimentação de E3:

- `tasks.md:119` e `design.md:886` —
  `market-analyzer --input src/market_analyzer/initial_data.csv`, a captura
  da linha de base da tarefa 2.3.
- `tasks.md:190-191` — os dois `git mv` que fazem a movimentação.

Atualizar qualquer uma dessas quebraria a tarefa que a contém. Ficam como
estão.

#### Lista fechada — consumidores

| Tarefa | Recebe deste inventário |
|---|---|
| **4.4** | bloco B (1 ocorrência) + as anotações de localização do bloco C |
| **5.1** | bloco A: **nada a corrigir**, confirmação registrada |
| **9.1** | as 12 linhas de `validacao-inicial.md`, incluindo a correção da linha 439 |
| **9.2** | as 4 linhas de `structure.md` e a confirmação sobre o `o/` |

#### Nota sobre este próprio diário

`impl-log.md` ainda é arquivo não rastreado e por isso ficou fora da
varredura. Quando for commitado passará a conter `o/` e `src/data` — todos
como **narrativa** (registro do que foi verificado), nunca como instrução.
Uma reexecução futura desta varredura deve classificá-lo no bloco C.

---

### 1.4 — Lista dos arquivos rastreados (insumo da auditoria de ignorar) ✅

**Data:** 18/11/2026
**Requisitos:** 3.7

#### A lista

```
$ git ls-files > %TEMP%\ma-ls-files-E0.txt
```

**32 arquivos**, salvos em
`C:\Users\yjovencio\AppData\Local\Temp\ma-ls-files-E0.txt` — **fora do
repositório**, como o enunciado exige, para não criar arquivo não rastreado.
`git status --porcelain` continua mostrando só as três mudanças da spec.

> **Correção registrada na tarefa 2.3.** Neste executor o `%TEMP%` aponta para
> uma **subpasta de sessão** (`...\AppData\Local\Temp\1`) — tanto no Git Bash
> quanto no PowerShell. O caminho acima foi escrito **explicitamente** para o
> `Temp` raiz, e não via `%TEMP%`, justamente para o arquivo sobreviver até a
> tarefa 4.5. A linha de base do CLI da tarefa 2.3 está no mesmo diretório.

Composição: 11 documentos e configuração, 15 módulos Python, 3 testes, e os
**3 arquivos que E3 e E4 vão mexer**:

| # | Arquivo | Destino |
|---|---|---|
| 12 | `src/data/processed/ocr_samples.csv` | `git mv` → `data/reference/` (E3) |
| 27 | `src/market_analyzer/initial_data.csv` | `git mv` → `data/reference/` (E3) |
| 13 | `src/market_analyzer/20261116-1555-54.7150164.mp4.lnk` | `git rm` (E4, V-04) |

#### Estado de hoje: a auditoria passa, e não prova nada

```
$ git ls-files | git check-ignore -v --no-index --stdin
(saída vazia, código 1)
```

Saída vazia é o resultado que o Req. 3.7 pede — mas **hoje ela é vazia por
vacuidade**: nenhum dos 32 arquivos casa com nenhuma regra do `.gitignore`
atual. Não há arquivo `.png`/`.mp4` rastreado, e os dois CSVs não são
alcançados por regra nenhuma. O portão P2 só passa a medir alguma coisa
depois que a tarefa 4.3 ancorar as regras.

#### V-17 reproduzido em três comandos

```
$ git check-ignore -v --no-index src/data/processed/ocr_samples.csv
(nada)                                    ← caminho REAL: não é ignorado

$ git check-ignore -v --no-index data/processed/ocr_samples.csv
.gitignore:15:data/processed/   data/processed/ocr_samples.csv
                                          ← o que a regra DE FATO cobre

$ git check-ignore -v --no-index data/reference/ocr_samples.csv
(nada)                                    ← destino pós-E3: não é ignorado
```

É o V-17 na mesa: a regra `data/processed/` existe, está ancorada na pasta do
próprio `.gitignore`, e por isso nunca alcançou o CSV, que mora em
`src/data/processed/`. **Por isso o arquivo foi versionado apesar da regra.**

A terceira linha é um achado útil para E3: `data/reference/` **já** não é
ignorado pelas regras atuais. A movimentação dos dois CSVs na tarefa 4.2 é
segura mesmo antes da reescrita do `.gitignore` na 4.3 — a ordem das duas
tarefas não é uma armadilha.

#### A flag `--no-index` é mesmo indispensável — verificado aqui

Repositório descartável em `%TEMP%`, com `arquivo.png` **rastreado** e a
regra `*.png` no `.gitignore`:

| Comando | Saída | Código |
|---|---|---|
| `git ls-files \| git check-ignore -v --stdin` | vazia | 1 |
| `git ls-files \| git check-ignore -v --no-index --stdin` | `.gitignore:1:*.png  arquivo.png` | 0 |

Sem a flag o git **silencia** sobre arquivo já rastreado, e o portão P2
passaria sempre, com qualquer `.gitignore`. A correção registrada no
`spec.json` está confirmada neste ambiente. O repositório descartável foi
apagado.

#### Previsão para o portão P2 (tarefa 4.5)

Confrontando a lista de 32 com as regras propostas na tarefa 4.3:

- os dois CSVs, já em `data/reference/`, são reincluídos por
  `!/data/reference/**` → **não ignorados**, como o Req. 3.5 exige;
- o `.lnk` **não** casa com `*.mp4` (o nome termina em `.lnk`), então não é
  ignorado nem atrapalha o P2, que roda **antes** de E4 removê-lo;
- nenhum outro rastreado casa com mídia global ou com `/data/raw/*` e
  `/data/processed/*`.

**Previsão: auditoria vazia por mérito, não por vacuidade.** Qualquer coisa
diferente disso no P2 é sinal de que as regras da 4.3 saíram do desenho.

---

## E0 encerrado

Quatro tarefas, nenhuma alteração em arquivo do projeto. Os três inventários
(1.2, 1.3, 1.4) estão fechados e registrados acima. Nada bloqueia E1.

---

## E1 — Ambiente instalável (Req. 4; habilita o Req. 5)

### 2.1 — `pyproject.toml` com grupo `dev`, pytest e ruff ✅

**Data:** 18/11/2026
**Requisitos:** 4.2, 4.3, 5.3, 7.2

Primeira tarefa da spec que altera arquivo do projeto. Conteúdo conforme
`design.md` D-7, sem desvio de valor.

#### Diff: 14 inserções, 0 remoções

Nenhuma linha preexistente foi tocada.

```toml
[project.optional-dependencies]
dev = [
    "pytest>=9.0",
    "ruff>=0.17",
]

[tool.pytest.ini_options]
minversion = "9.0"
testpaths = ["tests"]
addopts = ["-ra"]

[tool.ruff.lint]
# Conjunto padrao do ruff (E4, E7, E9, F) + a regra exigida pelo Requisito 7.
select = ["E4", "E7", "E9", "F", "UP032"]
```

`[project.optional-dependencies]` foi posto **dentro do bloco `[project]`**,
antes de `[project.scripts]`; as duas tabelas de ferramenta ficaram ao final,
depois de `[tool.setuptools.packages.find]`.

#### As quatro proibições do enunciado — verificadas por leitura do TOML

```
$ python -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); ..."
requires-python : >=3.10            ← preservado (Req. 4.3)
dev             : ['pytest>=9.0', 'ruff>=0.17']
pytest          : {'minversion': '9.0', 'testpaths': ['tests'], 'addopts': ['-ra']}
ruff.lint       : {'select': ['E4', 'E7', 'E9', 'F', 'UP032']}
pythonpath declarado?     False    ← não mascara instalação quebrada
target-version declarado? False    ← ruff infere de requires-python
```

O arquivo foi validado com `tomllib` em vez de inspeção visual: erro de
sintaxe em TOML só apareceria no `pip install` da tarefa 2.2, e aí ficaria
confundido com falha de rede ou de resolução de versão.

#### Dois pontos de forma, registrados por honestidade

- **Fim de linha.** `pyproject.toml` é **CRLF puro** (36 de 36 linhas),
  enquanto `tasks.md` é LF puro — a inconsistência que é o próprio V-24. As
  linhas acrescentadas foram escritas em **CRLF**, para não deixar o arquivo
  misto e não poluir o diff da renormalização de E2.
- **Comentário em ASCII.** O trecho de D-7 traz "Conjunto padrão"; escrevi
  "padrao", sem acento. Todo o `pyproject.toml` e o README são ASCII hoje, e
  introduzir o primeiro byte não-ASCII num arquivo de configuração às
  vésperas da renormalização de E2 troca zero benefício por algum risco. O
  sentido é idêntico e o comentário não é impresso em lugar nenhum — não se
  confunde com o Req. 11, que trata da borda do CLI.

#### Para a tarefa 2.2

Os dois pisos (`pytest>=9.0`, `ruff>=0.17`) vêm da pesquisa de D-7 —
pytest 9.2.0 de 27/10/2026 e ruff 0.17.5 de 12/11/2026. **Ainda não foram
exercitados contra o índice de pacotes**; quem prova que resolvem é o
`pip install -e ".[dev]"` da próxima tarefa.

**Portão:** não há portão nesta tarefa. O P1 vem na 2.4.

---

### 2.2 — Ambiente virtual e instalação em modo editável ✅

**Data:** 18/11/2026
**Requisitos:** 4.1, 4.3

#### Os três comandos, como escritos no enunciado

```powershell
python -m venv .venv                     # Python 3.12.10
.\.venv\Scripts\Activate.ps1             # funcionou — ver desvio 1
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

`Successfully installed` com 12 pacotes. O `pip show` confirma instalação
**editável** apontando para a raiz do repositório:

```
Name: market-analyzer
Editable project location: C:\Users\yjovencio\Desktop\market\market-analyzer
```

`.venv\Scripts\` passou a conter `market-analyzer.exe`, `pytest.exe` e
`ruff.exe`.

#### Versões resolvidas — D-7 acertou

| Pacote | Piso declarado | Resolvido | Previsto em D-7 |
|---|---|---|---|
| `pytest` | `>=9.0` | **9.2.0** | 9.2.0 (27/10/2026) ✅ |
| `ruff` | `>=0.17` | **0.17.5** | 0.17.5 (12/11/2026) ✅ |

Transitivos: numpy 2.5.5, Pillow 13.0.0, imageio-ffmpeg 0.8.1,
pytesseract 0.3.13. Python 3.12.10 satisfaz `requires-python = ">=3.10"`
(Req. 4.3).

#### Desvio 1 — a política de execução **não** bloqueou

O enunciado previa bloqueio do `Activate.ps1`. **Não houve.** Nesta máquina:

```
      Scope ExecutionPolicy
  CurrentUser    Unrestricted
 LocalMachine    RemoteSigned
```

A ativação funcionou, `$env:VIRTUAL_ENV` ficou correto e `python` passou a
resolver para o interpretador do venv.

→ **Para a tarefa 8.1:** o README deve documentar a ativação como o caminho
normal, **mantendo** a alternativa (`.\.venv\Scripts\python.exe`) como nota
para máquinas em `RemoteSigned` ou `Restricted`, que é o padrão do Windows
fora deste perfil. O desvio previsto não se materializou aqui, mas continua
plausível em outra máquina.

#### Desvio 2 — do executor, **não** do projeto

Neste ambiente cada comando roda em um processo novo de PowerShell, então a
ativação não sobrevive de um comando para o seguinte. Todas as tarefas
seguintes deste diário usam os caminhos explícitos `.\.venv\Scripts\python.exe`
e `.\.venv\Scripts\pytest.exe`.

→ **Para a tarefa 8.1: isto NÃO entra no README.** É propriedade de como a
implementação está sendo conduzida, não do projeto. Um humano com um terminal
aberto ativa uma vez e segue.

#### Desvio 3 — as aspas são mesmo obrigatórias

`".[dev]"` sem aspas é interpretado pelo PowerShell como expressão de índice.
O enunciado já avisava; fica confirmado.

#### Nenhum ruído não rastreado

```
$ git status --porcelain
 M .sdd/specs/fundacao-projeto/spec.json
 M .sdd/specs/fundacao-projeto/tasks.md
 M pyproject.toml
?? .sdd/specs/fundacao-projeto/impl-log.md
```

`.venv/` já é coberto pela regra existente do `.gitignore`. Nada a limpar
antes do P1 (Req. 10.5).

> **Correção registrada na tarefa 4.2.** Escrevi aqui que "a instalação
> editável moderna não deixa `egg-info` na árvore do projeto". **Falso** — a
> instalação criou `src/market_analyzer.egg-info/`. A conclusão continua
> válida, mas por outro motivo: o diretório é coberto pela regra
> `*.egg-info/` que já existia no `.gitignore`, e por isso nunca apareceu no
> `git status`. O mesmo vale para `src/market_analyzer/__pycache__/`, coberto
> por `__pycache__/`.

#### Observado agora, para o portão P1 (tarefa 2.4)

- **O binário do Tesseract está ausente do PATH** — o V-13 em pé. O `pip` não
  o instala; é programa externo. Os testes que dependem de OCR devem
  **pular**, não falhar, e o `addopts = ["-ra"]` da tarefa 2.1 é o que fará o
  motivo de cada *skip* aparecer na saída (Req. 5.4). Se algum **falhar** em
  vez de pular, é achado novo, não ruído de ambiente.
- O `pip` avisou que há versão nova (25.0.1 → 26.3). **Não atualizado**:
  fora do escopo desta spec e nenhum requisito fixa versão de `pip`.

**Portão:** o P1 é a tarefa 2.4. Antes dele, a 2.3 captura a linha de base do
CLI com os caminhos ainda antigos.

---

### 2.3 — Linha de base do CLI com os caminhos ainda antigos ✅

**Data:** 18/11/2026
**Requisitos:** 2.6, 7.6

```powershell
.\.venv\Scripts\market-analyzer.exe --input src/market_analyzer/initial_data.csv
```

#### Saída capturada

```text
Item: Algodão de isolamento acústico
Samples: 20
Minimum: 110037
Maximum: 220074
Mean: 154691.55
Median: 140745.00
Simulated trades: 2
Simulated profit: 179130.00
```

Salva **fora do repositório**, em
`C:\Users\yjovencio\AppData\Local\Temp\baseline-cli.txt`
(8 linhas, UTF-8, SHA-256 `3A4C3E33…2206462A`), ao lado do
`ma-ls-files-E0.txt` da tarefa 1.4.

> **Sobre `%TEMP%`:** neste executor a variável aponta para uma subpasta de
> sessão (`...\Temp\1`), no Git Bash **e** no PowerShell. Os dois artefatos
> foram gravados por caminho explícito no `Temp` raiz, para sobreviverem até
> as tarefas 4.5 e 9.5. A nota da tarefa 1.4 foi corrigida neste sentido.

#### Conferência contra a linha de base do topo de `tasks.md`

| Campo | Esperado | Obtido |
|---|---|---|
| Item | `Algodão de isolamento acústico` | idem ✅ |
| Samples | 20 | 20 ✅ |
| Minimum | 110037 | 110037 ✅ |
| Maximum | 220074 | 220074 ✅ |
| Mean | 154691.55 | 154691.55 ✅ |
| Median | 140745.00 | 140745.00 ✅ |
| Simulated trades | 2 | 2 ✅ |
| Simulated profit | 179130.00 | 179130.00 ✅ |

**Oito de oito.** É este o invariante que os portões P2, P4 e o de E6 vão
comparar.

#### V-21 não se reproduz neste console — ressalva para E6

O V-21 descreve a saída saindo como `Algod?o de isolamento ac?stico` no
terminal do Windows em **cp1252**. Aqui o console está em **chcp 65001**
(UTF-8) e os acentos saem corretos, como se vê acima.

Consequência prática: **a linha de base já nasce com a acentuação certa**, e
por isso ela sozinha não distingue "antes" de "depois" do Req. 11. Uma
tentativa de forçar `chcp 1252` dentro de uma única invocação também
devolveu texto correto — provavelmente porque o `[Console]::OutputEncoding`
do PowerShell já estava fixado quando a página de código mudou, e porque este
executor relê a saída do processo como UTF-8 de qualquer modo.

Fica registrado como **ponto em aberto da etapa E6**, não desta tarefa: a
verificação do Req. 11 vai precisar de um método que não dependa do console
deste executor — ler os **bytes** que o processo escreve em stdout sob uma
página de código cp1252, em vez de ler o texto já redecodificado. Não há o
que decidir agora; só não se deve tratar o acerto desta captura como prova de
que o V-21 está resolvido. **Ele não está** — nada foi alterado em `cli.py`
até aqui.

#### Estado do repositório

Inalterado por esta tarefa: a captura é leitura e o arquivo foi escrito fora
da árvore. `git status --porcelain` segue com as mesmas quatro entradas.

**Portão:** o P1 é a próxima tarefa, 2.4.

---

### 2.4 — Portão P1 ✅ **verde, após correção do critério 4**

**Data:** 18/11/2026
**Requisitos:** 4.7, 5.1, 5.2, 5.4, 5.5, 7.2, 7.4, 10.1, 10.5
**Estado:** 3 das 4 verificações passaram de imediato. A quarta divergiu, a
causa foi isolada, e a revisão humana decidiu **aceitar 15 e corrigir a
spec** — resolução ao final desta seção.

#### ✅ 1. Suíte — 10 verdes

```
platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0
configfile: pyproject.toml
testpaths: tests
collected 10 items

tests\test_market_analyzer.py ....    [ 40%]
tests\test_price_ocr.py ....          [ 80%]
tests\test_video_sampler.py ..        [100%]

10 passed in 0.12s
```

**10 testes, 0 falhas, 0 erros de coleta** (Req. 5.1, 5.2, 5.5). A subida de 8
para 10 é mesmo `tests/test_video_sampler.py`, que antes nem era coletado e
agora roda seus 2 casos. O `configfile: pyproject.toml` confirma que a
configuração da tarefa 2.1 está sendo lida.

#### ✅ 2. Tesseract ausente e suíte conclui mesmo assim

```
Get-Command tesseract          → AUSENTE
pytesseract.get_tesseract_version() → falha (binário ausente)
```

A suíte conclui sem nenhuma falha. **Nenhum teste foi pulado** — o resumo
`-ra` não listou nada porque não há *skip* algum: a suíte simplesmente não
exercita o binário. É o Req. 5.4 "satisfeito por desenho", como A-7 previu;
o `-ra` continua instalado para quando houver *skip* a declarar.

#### ✅ 3. `market-analyzer --help` → código de saída 0

Imprime *usage* completo com as cinco opções. Req. 4.7 atendido.

#### ❌ 4. `ruff check .` → **15 violações, não 21**

```
15  UP032  [*] f-string
Found 15 errors.
```

| Arquivo | Esperado (tarefa 1.2) | `ruff` reporta |
|---|---:|---:|
| `cli.py` | 9 | **4** (48, 54, 55, 57) |
| `csv_loader.py` | 3 | **2** (10, 37) |
| `ocr_batch.py` | 5 | 5 ✅ |
| `price_ocr.py` | 1 | 1 ✅ |
| `video_sampler.py` | 3 | 3 ✅ |
| **Total** | **21** | **15** |

**As 6 não reportadas:** `cli.py:49, 50, 51, 52, 53` e `csv_loader.py:19`.

#### A causa, isolada em repositório descartável

Primeira hipótese — conflito de aspas aninhadas sob `target-version` py310 —
**está errada**. Forçar `--target-version py312` devolve as mesmas 15.

Sonda com sete variantes:

```python
print("A: {}".format(d["k"]))        # NÃO reportado
print("B: {}".format(d['k']))        # NÃO reportado  ← sem conflito de aspas
print('C: {}'.format(d["k"]))        # NÃO reportado  ← sem conflito de aspas
print("D: {}".format(s[0]))          # reportado
print("E: {}".format(n))             # reportado
print("F: {}".format(", ".join(s)))  # NÃO reportado
print("G: {}".format(' '.join(s)))   # NÃO reportado
```

Idêntico em py310 e py312. O fator comum não é aspas nem versão:

> **`UP032` não reporta chamada a `.format()` cujo argumento contenha um
> literal de string.** É conservadorismo deliberado do ruff — ele se recusa a
> embutir um literal de string dentro de um campo de substituição.

Confere com as 6 do projeto: `stats["count"]`, `stats["minimum"]`,
`stats["maximum"]`, `stats["mean"]`, `stats["median"]` (chave literal) e
`", ".join(sorted(missing))` (literal como receptor). E confere com as 15
reportadas, em que **nenhum** argumento tem literal de string. 21 − 6 = 15,
sem sobra.

#### O que isso significa — três consequências

1. **A intenção do portão está atendida; o critério numérico, não.** O texto
   da tarefa diz que esta verificação "é a prova de que a regra está ativa de
   fato, e não apenas declarada". As 15 violações, com arquivo e linha,
   provam exatamente isso. O número 21 é que foi herdado da contagem de
   `grep` da tarefa 1.2 e supôs cobertura total do `UP032`.

2. **O Req. 7.4 tem um buraco real.** Ele diz: "SE um novo uso de `.format()`
   for introduzido, ENTÃO `ruff check` DEVE falhar apontando `UP032`". Isso é
   **falso** para qualquer `.format()` cujo argumento contenha literal de
   string — e 6 dos 21 usos do próprio projeto têm exatamente essa forma. O
   linter **não** é guarda completo da convenção. Esta é uma premissa do
   design que não se sustenta, não um erro de implementação.

3. **E5 muda de forma.** O `ruff check --fix` da tarefa 6.8 converte **15**
   dos 21. As outras **6 precisam ser convertidas à mão**, e nenhum comando
   do portão P4 vai acusar se forem esquecidas. O inventário da tarefa 1.2
   deixa de ser informativo e passa a ser **a única verificação completa do
   Req. 7.1** — `grep -c "\.format(" src/` → 0 é o que prova a conversão
   integral, não o `ruff check` limpo.

#### ✅ 5. `git status --porcelain` — só o intencional

```
 M .sdd/specs/fundacao-projeto/spec.json
 M .sdd/specs/fundacao-projeto/tasks.md
 M pyproject.toml
?? .sdd/specs/fundacao-projeto/impl-log.md
```

Nota de rodapé: a tarefa previa que `.venv/` apareceria "até a reescrita do
`.gitignore` em 4.3". **Não aparece** — o `.gitignore` atual já tem a regra
`.venv/`, e ela é ancorada na raiz, onde o venv foi criado. Sem ação.

#### Não commitado

O commit é o último passo deste portão e equivale a declará-lo verde. Com o
critério 4 em divergência explicada mas não decidida, **nada foi commitado** e
a tarefa 2.4 **não foi marcada**. A etapa E2 segue bloqueada (Req. 10.6).

#### Resolução — decidido na revisão de 18/11/2026

**Decisão: aceitar 15 como o número correto do portão e corrigir a spec.**
A intenção do portão — provar que a regra está ativa — está atendida pelas 15
violações com arquivo e linha. O número 21 era uma suposição sobre o alcance
do `UP032`, não uma medida.

Quatro documentos ajustados:

| Documento | Ajuste |
|---|---|
| `tasks.md` **2.4** | 21 → **15**, com os arquivos e linhas esperados e a explicação da causa |
| `tasks.md` **6.8** | `--fix` converte **6 dos 12** alvos; as outras 6 (`cli.py:49-53`, `csv_loader.py:19`) vão **à mão**, com a receita de cada uma |
| `requirements.md` **Req. 7.4** | registrado o limite: o linter *cobre* a convenção mas não a *esgota*; a verificação completa do 7.1 é a busca por `.format(` |
| `spec.json` | correção registrada em `notes`, como as anteriores |

O portão P4 (tarefa 6.10) **já** exigia "busca por `.format(` sob `src/` →
zero ocorrências" como item separado do `ruff check` limpo. Nada precisou ser
acrescentado ali: a rede já estava armada, só não se sabia que ela era a
única que pega tudo.

#### Portão P1 fechado — commit

Com o critério 4 corrigido, as cinco verificações passam. E2 está liberada.

---

## E2 — Normalização de fim de linha (Req. 3.8–3.10)

### 3.1 — `.gitattributes` na raiz ✅

**Data:** 18/11/2026
**Requisitos:** 3.8, 3.10

Arquivo criado com os três blocos de `design.md` D-4, na ordem especificada,
sem desvio de conteúdo. 20 linhas, LF, UTF-8.

#### Verificação que importa: o que o git **resolve**, não o que o arquivo diz

Ler o arquivo não prova nada — o que vale é a resolução de atributos. Por
`git check-attr -a`:

| Caminho | Resolvido |
|---|---|
| `src/market_analyzer/cli.py` | `text: set`, `diff: python` |
| `README.md`, `pyproject.toml` | `text: set` |
| `src/market_analyzer/initial_data.csv` | `text: set` |
| `.gitignore`, `.gitattributes` | `text: set` |
| `data/fixtures/amostra.png` | `binary: set` · `text: unset` · `diff: unset` · `merge: unset` |
| `data/raw/video.mp4` | idem |

A macro `binary` expande mesmo para `-text -diff -merge`: é o mecanismo que
o Req. 3.10 pede, e é o que protege as fixtures `.png` — um único byte
trocado por conversão de fim de linha invalidaria o gabarito de OCR em
silêncio.

> Os dois últimos caminhos ainda não existem no disco; `git check-attr`
> resolve sobre a cadeia do caminho, não sobre o arquivo. Nada foi criado
> para fazer esta verificação.

#### `eol` não aparece no arquivo

```
$ grep -c "eol" .gitattributes
0
```

Confirmado o que a tarefa exige: `* text=auto` **sem** `eol=lf`. Forçar LF
na árvore de trabalho contrariaria a letra do critério 3.8, que manda cada
checkout usar o fim de linha nativo — e o ambiente de referência é Windows.

#### Risco verificado: o `.lnk` não está coberto pela lista de binários

O atalho `src/market_analyzer/20261116-1555-54.7150164.mp4.lnk` tem extensão
**`.lnk`**, que **não** consta do bloco de binários de D-4. Ele cai no
`* text=auto` global:

```
$ git check-attr -a <o .lnk>
text: auto
```

Isso só seria perigoso se o git o tratasse como texto na re-normalização da
tarefa 3.2. **Não trata:** o conteúdo começa em `4c 00 00 00 01 14 02 00`, com
NUL já no segundo byte, e o git o classifica como binário por heurística —

```
$ git diff --no-index --stat /dev/null <o .lnk>
 ... | Bin 0 -> 3029 bytes
```

Com `text=auto`, o git só normaliza o que **detecta** como texto. O atalho
passa intacto pela tarefa 3.2.

**Decidido não acrescentar `*.lnk binary` ao arquivo:** seria desvio de D-4
para proteger um arquivo que a tarefa 5.2 apaga em E4, e a proteção já existe
por detecção de conteúdo. Fica registrado para que a ausência não seja lida
como descuido.

#### Estado

```
$ git status --porcelain
?? .gitattributes
```

Nenhum arquivo passou a aparecer como modificado só por existir o
`.gitattributes` — criar o arquivo **não** re-normaliza o que já está no
índice. É exatamente por isso que a tarefa 3.2 existe, e o `--dry-run` do
`git add --renormalize` já confirma que ela alcançaria os 32 arquivos
rastreados.

Sem commit: o `.gitattributes` entra no mesmo commit da re-normalização, como
`design.md` §9 E2 descreve (criar → renormalizar → commitar).

---

### 3.2 — Re-normalização do conteúdo versionado ✅

**Data:** 18/11/2026
**Requisitos:** 3.9
**Commit:** `3458d4b` — `chore: add .gitattributes and renormalize line endings`

#### O commit próprio, como a tarefa exige

A tarefa manda commitar "em commit próprio, sem misturar com qualquer outra
alteração". A árvore tinha o registro da tarefa 3.1 pendente, que **foi
commitado antes**, em `d446d0d`. O commit de E2 ficou com um arquivo só.

#### `git add --renormalize .` não mudou **nada**

```
$ git add .gitattributes && git add --renormalize .
$ git diff --cached --stat
 .gitattributes | 20 ++++++++++++++++++++
 1 file changed, 20 insertions(+)
```

Nenhum arquivo rastreado teve conteúdo alterado. O "diff grande por desenho"
que a tarefa antecipava **não se materializou**, e o motivo importa.

#### Por que foi nulo — e por que isso **não** torna o V-24 inofensivo

O índice já estava em LF. Mas não por decisão do repositório:

```
$ git config --show-origin core.autocrlf
file:C:/Program Files/Git/etc/gitconfig    true
```

O `core.autocrlf=true` vem do **gitconfig de sistema** — é o padrão do Git
for Windows, não configuração deste projeto. Ou seja: a normalização era
propriedade da **instalação do git desta máquina**, não do repositório.

É exatamente o que o critério 3.9 descreve: *"QUANDO o repositório for clonado
em uma máquina com configuração de `core.autocrlf` diferente da atual..."*.
Até aqui, não havia garantia nenhuma — um colaborador com `autocrlf=false` ou
`input` produziria outro resultado, e bastaria um commit com bytes CRLF para
envenenar o índice.

O `.gitattributes` transforma isso em propriedade do repositório. O passo
obrigatório continuou sendo obrigatório: **não dava para saber que era nulo
sem executá-lo**, e o resultado nulo é em si a prova de que o índice estava
íntegro.

#### Efeito colateral esperado, registrado para não assustar depois

Os `.md` estão em **LF no disco** agora, enquanto o índice está em LF e o
`autocrlf=true` manda entregar **CRLF** no checkout. Um clone novo vai
materializá-los em CRLF, com bytes diferentes dos que estão no disco neste
momento. Isso é o comportamento correto do critério 3.8 — "cada checkout usa
o fim de linha nativo" — e o `git status` continua limpo porque o git compara
após normalizar. A verificação por clone é o critério 3.9 e está na tarefa
3.3, com a repetição final na 9.5.

#### Estado logo após o commit

```
$ git status --porcelain
(saída vazia)
```

Primeira das duas verificações do portão de E2, feita no momento certo —
imediatamente após o commit, antes de qualquer outra escrita.

---

### 3.3 — Portão de E2 ✅ **verde**

**Data:** 18/11/2026
**Requisitos:** 3.9, 10.5, 10.6

#### ✅ 1. `git status --porcelain` logo após o commit → vazio

Verificado no momento exato, em `3458d4b`, e registrado na tarefa 3.2. As
únicas pendências da árvore agora são `impl-log.md` e `tasks.md` — o registro
desta própria etapa, não resíduo de re-normalização:

```
 M .sdd/specs/fundacao-projeto/impl-log.md | 70 +
 M .sdd/specs/fundacao-projeto/tasks.md    |  2 +-
```

#### ✅ 2. `pytest` → 10 verdes

```
collected 10 items
tests\test_market_analyzer.py ....   [ 40%]
tests\test_price_ocr.py ....         [ 80%]
tests\test_video_sampler.py ..       [100%]
10 passed in 0.10s
```

Inalterada em relação ao portão P1. A normalização não tocou em
comportamento, como se esperava de uma etapa que não mudou byte nenhum de
conteúdo.

#### ✅ 3. Critério 3.9 provado por clone — o teste que o requisito descreve

As duas verificações acima **não exercitam o critério 3.9**: `git status`
limpo nesta árvore nada diz sobre outra máquina. O critério fala de clone
"em uma máquina com configuração de `core.autocrlf` diferente da atual".
Três clones descartáveis, um por configuração:

| `core.autocrlf` | `README.md` no disco | `git status` |
|---|---|---|
| `false` | **CRLF** (35) | vazio ✅ |
| `input` | **LF** (35) | vazio ✅ |
| `true` | **CRLF** (35) | vazio ✅ |

**Nenhum arquivo aparece modificado sem mudança de conteúdo, nas três.**
Critério 3.9 satisfeito.

Detalhe que confirma o critério 3.8: com `autocrlf=false` o checkout saiu em
**CRLF**, não em LF. Com o atributo `text` ativo, o fim de linha do checkout
passa a ser governado por `core.eol`, que vale `native` por padrão — e nativo
no Windows é CRLF. É literalmente "cada checkout usa o fim de linha nativo da
máquina". O `input` é a exceção coerente: ele manda não converter na saída.

#### ✅ 4. O lado que realmente importava do V-24 — normalização **no commit**

O risco do V-24 nunca foi o checkout; era o **commit**. Com
`core.autocrlf=false`, bytes CRLF entravam no índice e envenenavam o
repositório. Testado dentro do clone `autocrlf=false`:

```
$ printf 'linha um\r\nlinha dois\r\n' > novo.md     # CRLF=2 no disco
$ git add novo.md && git commit -m teste
$ git cat-file -p HEAD:novo.md | od -c
0000000   l i n h a   u m \n l i n h a   d
0000020   o i s \n
```

**O objeto gravado está em LF**, apesar de `autocrlf=false` e de o arquivo
estar em CRLF no disco. O `* text=auto` do `.gitattributes` normaliza na
entrada independentemente da configuração local da máquina.

É o V-24 fechado por demonstração, não por afirmação: a garantia deixou de
ser propriedade da instalação do git e passou a ser propriedade do
repositório.

Os três clones foram apagados após a verificação.

#### E2 encerrada

Portão verde nas quatro verificações. **E3 liberada** (Req. 10.6).

---

## E3 — Dados fora do código e regras de ignorar ancoradas (Req. 2, 3.1–3.7)

### 4.1 — Árvore `data/` na raiz ✅

**Data:** 18/11/2026
**Requisitos:** 2.2

Quatro pastas criadas na raiz, cada uma com um `.gitkeep` vazio (0 byte):

```
data/fixtures/.gitkeep
data/processed/.gitkeep
data/raw/.gitkeep
data/reference/.gitkeep
```

`reference/` recebeu o marcador mesmo indo conter os dois CSVs da tarefa 4.2,
pela decisão da revisão de 18/11: sem ele a pasta existiria apenas enquanto
tivesse conteúdo, e bastaria alguém mover os CSVs para ela evaporar junto. O
marcador torna a garantia do Req. 2.2 estrutural em vez de contingente.

#### Achado: metade dos marcadores está **ignorada** pelas regras atuais

```
$ git status --porcelain
?? data/
```

Parece inofensivo, mas não é. Arquivo a arquivo:

| Marcador | Estado | Regra |
|---|---|---|
| `data/raw/.gitkeep` | **IGNORADO** | `.gitignore:14:data/raw/` |
| `data/processed/.gitkeep` | **IGNORADO** | `.gitignore:15:data/processed/` |
| `data/fixtures/.gitkeep` | livre | — |
| `data/reference/.gitkeep` | livre | — |

**É o V-17 invertendo de polaridade.** As regras `data/raw/` e
`data/processed/` contêm barra no meio, então o git as ancora na pasta do
próprio `.gitignore`, ou seja na **raiz**. Enquanto os dados moravam em
`src/data/processed/`, essas regras não alcançavam nada — era esse o defeito,
e foi por isso que `ocr_samples.csv` acabou versionado. Agora que `data/`
existe de fato na raiz, as mesmas regras passam a alcançar exatamente os
caminhos novos, e excluem a pasta inteira.

Um diretório excluído não admite reinclusão: **nada sob `data/raw/` pode ser
readicionado enquanto a regra for `data/raw/`**, nem com `!`. Por isso a
tarefa 4.3 troca para `/data/raw/*` + `!/data/raw/.gitkeep` — ignorar o
*conteúdo*, nunca a *pasta*.

#### Nada foi forçado para o índice

Seria possível contornar com `git add -f`, e seria errado: o portão P2 existe
para provar que as **regras** deixam os marcadores passarem. Forçá-los agora
faria o portão medir o `-f`, não o `.gitignore`.

A cadeia é: **4.1** cria → **4.3** corrige as regras → **4.5** verifica e
commita. Até lá, `data/raw/` e `data/processed/` permanecem fora do índice, e
o Req. 2.2 ("presentes em um clone limpo mesmo quando vazios") só fica
satisfeito ao fim de E3 — não nesta tarefa.

#### Sem commit

E3 commita uma vez só, no portão P2 (tarefa 4.5), como `design.md` §9 E3
descreve.

---

### 4.2 — Os dois CSVs em `data/reference/` ✅

**Data:** 18/11/2026
**Requisitos:** 2.1, 2.3, 2.4, 2.5

```
$ git mv src/market_analyzer/initial_data.csv data/reference/initial_data.csv
$ git mv src/data/processed/ocr_samples.csv   data/reference/ocr_samples.csv
```

#### Movidos, não copiados — prova em dois níveis

```
$ git diff --cached --name-status --find-renames
R100    src/market_analyzer/initial_data.csv    data/reference/initial_data.csv
R100    src/data/processed/ocr_samples.csv      data/reference/ocr_samples.csv
```

`R100` é 100% de similaridade. Mais forte que isso: **o blob é literalmente o
mesmo objeto** nos dois casos —

| Arquivo | SHA do blob em `HEAD` | SHA no índice |
|---|---|---|
| `initial_data.csv` | `1564a076…` | **`1564a076…`** |
| `ocr_samples.csv` | `bc4e288e…` | **`bc4e288e…`** |

Nenhum byte mudou. A linha de base do CLI (tarefa 2.3) não pode ter sido
afetada pela movimentação — o que o portão P2 vai reconfirmar executando o
CLI pelo caminho novo.

> A verificação por `git log --follow` só é possível **depois** do commit, que
> acontece no portão P2 (tarefa 4.5). Fica anotada para lá.

#### `src/data/` removida

O `git mv` tirou o arquivo mas deixou os diretórios vazios no disco — git não
versiona diretório. Conferido que não sobrara nada (`find src/data -type f` →
0 arquivos, nem ocultos) e removidos `src/data/processed/` e `src/data/` com
`rmdir`, que se recusa a apagar pasta não vazia. `src/` agora contém só o
pacote.

#### `pyproject.toml` não declara nada de dados — confirmado

```
$ grep -niE "package-data|package_data|include-package-data" pyproject.toml
(vazio)
```

Nada foi acrescentado. A separação do Req. 2.1 é feita **tirando os dados de
dentro de `src/`**, não configurando o empacotador para excluí-los — que é
uma solução que depende de alguém lembrar de mantê-la.

#### Os CSVs não estão ignorados no destino

```
$ git check-ignore -v --no-index data/reference/initial_data.csv   → livre
$ git check-ignore -v --no-index data/reference/ocr_samples.csv    → livre
```

Mesmo sob o `.gitignore` **antigo**, que ainda não foi reescrito. Confirma a
previsão da tarefa 1.4: mover antes de corrigir as regras (4.3) não é
armadilha. Req. 2.5 e 3.5 encaminhados; a prova formal é o portão P2.

#### Estado

```
R  src/market_analyzer/initial_data.csv -> data/reference/initial_data.csv
R  src/data/processed/ocr_samples.csv   -> data/reference/ocr_samples.csv
?? data/fixtures/
?? data/reference/.gitkeep
```

`data/raw/.gitkeep` e `data/processed/.gitkeep` continuam **ausentes da lista
por estarem ignorados** — o achado da tarefa 4.1, que a 4.3 resolve. Sem
commit; E3 commita uma vez só no portão P2.

---

### 4.3 — `.gitignore` reescrito com ancoragem na raiz ✅

**Data:** 18/11/2026
**Requisitos:** 3.1, 3.2, 3.3, 3.5, 3.6

Arquivo substituído pelo conteúdo de `design.md` D-5, nos cinco blocos e na
ordem especificada. 37 linhas, CRLF (como o arquivo anterior).

#### Os quatro marcadores foram destravados

O problema da tarefa 4.1 — `data/raw/.gitkeep` e `data/processed/.gitkeep`
ignorados — está resolvido. `git status --porcelain -uall data/`:

```
A  data/reference/initial_data.csv
A  data/reference/ocr_samples.csv
?? data/fixtures/.gitkeep
?? data/processed/.gitkeep      ← antes invisível
?? data/raw/.gitkeep            ← antes invisível
?? data/reference/.gitkeep
```

`/data/raw/*` exclui o **conteúdo** e não a pasta, então a negação
`!/data/raw/.gitkeep` passa a valer — que é exatamente o motivo pelo qual
D-5 escolheu `/*` em vez de `/`.

#### Comportamento verificado com arquivos reais

Criado um `.png` descartável em cada pasta:

| Arquivo | `git status -uall` | `git add --dry-run` |
|---|---|---|
| `data/fixtures/teste.png` | **listado** | `add 'data/fixtures/teste.png'` ✅ |
| `data/raw/teste.png` | **ausente** | recusado: *"paths are ignored by one of your .gitignore files"* ✅ |

A negação `!/data/fixtures/**` vence o `*.png` global porque vem **depois**
dele. Os dois arquivos de teste foram apagados.

---

#### ⚠️ Achado grave: o portão P2 estava escrito sobre uma leitura errada do `git check-ignore`

Ao conferir as regras eu interpretei a saída do `check-ignore` pelo código de
saída, e errei. Medindo:

```
$ git check-ignore -v README.md                      → (nada)        exit=1
$ git check-ignore -v data/raw/teste.png             → /data/raw/*   exit=0
$ git check-ignore -v data/fixtures/teste.png        → !/data/fixtures/**   exit=0
```

> **`git check-ignore -v` sai com código 0 e imprime a regra sempre que
> alguma casa — inclusive quando a regra é uma negação.** Código de saída e
> presença de saída **não** distinguem "ignorado" de "reincluído". Quem
> distingue é o `!` no início do padrão impresso.

Isso contamina três expectativas do portão P2 e um parágrafo do D-5:

| Onde | Dizia | É |
|---|---|---|
| 4.5, fixtures | "não ignorado (saída vazia, código 1)" | imprime `!/data/fixtures/**`, código 0 |
| 4.5, `data/raw/` | "ignorado, com `/data/raw/*` apontada" | **correto** |
| 4.5, `reference` | "não ignorado" | imprime `!/data/reference/**`, código 0 |
| 4.5 e D-5, auditoria do Req. 3.7 | "saída vazia" | **duas linhas** |

A auditoria, rodada exatamente como estava escrita:

```
$ git ls-files | git check-ignore -v --no-index --stdin
.gitignore:37:!/data/reference/**    data/reference/initial_data.csv
.gitignore:37:!/data/reference/**    data/reference/ocr_samples.csv
```

E a tarefa mandava: *"Se algum arquivo aparecer, removê-lo do índice com
`git rm --cached` antes de seguir"*. Seguir isso ao pé da letra **apagaria do
índice os dois CSVs de referência** — violando de uma vez os Req. 2.4, 2.5 e
3.5, que mandam mantê-los versionados. O portão destruiria o que ele existe
para proteger.

#### Correção aplicada

A intenção do Req. 3.7 continua válida: nenhum arquivo rastreado pode estar
ignorado. O que muda é o comando.

```
$ git ls-files | git check-ignore -v --no-index --stdin | grep -v ":!"
(saída vazia)
```

Filtrando as negações — que são justamente as linhas seguras — a auditoria
fica vazia **por mérito**. Só um arquivo casado por regra **sem** `!` é
defeito, e aí sim sai do índice com `git rm --cached`.

Três documentos ajustados:

- **`tasks.md` 4.5** — as três expectativas corrigidas, o `grep -v ":!"`
  acrescentado à auditoria, uma nota de advertência no topo da tarefa, e uma
  **prova independente** por `git status -uall` + `git add --dry-run`, que
  não depende de interpretar o `check-ignore`.
- **`design.md` D-5** — nota no parágrafo "Auditoria do Req. 3.7".
- **`spec.json`** — correção registrada em `notes`.

Nenhum requisito foi alterado: o 3.7 pede que nenhum rastreado esteja
ignorado, e continua pedindo isso. O que estava errado era o instrumento de
medida.

#### Sem commit

E3 commita uma vez só, no portão P2 (tarefa 4.5) — agora com o portão
corrigido.

---

### 4.4 — Caminhos de dados atualizados nos documentos ✅

**Data:** 18/11/2026
**Requisitos:** 2.7

Executada sobre a **lista fechada da tarefa 1.3**, sem nova varredura
exploratória: bloco B (a única instrução) e as anotações de localização do
bloco C. Tarefa puramente documental — nenhum código tocado, nenhum teste a
escrever.

#### B — A instrução, atualizada (1 ocorrência)

`README.md:15`, antes:

```
- `src/data`: dados locais de desenvolvimento; capturas brutas nao devem ser versionadas.
```

Depois (4 linhas, sem acentuação, como o resto do arquivo):

```
- `data`: dados do projeto, na raiz e fora de `src`, em quatro subpastas —
  `data/raw` (videos e frames capturados) e `data/processed` (CSVs gerados
  pelo pipeline) nao sao versionadas; `data/fixtures` (frames rotulados a mao)
  e `data/reference` (series de referencia) sao versionadas.
```

As quatro subpastas aparecem nomeadas, cada uma com o que guarda e se é
versionada — o que o `src/data` anterior não dizia. A afirmação sobre captura
bruta não se perdeu: virou a metade "não versionadas" da frase.

As três falsidades vizinhas do V-15 (`storage` nas linhas 12, `src/tests` na
14, Git na 27) **continuam lá**: são da tarefa 8.1, que reescreve o README
inteiro. A 4.4 corrige só a linha de caminho de dados.

#### C — Narrativa de achado: preservada, com a localização atual ao lado

Régua do A-2 aplicada nas seis linhas do inventário. O caminho antigo
permanece intacto como evidência; a anotação vem depois dele, entre
`*(hoje em ...)*`.

| Achado | Caminho preservado | Anotação acrescentada |
|---|---|---|
| **V-06** | `initial_data.csv` | `data/reference/initial_data.csv` |
| **V-06** | `src/data/processed/ocr_samples.csv` | `data/reference/ocr_samples.csv` |
| **V-16** | `initial_data.csv` | `data/reference/initial_data.csv` |
| **V-16** | `src/data/` | `data/` na raiz |
| **V-17** | `o/data/...` | `data/` na raiz |
| **V-17** | `o/src/data/processed/` | `data/reference/` |

Os três parágrafos foram requebrados para acomodar as anotações dentro da
largura do arquivo. Nenhuma palavra do texto original foi removida ou
reescrita — em particular, o tempo verbal continua no presente ("está",
"contêm"), porque **dar baixa nos achados é a tarefa 9.1**, não esta. As
linhas deslocaram: V-06 passou de 122–123 para 122–125, V-16 de 232–233 para
234–236 e V-17 de 239–240 para 242–244.

#### O que foi deliberadamente deixado em paz

| Alvo | Por quê | Dono |
|---|---|---|
| V-14, V-15, V-18, V-19 e as linhas 326, 391, 443 de `validacao-inicial.md` | narrativa sem caminho de dados a anotar; falta a baixa | 9.1 |
| `.sdd/steering/structure.md` (4 linhas) | tabela de pendências, baixa dos achados | 9.2 |
| Resto do `README.md` | reescrita completa | 8.1 |
| `tasks.md:119`, `design.md:886`, `tasks.md:190-191` | instrução operacional que roda **antes** da movimentação de E3; atualizar quebraria a tarefa que a contém | ninguém — ficam como estão |

#### Verificação

Varredura do 1.3 reexecutada nos dois arquivos editados:

```
$ grep -nE 'market_analyser|src/data|initial_data\.csv|(^|[^A-Za-z0-9_.-])o/' README.md
(saída vazia)
```

`README.md` ficou **sem nenhuma** das quatro cadeias — o Req. 2.7 está
satisfeito do lado da instrução. Em `validacao-inicial.md` as cadeias
permanecem, por desenho (A-2), e as **sete** linhas restantes (218, 221, 229,
252, 326, 391 e 443, ex-216, 219, 227, 248, 322, 387 e 439) são exatamente as
do inventário previstas para 9.1 — nenhuma delas é instrução.

#### Sem commit

E3 commita uma vez só, no portão P2 (tarefa 4.5).

---

### 4.5 — Portão P2 ✅ **verde**

**Data:** 18/11/2026
**Requisitos:** 2.1, 2.5, 2.6, 3.4, 3.5, 3.7, 10.5, 10.6

Executado já com a correção de 18/11/2026 incorporada ao `tasks.md`: o que
distingue "ignorado" de "reincluído" é o **`!` no início do padrão impresso**,
nunca o código de saída nem a presença de saída. As oito verificações
passaram de primeira; nenhuma remediação foi necessária.

> **Desvio deliberado de procedimento.** O `tasks.md` manda *mover* o `.png`
> de teste de `fixtures/` para `raw/`, mas a prova independente do mesmo item
> exige "os dois arquivos de teste no lugar". Em vez de mover, o arquivo foi
> **copiado**, de modo que os dois existissem ao mesmo tempo. As duas
> verificações de `check-ignore` saem idênticas e a prova independente fica
> exercitável.

#### ✅ 1. `data/fixtures/teste.png` — casado por **negação**, logo não ignorado

```
$ printf 'png-descartavel\n' > data/fixtures/teste.png
$ git check-ignore -v data/fixtures/teste.png
.gitignore:35:!/data/fixtures/**	data/fixtures/teste.png
exit=0
```

Linha, número e texto da regra batem com o esperado: `.gitignore:35` e
`!/data/fixtures/**`. O `!` inicial é a prova — **não ignorado**, apesar de
`*.png` estar na lista de mídia global (Req. 3.3).

#### ✅ 2. `data/raw/teste.png` — casado por regra **sem** `!`, logo ignorado

```
$ cp data/fixtures/teste.png data/raw/teste.png
$ git check-ignore -v data/raw/teste.png
.gitignore:28:/data/raw/*	data/raw/teste.png
exit=0
```

Regra `/data/raw/*`, **sem** negação: ignorado. Mesmo código de saída do item
1 e mesma presença de saída — a diferença está só no `!`, exatamente como a
correção previa.

#### ✅ 3. Prova independente do critério 3.4 — sem interpretar o `check-ignore`

```
$ git status --porcelain -uall data/
A  data/reference/initial_data.csv
A  data/reference/ocr_samples.csv
?? data/fixtures/.gitkeep
?? data/fixtures/teste.png
?? data/processed/.gitkeep
?? data/raw/.gitkeep
?? data/reference/.gitkeep
```

Com os **dois** arquivos de teste no disco, o `status` lista
`data/fixtures/teste.png` e **não** lista `data/raw/teste.png`. Os quatro
`.gitkeep` aparecem, inclusive os de `raw/` e `processed/`, o que confirma de
quebra as exceções `!/data/raw/.gitkeep` e `!/data/processed/.gitkeep`.

```
$ git add --dry-run data/raw/teste.png
The following paths are ignored by one of your .gitignore files:
data/raw/teste.png
hint: Use -f if you really want to add them.
exit=1

$ git add --dry-run data/fixtures/teste.png
add 'data/fixtures/teste.png'
exit=0
```

Recusa de um lado, aceitação do outro. É esta a verificação do critério 3.4,
e ela não depende de ler padrão nenhum. Os dois arquivos de teste foram
apagados em seguida — o `--dry-run` não chegou a mexer no índice.

#### ✅ 4. `data/reference/` fora do alcance das regras de dados (Req. 3.5)

```
$ git check-ignore -v --no-index data/reference/ocr_samples.csv
.gitignore:37:!/data/reference/**	data/reference/ocr_samples.csv
exit=0

$ git check-ignore -v --no-index data/reference/initial_data.csv
.gitignore:37:!/data/reference/**	data/reference/initial_data.csv
exit=0
```

Negação nos dois: **não ignorados**. O `--no-index` é indispensável, e o
contraste mostra por quê:

```
$ git check-ignore -v data/reference/ocr_samples.csv     # sem --no-index
exit=1
```

Sem a opção o git simplesmente se cala sobre arquivo já rastreado, e a
verificação não provaria nada — o silêncio seria o mesmo de um caminho que
não casa com regra alguma.

#### ✅ 5. Auditoria do conjunto rastreado (Req. 3.7) — saída vazia

```
$ git ls-files | git check-ignore -v --no-index --stdin | grep -v ":!"
(saída vazia)
```

A saída **sem** o filtro mostra o que o `grep -v ":!"` descarta, e por que ele
é obrigatório:

```
$ git ls-files | git check-ignore -v --no-index --stdin
.gitignore:37:!/data/reference/**	data/reference/initial_data.csv
.gitignore:37:!/data/reference/**	data/reference/ocr_samples.csv
```

As duas únicas linhas são **negações** — os arquivos seguros, que os
Req. 2.4, 2.5 e 3.5 mandam manter versionados. Sem o filtro, a auditoria os
acusaria e induziria a um `git rm --cached` que **violaria** esses três
critérios. Nenhum arquivo rastreado casa com regra sem `!`, portanto **zero
defeitos**:

| Medida | Valor |
|---|---|
| arquivos rastreados | 34 |
| casados por alguma regra, descontadas as negações | **0** |

Corroboração que não depende do filtro: o `check-ignore` **sem `-v`** lista
apenas o que de fato está ignorado, e as negações nem aparecem.

```
$ git ls-files | git check-ignore --no-index --stdin | wc -l
0
```

#### ✅ 6. Nenhum arquivo de dado sob `src/` (Req. 2.1, 2.5)

```
$ git ls-files src | sed 's/.*\.//' | sort | uniq -c
      1 lnk
     14 py
```

Extensões reais dos 15 rastreados em `src/`: **nenhum `.csv`, `.png`, `.mp4`
ou congênere**. No disco idem — `find src -type f` filtrando essas extensões
devolve saída vazia.

> **O `.lnk` não é falso negativo.** O único não-`.py` é
> `src/market_analyzer/20261116-1555-54.7150164.mp4.lnk` (3 029 bytes). O
> nome **contém** `.mp4`, mas a extensão é `.lnk`: um atalho do Windows, que
> guarda um caminho e não dado. Ele é o V-04, endereçado nominalmente pelo
> **Req. 6.1** e removido na tarefa 5.2 — a etapa seguinte. Sua presença aqui
> é prevista pelo sequenciamento (P2 antes de E4), não uma falha deste
> portão.

Lado da distribuição (Req. 2.5), reconferido:

```
$ grep -nEi "package-data|include-package-data" pyproject.toml
(nenhuma ocorrência)
```

A separação continua sendo feita **tirando os dados de dentro de `src/`**,
não por configuração de empacotamento.

#### ✅ 7. CLI no novo caminho, idêntico à linha de base da tarefa 2.3

```
$ ./.venv/Scripts/market-analyzer.exe --input data/reference/initial_data.csv
Item: Algodão de isolamento acústico
Samples: 20
Minimum: 110037
Maximum: 220074
Mean: 154691.55
Median: 140745.00
Simulated trades: 2
Simulated profit: 179130.00
```

Oito de oito contra a tabela da 2.3, inclusive o mínimo 110037 e o máximo
220074 que o critério 2.6 nomeia. A comparação foi feita **byte a byte**
contra o artefato guardado em
`C:\Users\yjovencio\AppData\Local\Temp\baseline-cli.txt`, não a olho:

```
baseline sem BOM   sha256: d377fed2…5de15ccb
saída desta tarefa sha256: d377fed2…5de15ccb
BYTES IDENTICOS: True
```

O BOM descontado é o `EF BB BF` que o `Out-File -Encoding utf8` do PowerShell
acrescentou ao capturar a linha de base; o conteúdo, CRLF incluído, é o mesmo
objeto de 176 − 3 = 173 bytes.

> **Ressalva de encoding — o V-21 reaparece, e é da etapa E6.** A captura
> desta tarefa saiu de um executor cujo stdout é um *pipe*, não um console.
> Nessa condição o Python escolhe a página de código ANSI da máquina e
> escreveu `Algod\xE3o` em **cp1252**, enquanto a linha de base de 2.3 saiu em
> UTF-8 de um console em `chcp 65001`. Uma comparação de bytes crua acusaria
> diferença que **não é de comportamento**. Duas verificações foram feitas, e
> as duas fecham:
>
> 1. decodificando cada captura na sua própria codificação (cp1252 aqui,
>    `utf-8-sig` lá), o **texto** é idêntico nas 8 linhas;
> 2. com `PYTHONIOENCODING=utf-8` forçado, a saída é **byte a byte idêntica**
>    à linha de base sem BOM — o SHA-256 acima.
>
> Forçar `chcp 65001` do lado do PowerShell **não** resolve: o filho continua
> sem console e segue emitindo cp1252, e o pai passa a decodificar como UTF-8,
> produzindo `Algod\uFFFDo`. Mais uma confirmação do que a 2.3 já registrara:
> a verificação do Req. 11 vai precisar olhar os **bytes** que o processo
> escreve, não o texto redecodificado pelo terminal. Nada em `cli.py` foi
> tocado até aqui — o V-21 continua **em aberto**, para E6.

#### ✅ 8. Suíte — 10 verdes

```
platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0
configfile: pyproject.toml
testpaths: tests
collected 10 items

tests\test_market_analyzer.py ....    [ 40%]
tests\test_price_ocr.py ....          [ 80%]
tests\test_video_sampler.py ..        [100%]

10 passed in 0.15s
```

Inalterada desde P1 e desde o portão de E2. Mover os CSVs não quebrou nenhum
teste porque nenhum deles os lia por caminho: os dois são insumo de inspeção
manual, não fixture de suíte.

#### Estado da árvore no momento do commit

```
$ git status --porcelain -uall
 M .gitignore
 M .sdd/specs/fundacao-projeto/design.md
 M .sdd/specs/fundacao-projeto/impl-log.md
 M .sdd/specs/fundacao-projeto/spec.json
 M .sdd/specs/fundacao-projeto/tasks.md
 M README.md
R  src/market_analyzer/initial_data.csv -> data/reference/initial_data.csv
R  src/data/processed/ocr_samples.csv -> data/reference/ocr_samples.csv
 M validacao-inicial.md
?? data/fixtures/.gitkeep
?? data/processed/.gitkeep
?? data/raw/.gitkeep
?? data/reference/.gitkeep
```

Os dois CSVs entram como **`R` (renomeação)**, não como par
adição + exclusão — é o critério 10.4 preservado, e o que faz
`git log --follow` continuar alcançando o histórico deles.

Nenhum dos quatro `.gitkeep` precisou de `git add -f`: os de `raw/` e
`processed/` são reincluídos pelas negações das linhas 29 e 31, e os de
`fixtures/` e `reference/` nunca chegam a ser alcançados por regra de
ignorar. O `.png` de teste não aparece em lugar nenhum — foi apagado antes do
commit.

**Nenhum `git rm --cached` foi executado nesta tarefa, em caminho algum.**

#### E3 encerrada

Portão verde nas oito verificações. **E4 liberada** (Req. 10.6).

---

## E4 — Remoção de artefatos obsoletos (Req. 6)

### 5.1 — Nenhuma referência a `market_analyser` a corrigir ✅

**Data:** 18/11/2026
**Requisitos:** 6.4

Tarefa de **verificação**, não de alteração: o Req. 6.4 é condicional ("SE
algum módulo, teste ou documento referenciar `market_analyser`, ENTÃO a
referência DEVE ser corrigida... antes da exclusão"). Nada de runtime muda
aqui, logo **nenhum teste foi escrito** — não há comportamento novo a cobrir.
Se a varredura tivesse achado referência em código, aí sim o ciclo test-first
valeria; não achou.

A varredura da tarefa 1.3 foi **reexecutada do zero**, e não apenas citada: a
árvore mudou desde então (E1, E2 e E3 commitadas; CSVs em `data/reference/`,
`.gitignore` reescrito). Três passagens independentes, cada uma mais larga que
a anterior.

#### 1 — Código, testes e configuração: zero

```
$ git grep -nI 'market_analyser' -- src tests pyproject.toml .gitignore .gitattributes
(saída vazia, exit 1)
```

Sem ocorrência nem com `-i` (`analyser` em qualquer caixa) sob `src` e
`tests`. O achado da 1.3 **se mantém**.

#### 2 — Árvore versionada inteira: 21 linhas, nenhuma é instrução

| Onde | Linhas | Classificação |
|---|---:|---|
| `.sdd/specs/fundacao-projeto/` (`design.md` 4, `impl-log.md` 8, `requirements.md` 4, `tasks.md` 3) | 19 | documento de plano → **não tocar** |
| `.sdd/steering/structure.md:107` | 1 | narrativa de achado (V-19) → preservar |
| `validacao-inicial.md:252` | 1 | narrativa de achado (V-19) → preservar |

As 8 linhas do `impl-log.md` são a contagem **antes** desta entrada, que
naturalmente acrescenta outras.

Fora da spec restam **duas** ocorrências, uma por arquivo, e as duas são o
mesmo achado V-19:

- `validacao-inicial.md:252` — título `#### 🔵 V-19 · market_analyser.py é
  dívida sem motivo`. Descreve o defeito; não manda ninguém usar o módulo.
- `.sdd/steering/structure.md:107` — linha do V-19 na tabela "Pendências
  estruturais", cuja coluna *Correção prevista* diz "Remover". É a instrução
  **de apagar**, que continua correta até a tarefa 5.2 executá-la.

Nenhuma das duas recebe anotação de localização: a régua do A-2 anota *onde a
coisa está hoje* para caminho que **se moveu**, e o shim não se move — é
apagado. A baixa das duas linhas é das tarefas **9.1** e **9.2** (E8), onde já
estava prevista, não desta.

> **Deslocamento desde a 1.3:** o V-19 de `validacao-inicial.md` passou da
> linha **248** para a **252**, empurrado pelas anotações que a tarefa 4.4
> acrescentou ao V-06, V-16 e V-17. `structure.md:107` não se moveu. O
> inventário da 1.3 permanece válido; só os números mudaram.

#### 3 — Disco inteiro, binários inclusive: dois artefatos gerados

Passagem mais larga que a da 1.3, que só olhou arquivos **versionados**. Com
`grep -ra` sobre tudo exceto `.git/` e `.venv/`, aparecem dois caminhos que o
`git grep` não enxerga:

| Caminho | Situação | Veredito |
|---|---|---|
| `src/market_analyzer.egg-info/SOURCES.txt:5` | não rastreado; ignorado por `.gitignore:4` (`*.egg-info/`) | metadado de build, regenerado na próxima instalação |
| `.ruff_cache/0.17.5/` (2 arquivos) | não rastreados; ignorados por `.gitignore:7` | cache binário do linter |

Nenhum dos dois é módulo, teste ou documento — são **saída de ferramenta**,
reconstruída a cada execução. Não são alvo do Req. 6.4 e não foram tocados.
Ficam registrados porque explicam por que a 1.3 relatava cinco ocorrências de
documento e esta tarefa relata duas: as listas não divergem, as varreduras é
que têm alcances diferentes.

#### 4 — O shim não se referencia, e o ponto de entrada não passa por ele

```
$ cat src/market_analyzer/market_analyser.py
"""Backward-compatible entry point for the previous filename."""

from market_analyzer.cli import main


if __name__ == "__main__":
    main()
```

Três fatos que a tarefa 5.2 herda prontos:

1. O corpo do shim **não contém** a cadeia `market_analyser` — importa
   `market_analyzer.cli`, a grafia correta. Apagá-lo não deixa referência
   órfã.
2. `pyproject.toml:24` declara
   `market-analyzer = "market_analyzer.cli:main"` e
   `entry_points.txt` instalado repete
   `market-analyzer = market_analyzer.cli:main`. O console script **não
   atravessa** o shim — o Req. 6.5 está garantido por desenho, antes mesmo da
   remoção.
3. O atalho `src/market_analyzer/20261116-1555-54.7150164.mp4.lnk` (3029
   bytes) não contém a cadeia nem em ASCII nem em UTF-16LE — verificado byte a
   byte, já que `grep -I` o trataria como binário e o pularia.

#### 5 — Suíte intacta

```
$ .venv/Scripts/python.exe -m pytest -q
..........                                     [100%]
10 passed in 0.14s
```

Esperado: nada foi alterado. Serve de linha de base imediata para o portão P3,
que exige as mesmas 10 verdes **depois** das duas exclusões.

#### Resultado

**Nada a corrigir.** O Req. 6.4 está satisfeito por vacuidade: a premissa "SE
algum módulo, teste ou documento referenciar `market_analyser`" é falsa para
módulo e teste, e os dois documentos que citam o nome são narrativa de achado
que o A-2 manda preservar. Nenhum arquivo foi editado nesta tarefa além deste
diário e da marcação em `tasks.md`.

**Tarefa 5.2 liberada, sem impedimento.** Única consequência a lembrar lá: o
`SOURCES.txt` do `egg-info` continuará listando o shim até a próxima
instalação editável, sem efeito sobre o console script.

---

### 5.2 — Atalho `.lnk` e shim de grafia britânica removidos ✅

**Data:** 18/11/2026
**Requisitos:** 6.1, 6.2

Duas exclusões, um `git rm` cada:

```
git rm "src/market_analyzer/20261116-1555-54.7150164.mp4.lnk"
git rm src/market_analyzer/market_analyser.py
```

As exclusões foram executadas na sessão do desenvolvedor, fora do executor.
Esta entrada registra a **verificação do efeito**, não a digitação dos
comandos.

#### Efeito conferido nos dois planos que o Req. 6.1 exige juntos

| Plano | Verificação | Resultado |
|---|---|---|
| Disco | `ls src/market_analyzer/` | nenhum dos dois presente |
| Índice | `git status --porcelain` | `D ` para ambos — deleção já no índice |
| Árvore inteira | `git ls-files \| grep -E '\.lnk\|market_analyser'` | saída vazia |

O `D` com espaço à direita é a assinatura do `git rm`: a deleção está
**staged**, não apenas no working tree. Fosse ` D`, o arquivo teria sido
apagado só do disco e o índice continuaria a rastreá-lo — meio caminho que o
Req. 6.1 não aceita.

#### O atalho era de fato irrecuperável — resolvido antes de apagar

O Req. 6.1 justifica a remoção dizendo que o atalho "aponta para pasta
temporária do Windows, não é portável e não resolve". A premissa foi
verificada empiricamente antes da exclusão, via `WScript.Shell`:

```
TargetPath  : ...\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState\Recordings\
              20261116-1555-54.7150164.mp4
Existe alvo?: False
```

Três confirmações de uma vez: é gravação da Ferramenta de Captura do Windows;
mora em `TempState`, temporária por definição; e **o alvo já não existia**.
Além disso, o `WorkingDirectory` apontava para um perfil de usuário diferente
do da máquina atual — o atalho veio de outro perfil, coerente com o fluxo em
que as capturas são produzidas fora da máquina de desenvolvimento. Apagar não
destruiu nenhum caminho de acesso a dado: não havia caminho.

#### Resultado

Req. 6.1 e 6.2 satisfeitos. Nenhum arquivo além dos dois foi tocado — o commit
da etapa (adiante) contém exatamente duas deleções e nada mais.

---

### 5.3 — Portão P3: obsoletos fora e ponto de entrada intacto ✅

**Data:** 18/11/2026
**Requisitos:** 6.1, 6.3, 6.5, 10.5, 10.6

#### As quatro verificações do portão

```
$ git ls-files | grep -E '\.lnk|market_analyser'
(saída vazia)                                        → Req. 6.3 ✅

$ .venv/Scripts/market-analyzer --help
usage: market-analyzer [-h] [--version] --input INPUT ...
                                                     → Req. 6.5 ✅

$ .venv/Scripts/python -m pytest -q
..........                            [100%]
10 passed in 1.25s                                   → Req. 10.5 ✅

$ .venv/Scripts/python -c "import market_analyzer.market_analyser"
ModuleNotFoundError: No module named
  'market_analyzer.market_analyser'                  → remoção efetiva ✅
```

A quarta não está na redação do portão e foi acrescentada: `git ls-files`
prova que o git não rastreia mais o shim, mas não prova que o **intérprete**
deixou de encontrá-lo. Com instalação editável, um `.py` órfão no disco
continuaria importável sem aparecer no índice. O `ModuleNotFoundError` fecha
essa brecha.

O Req. 6.5 confirma na prática o que a tarefa 5.1 já havia estabelecido por
desenho: o console script declara `market_analyzer.cli:main` e nunca
atravessou o shim, então a remoção não tinha como quebrá-lo. A verificação é
barata e vale como rede.

#### Commit da etapa

`1e8e256` — `refactor: remove wrong files`, contendo exatamente:

```
src/market_analyzer/20261116-1555-54.7150164.mp4.lnk | Bin 3029 -> 0 bytes
src/market_analyzer/market_analyser.py               |   8 --------
2 files changed, 8 deletions(-)
```

Veio de `--amend` sobre `1fd204f`, que havia sido publicado com a mensagem
`fix: remove wrong files` — trocada por `refactor:`, já que nada estava
quebrado em funcionamento. Consequência operacional: `main` ficou
`ahead 1, behind 1` de `origin/main` e exige `push --force-with-lease` para
reconciliar.

#### Divergência de ordem, registrada por honestidade

A redação do portão manda commitar **ao fim** das verificações, com o diário
já escrito. Na prática o commit do código veio primeiro e este registro
depois, em commit separado. As evidências acima foram todas coletadas **antes**
do commit `1e8e256`, não reconstruídas a posteriori — mas quem ler o histórico
verá o código sair num commit e a baixa documental em outro. Sem efeito sobre
os requisitos; anotado para não parecer lapso.

#### Resultado

**Etapa E4 encerrada.** Requisito 6 integralmente satisfeito: 6.1 e 6.2 pela
remoção, 6.3 pela ausência no índice, 6.4 por vacuidade (tarefa 5.1) e 6.5
pelo `--help` vivo. Próxima etapa: **E5**, tarefa 6.1.
