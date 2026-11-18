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

`.venv/` já é coberto pela regra existente do `.gitignore`, e a instalação
editável moderna não deixa `egg-info` na árvore do projeto. Nada a limpar
antes do P1 (Req. 10.5).

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
