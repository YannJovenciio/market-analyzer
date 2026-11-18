# Tarefas de implementação — fundacao-projeto

> **Fase: tarefas geradas.** Aguardando revisão humana.
> Esta lista traduz a **sequência E0–E8 de `design.md` §9** em passos
> executáveis. A ordem **não é preferência**: os Requisitos 10.1 a 10.3
> proíbem alteração de sintaxe antes de rede de teste verificada. Não
> reordene, não funda etapas e não pule portões.

## Como usar

- Execute na ordem numérica. Cada grupo maior corresponde a uma etapa do
  design (E0 a E8) e termina em uma **tarefa de portão**, com comando e
  resultado esperado explícitos.
- **Portão reprovado bloqueia a etapa seguinte.** Se qualquer etapa deixar a
  suíte vermelha, corrija ou reverta antes de seguir (Req. 10.6).
- Ambiente de referência: **Windows + PowerShell**, a partir da raiz do
  repositório (`market-analyzer/`), com o venv ativado a partir da tarefa 2.2.
- **Nada aqui envia commits para o remoto.** A chave SSH não está configurada
  neste ambiente; todos os portões rodam localmente.

### Legenda

| Marcador | Significado |
|---|---|
| `- [ ]` | Tarefa obrigatória, sequencial |
| `- [ ] (P)` | Pode ser executada em paralelo com as outras `(P)` do mesmo bloco |
| `- [ ]*` | Cobertura de teste adiável para depois do MVP desta spec |

### Linha de base de regressão (invariante de ponta a ponta)

Comparada nos portões P2, P4 e no portão de E6:

```text
Item: Algodão de isolamento acústico
Samples: 20   Minimum: 110037   Maximum: 220074
Mean: 154691.55   Median: 140745.00
Simulated trades: 2   Simulated profit: 179130.00
```

### Já satisfeito antes desta lista — não há tarefa

- **Critérios 1.1 a 1.6** — o achatamento foi executado e commitado
  (`47d5603`); `o/` não existe. Resta apenas o 1.7, coberto pelas tarefas 1.3
  e 9.2.
- **`data/reference/` no `structure.md`** e **contagem de 74 critérios nos
  metadados** — ajustados na aprovação do design (A-3, A-8).
- **`tests/support.py`** — deliberadamente **não** criado nesta spec (A-7). O
  Req. 5.4 é satisfeito por desenho; a verificação está na tarefa 2.4.

---

## 1. E0 — Auditoria e congelamento (nada é alterado)

Etapa somente de leitura. Produz os inventários que as etapas E3, E5 e E8
consomem.

- [x] **1.1 Partir de árvore de trabalho limpa e confirmar a preservação do histórico**
  - Commitar as edições de documentação pendentes (ou guardá-las em stash), até
    `git status --porcelain` devolver **saída vazia**.
  - Rodar `git log --follow -- README.md` (ou outro arquivo movido no
    achatamento) e confirmar que a saída **alcança o commit `35fdcc9`**.
  - Registrar no diário da etapa que o critério 10.4 foi cumprido **no efeito**
    (movimentação fora do git + detecção de renomeação em `47d5603`), conforme
    `design.md` §11, A-1. Não há ação corretiva.
  - _Requisitos: 1.3, 10.4, 10.5_

- [x] **1.2 (P) Inventariar as chamadas a `str.format()`**
  - Buscar `.format(` sob `src/` e anotar arquivo e linha de cada ocorrência.
  - Resultado esperado: **21 ocorrências em 5 arquivos** — `cli.py` (9),
    `csv_loader.py` (3), `ocr_batch.py` (5), `price_ocr.py` (1),
    `video_sampler.py` (3). Divergência na contagem interrompe a etapa até ser
    explicada.
  - _Requisitos: 7.1_

- [x] **1.3 (P) Varrer os documentos versionados em busca de caminhos obsoletos**
  - Buscar, em todos os arquivos versionados, as cadeias `o/`, `src/data`,
    `src/market_analyzer/initial_data.csv` e `market_analyser`.
  - Classificar cada ocorrência em **instrução** (atualizar) ou **narrativa de
    achado** (preservar e anotar a localização atual ao lado).
  - Entregar a lista fechada, que é o insumo das tarefas 4.4, 5.1 e do grupo 9.
  - _Requisitos: 1.7, 2.7, 6.4_

- [x] **1.4 (P) Listar os arquivos rastreados como insumo da auditoria de ignorar**
  - Salvar a saída de `git ls-files` fora do repositório (p. ex. em `%TEMP%`),
    para não criar arquivo não rastreado.
  - Essa lista é comparada contra as novas regras de ignorar na tarefa 4.5.
  - _Requisitos: 3.7_

---

## 2. E1 — Ambiente instalável (Req. 4; habilita o Req. 5)

Nenhuma alteração de sintaxe acontece nesta etapa nem em qualquer etapa
anterior ao portão P1.

- [x] **2.1 Ampliar o `pyproject.toml` com grupo `dev`, pytest e ruff**
  - Acrescentar `[project.optional-dependencies]` com `dev = ["pytest>=9.0",
    "ruff>=0.17"]`.
  - Acrescentar `[tool.pytest.ini_options]` com `minversion = "9.0"`,
    `testpaths = ["tests"]` e `addopts = ["-ra"]` — o `-ra` é o que faz o
    motivo de cada *skip* aparecer na saída.
  - Acrescentar `[tool.ruff.lint]` com `select = ["E4", "E7", "E9", "F",
    "UP032"]`.
  - **Não** declarar `pythonpath` (mascararia uma instalação quebrada), **não**
    declarar `target-version` (o ruff o infere de `requires-python`) e
    **preservar** `requires-python = ">=3.10"`.
  - _Requisitos: 4.2, 4.3, 5.3, 7.2_

- [x] **2.2 Criar o ambiente virtual e instalar o projeto em modo editável**
  - `python -m venv .venv`
  - `.\.venv\Scripts\Activate.ps1` — se a política de execução do PowerShell
    bloquear, seguir sem ativação usando `.\.venv\Scripts\python.exe` e
    `.\.venv\Scripts\pytest.exe`.
  - `python -m pip install -e ".[dev]"` — as aspas são obrigatórias.
  - Anotar os dois desvios acima; eles precisam constar do README na tarefa 8.1.
  - _Requisitos: 4.1, 4.3_

- [x] **2.3 Capturar a linha de base do CLI com os caminhos ainda antigos**
  - `market-analyzer --input src/market_analyzer/initial_data.csv`
  - Salvar a saída **fora do repositório** (p. ex. `%TEMP%\baseline-cli.txt`).
  - Conferir contra o bloco de linha de base no topo deste documento: 20
    amostras, mínimo 110037, máximo 220074.
  - _Requisitos: 2.6, 7.6_

- [x] **2.4 Portão P1 — suíte verde, CLI instalado e regra do linter provada ativa**
  - `pytest` → **10 testes, 0 falhas, 0 erros de coleta**. A subida de 8 para
    10 é `tests/test_video_sampler.py` passando a executar seus 2 casos.
  - Confirmar na mesma execução que **o binário do Tesseract continua ausente**
    e ainda assim a suíte conclui sem nenhuma falha (Req. 5.4, satisfeito por
    desenho — ver A-7).
  - `market-analyzer --help` → termina sem erro.
  - `ruff check .` → **exatamente 15 violações `UP032`**, com arquivo e linha,
    nos 5 arquivos conhecidos: `cli.py` (4: 48, 54, 55, 57), `csv_loader.py`
    (2: 10, 37), `ocr_batch.py` (5), `price_ocr.py` (1), `video_sampler.py`
    (3). Este é o estado **correto** nesta etapa: é a prova de que a regra
    está ativa de fato, e não apenas declarada.
  - **Correção de 18/11/2026, verificada em execução.** Esta tarefa pedia 21,
    herdando a contagem de `grep` da tarefa 1.2 e supondo cobertura total do
    `UP032`. A regra **não reporta chamada a `.format()` cujo argumento
    contenha literal de string** — em qualquer `target-version`, e mesmo sem
    conflito de aspas. As 6 não reportadas são `cli.py:49-53`
    (`stats["count"]`, `stats["minimum"]`, `stats["maximum"]`,
    `stats["mean"]`, `stats["median"]`) e `csv_loader.py:19`
    (`", ".join(...)`). 21 − 6 = 15. Consequência: o linter cobre a
    convenção, mas não a esgota — ver Req. 7.4 e a tarefa 6.8.
  - `git status --porcelain` → só as alterações intencionais do
    `pyproject.toml` (`.venv/` ainda aparecerá até a reescrita do `.gitignore`
    em 4.3; não commitá-lo).
  - Commitar.
  - **Portão bloqueante: enquanto este portão não estiver verde, nenhuma tarefa
    do grupo 6 pode ser iniciada.**
  - _Requisitos: 4.7, 5.1, 5.2, 5.4, 5.5, 7.2, 7.4, 10.1, 10.5_

---

## 3. E2 — Normalização de fim de linha (Req. 3.8–3.10)

Etapa isolada de propósito: re-normalização misturada a movimentação de
arquivos produz um diff ilegível e atrapalha a detecção de renomeação de E3.

- [ ] **3.1 Criar o `.gitattributes` na raiz**
  - Três blocos, nesta ordem: `* text=auto`; tipos de texto declarados
    (`*.py text diff=python`, `*.md`, `*.toml`, `*.csv`, `*.txt`, `.gitignore`,
    `.gitattributes`); binários (`*.png`, `*.jpg`, `*.jpeg`, `*.mp4`, `*.avi`,
    `*.mov` marcados como `binary`).
  - **Sem `eol=lf`**: forçar LF na árvore de trabalho contraria a letra do
    critério 3.8, que manda cada checkout usar o fim de linha nativo.
  - _Requisitos: 3.8, 3.10_

- [ ] **3.2 Re-normalizar o conteúdo já versionado**
  - `git add --renormalize .` — passo **obrigatório**: criar o
    `.gitattributes` não re-normaliza o que já está no índice, e sem ele o
    critério 3.9 não fica garantido.
  - Commitar em commit próprio, sem misturar com qualquer outra alteração. O
    diff será grande por desenho.
  - _Requisitos: 3.9_

- [ ] **3.3 Portão de E2 — árvore estável e suíte intacta**
  - `git status --porcelain` logo após o commit → **saída vazia**.
  - `pytest` → ainda **10 testes, 0 falhas**.
  - _Requisitos: 3.9, 10.5, 10.6_

---

## 4. E3 — Dados fora do código e regras de ignorar ancoradas (Req. 2, 3.1–3.7)

- [ ] **4.1 Criar a árvore `data/` na raiz**
  - Criar `data/raw/`, `data/processed/`, `data/fixtures/` e `data/reference/`.
  - Criar `.gitkeep` nas **quatro** pastas, para que todas existam em um clone
    limpo mesmo vazias.
  - *Decidido na revisão de 18/11/2026:* `reference/` recebe `.gitkeep` embora
    vá conter os dois CSVs da tarefa 4.2. O Req. 2.2 exige presença em clone
    limpo **"mesmo quando vazios"** — sem o marcador, a pasta existiria apenas
    enquanto tivesse conteúdo, e bastaria alguém mover os CSVs para ela
    evaporar junto. Um arquivo vazio torna a garantia estrutural em vez de
    contingente, e deixa a regra uniforme nas quatro.
  - _Requisitos: 2.2_

- [ ] **4.2 Mover os dois CSVs para `data/reference/` preservando o histórico**
  - `git mv src/market_analyzer/initial_data.csv data/reference/initial_data.csv`
  - `git mv src/data/processed/ocr_samples.csv data/reference/ocr_samples.csv`
  - Remover `src/data/`, agora vazia.
  - Confirmar que `pyproject.toml` **não** declara `package-data` nem
    `include-package-data` — nada deve ser acrescentado; a separação é feita
    tirando os dados de dentro de `src/`.
  - _Requisitos: 2.1, 2.3, 2.4, 2.5_

- [ ] **4.3 Reescrever o `.gitignore` com ancoragem na raiz e exceções por negação**
  - Blocos: ambiente e ferramenta (`__pycache__/`, `*.py[cod]`, `*.egg-info/`,
    `.venv/`, `.pytest_cache/`, `.ruff_cache/`); editor e logs; mídia global
    (`*.mp4`, `*.avi`, `*.mov`, `*.png`, `*.jpg`, `*.jpeg`).
  - Dados: `/data/raw/*` + `!/data/raw/.gitkeep` e `/data/processed/*` +
    `!/data/processed/.gitkeep`. **Ignorar o conteúdo (`/*`), nunca a pasta** —
    o git não reinclui nada sob um diretório excluído, e as pastas precisam
    existir no clone.
  - Exceções deliberadas, obrigatoriamente **depois** das regras acima:
    `!/data/fixtures/**` e `!/data/reference/**`.
  - _Requisitos: 3.1, 3.2, 3.3, 3.5, 3.6_

- [ ] **4.4 Atualizar nos documentos os caminhos de dados que servem de instrução**
  - Usar a lista fechada da tarefa 1.3: toda ocorrência classificada como
    **instrução** passa a apontar `data/reference/...`.
  - Em `validacao-inicial.md`, as ocorrências que **descrevem um achado**
    (V-06, V-16, V-17) permanecem como evidência, recebendo ao lado a
    localização atual — p. ex. `src/data/processed/ocr_samples.csv` *(hoje em
    `data/reference/ocr_samples.csv`)*.
  - _Requisitos: 2.7_

- [ ] **4.5 Portão P2 — ignorar verificado arquivo a arquivo e CLI na linha de base**
  - Criar um `.png` descartável em `data/fixtures/`:
    `git check-ignore -v data\fixtures\teste.png` → **não ignorado** (saída
    vazia, código de saída 1).
  - Mover o mesmo arquivo para `data/raw/`:
    `git check-ignore -v data\raw\teste.png` → **ignorado**, com a regra
    `/data/raw/*` apontada na saída. Apagar o arquivo de teste depois da
    verificação.
  - `git check-ignore -v --no-index data/reference/ocr_samples.csv` → **não
    ignorado**. O `--no-index` é necessário: sem ele, o git nunca reporta
    arquivo já rastreado e a verificação não prova nada.
  - Auditoria do conjunto rastreado:
    `git ls-files | git check-ignore -v --no-index --stdin` → **saída vazia**.
    Se algum arquivo aparecer, removê-lo do índice com `git rm --cached` antes
    de seguir.
  - `git ls-files src` → **nenhum arquivo com extensão de dado** (`.csv`,
    `.png`, `.mp4` e congêneres).
  - `market-analyzer --input data/reference/initial_data.csv` → saída
    **idêntica** à capturada na tarefa 2.3.
  - `pytest` → 10 verdes. Commitar.
  - _Requisitos: 2.1, 2.5, 2.6, 3.4, 3.5, 3.7, 10.5, 10.6_

---

## 5. E4 — Remoção de artefatos obsoletos (Req. 6)

- [ ] **5.1 Corrigir qualquer referência remanescente a `market_analyser` antes de apagar**
  - Partir da varredura da tarefa 1.3. Cada ocorrência em módulo, teste ou
    documento é corrigida para `market_analyzer.cli` ou removida.
  - Esta verificação acontece **antes** da exclusão, não depois.
  - _Requisitos: 6.4_

- [ ] **5.2 Remover o atalho `.lnk` e o shim de grafia britânica**
  - `git rm "src/market_analyzer/20261116-1555-54.7150164.mp4.lnk"`
  - `git rm src/market_analyzer/market_analyser.py`
  - `git rm` tira do índice e do disco em uma operação só, que é o que os
    critérios 6.1 e 6.3 pedem juntos.
  - _Requisitos: 6.1, 6.2_

- [ ] **5.3 Portão P3 — obsoletos fora e ponto de entrada intacto**
  - `git ls-files` → **não lista** nenhum dos dois arquivos; nenhum dos dois
    está no disco.
  - `market-analyzer --help` → funciona; o entry point
    `market-analyzer = "market_analyzer.cli:main"` não referenciava o shim.
  - `pytest` → 10 verdes. Commitar.
  - _Requisitos: 6.1, 6.3, 6.5, 10.5, 10.6_

---

## 6. E5 — Contrato do nome de frame e migração para f-string (Req. 7, 8)

**A subordem deste grupo é parte do design.** Dois pontos não negociáveis:
`video_sampler.py` só é tocado na tarefa 6.5, já com seus testes rodando
(Req. 10.3), e `ruff check --fix` só roda na tarefa 6.7 — aplicá-lo antes
converteria o template-contrato em f-string inline e desfaria a extração.

- [ ] **6.1 Confirmar a pré-condição de entrada em E5**
  - O portão P1 (tarefa 2.4) está verde.
  - `pytest tests/test_video_sampler.py -v` → o módulo **coleta e executa**
    seus casos, e eles passam. Enquanto isso não for verdade, nenhuma tarefa
    deste grupo pode começar, e em especial `video_sampler.py` não pode ser
    alterado.
  - _Requisitos: 10.1, 10.2, 10.3_

- [ ] **6.2 Criar `src/market_analyzer/ingestion/frame_naming.py`**
  - Única definição do formato, com `FRAME_GLOB: Final[str] = "frame_*.png"`,
    `frame_name(seconds: float) -> str`, `frame_seconds(path: Path) -> float` e
    `sort_frames(paths: Iterable[Path]) -> list[Path]`.
  - `frame_name` escreve o nome como **f-string normal** —
    `f"frame_{seconds:06.1f}s.png"` — e levanta `ValueError` contendo o valor
    recebido se `seconds` for negativo ou não finito.
  - `frame_seconds` reconhece `^frame_(\d{4,}\.\d)s\.png$`, ancorado nas duas
    pontas, e levanta `ValueError` contendo o nome recebido fora do contrato.
  - `sort_frames` é **pura**: ordena por `frame_seconds`, não varre diretório e
    propaga o `ValueError` de um nome intruso em vez de ignorá-lo.
  - Importar **apenas** biblioteca padrão (`pathlib`, `re`, `typing`). Nada de
    `domain`, nada de terceiros. Identificadores e docstrings em inglês.
  - _Requisitos: 7.5, 8.1, 8.6_

- [ ] **6.3 Criar `tests/test_frame_naming.py` e vê-lo passar antes de mexer em consumidor**
  - Ida-e-volta `frame_seconds(Path(frame_name(t))) == float(f"{t:.1f}")` para
    `t` em 0, 10, 9999.9 e 10000.0.
  - Formato exato: `frame_name(10.0) == "frame_0010.0s.png"`.
  - Nome fora do contrato → `ValueError` **com o nome na mensagem**.
  - `seconds` negativo → `ValueError`.
  - `sort_frames` com `frame_10000.0s.png` e `frame_9999.9s.png` devolve
    `9999.9` **primeiro** — ordenação numérica, não lexicográfica.
  - Testes puros: sem disco, sem rede, sem Tesseract. Se algum caso vier a
    precisar de escrita, usar `tempfile.TemporaryDirectory()`.
  - `pytest` → os casos novos passam **antes** de qualquer consumidor mudar.
  - _Requisitos: 5.7, 8.3, 8.4, 8.5_

- [ ] **6.4 Criar `src/market_analyzer/ingestion/dependencies.py`**
  - `require_pytesseract() -> ModuleType` e
    `require_imageio_ffmpeg() -> ModuleType`: importam **dentro da função** e,
    em falha, levantam `RuntimeError` encadeado (`raise ... from error`)
    nomeando a distribuição ausente e o comando de instalação.
  - `TESSERACT_NOT_FOUND_MESSAGE: Final[str]`: texto único que identifica o
    Tesseract como **pré-requisito externo não instalável por pip** e aponta a
    seção "Pré-requisitos" do `README.md`. **Sem URL na mensagem** — a URL vive
    no README.
  - O módulo não imprime, não encerra processo e **não checa o PATH
    preventivamente**: a detecção do binário ausente continua vindo do
    `TesseractNotFoundError`, no ponto onde a falha realmente ocorre.
  - _Requisitos: 4.4, 4.5_

- [ ] **6.5 Reescrever `ocr_batch.py` (leitor) sobre `frame_naming`**
  - Apagar a constante `FRAME_TIMESTAMP` e o `frame_seconds()` local.
  - `glob("frame_*.png")` → `glob(FRAME_GLOB)`; `sorted(..., key=frame_seconds)`
    → `sort_frames(...)`.
  - Converter os 5 `.format()` deste arquivo em f-string.
  - Ao fim: nenhum literal de formato de frame e nenhuma expressão regular de
    nome de frame restam no arquivo. `ocr_batch` **não** passa a importar
    `video_sampler`.
  - `pytest` → verde.
  - _Requisitos: 7.1, 8.2, 8.5_

- [ ] **6.6 Reescrever `video_sampler.py` (escritor) — só aqui, e já com rede de teste**
  - `import imageio_ffmpeg` do topo → `require_imageio_ffmpeg()` dentro de
    `sample_video()`.
  - Nome do frame via `frame_name()`, removendo o literal do formato.
  - Converter os 3 `.format()` deste arquivo em f-string.
  - Preservar a assinatura pública de `sample_video`.
  - `pytest` → verde, **incluindo** os casos de `test_video_sampler.py`.
  - _Requisitos: 4.5, 5.1, 7.1, 8.2_

- [ ] **6.7 Fazer `price_ocr.py` usar `dependencies`**
  - `import pytesseract` inline → `require_pytesseract()`.
  - A mensagem do Tesseract ausente passa a vir de
    `TESSERACT_NOT_FOUND_MESSAGE`, encadeada sobre
    `pytesseract.TesseractNotFoundError`.
  - Converter o 1 `.format()` deste arquivo em f-string. Preservar a assinatura
    de `read_price`. Nenhum `print` nem `sys.exit` entra em função de núcleo.
  - `pytest` → verde.
  - _Requisitos: 4.4, 4.5, 7.1_

- [ ] **6.8 Converter os `.format()` restantes, só agora com `ruff check --fix`**
  - Alvos restantes: `csv_loader.py` (3) e `cli.py` (9).
  - `ruff check --fix .` — **esta tarefa não pode ser antecipada**: rodada antes
    da tarefa 6.6, a ferramenta transformaria o template-contrato em f-string
    inline e desfaria a extração do `frame_naming`.
  - **O `--fix` converte 6 dos 12 alvos**, não os 12: `csv_loader.py` 10 e 37,
    e `cli.py` 48, 54, 55 e 57. O `UP032` não reporta — e portanto não
    conserta — chamada cujo argumento contenha literal de string (verificado
    na tarefa 2.4).
  - **Converter à mão as 6 restantes:** `cli.py:49, 50, 51, 52, 53` e
    `csv_loader.py:19`. Em `cli.py` usar aspas simples internas
    (`f"Samples: {stats['count']}"`), válido no piso 3.10. Em
    `csv_loader.py` extrair o `", ".join(sorted(missing))` para uma
    variável antes da f-string. **Nenhum comando do portão P4 acusa se alguma
    for esquecida, exceto a busca por `.format(`** — ela é a verificação
    completa do critério 7.1, não o `ruff check` limpo.
  - Revisar o diff **item a item**.
  - Nenhum `# noqa` é introduzido: a exceção do template-contrato foi resolvida
    por extração de função.
  - _Requisitos: 7.1, 7.4, 7.5_

- [ ]* **6.9 Cobertura adicional de `dependencies.py`** *(adiável pós-MVP)*
  - Testes para `require_pytesseract()` e `require_imageio_ffmpeg()`
    verificando que a ausência da distribuição vira `RuntimeError` encadeado
    com o nome e o comando de instalação na mensagem. Exige simular a ausência,
    já que ambas são dependências obrigatórias do projeto.
  - _Requisitos: 4.5_

- [ ] **6.10 Portão P4 — linter limpo, contrato único e comportamento inalterado**
  - `ruff check .` → **nenhuma violação**.
  - Busca por `.format(` sob `src/` → **zero ocorrências**.
  - Busca por `# noqa` em todo o repositório → **zero ocorrências**.
  - Busca por literal de formato de frame ou regex de nome de frame em
    `video_sampler.py` e `ocr_batch.py` → **zero ocorrências**.
  - Conferir a regra de dependência: `frame_naming` e `dependencies` importam
    só biblioteca padrão; `domain` continua sem importar nada; nenhuma camada
    importa `cli`.
  - `pytest` → ≈15 verdes, nenhum falhando, acima da linha de base de 8.
  - `market-analyzer --input data/reference/initial_data.csv` → **idêntico** à
    linha de base da tarefa 2.3. Commitar.
  - _Requisitos: 7.1, 7.3, 7.5, 7.6, 8.1, 8.2, 8.6, 10.5, 10.6_

---

## 7. E6 — Encoding da saída na borda (Req. 11)

- [ ] **7.1 Acrescentar `configure_output_encoding()` a `cli.py`**
  - Assinatura: `configure_output_encoding(streams: Iterable[TextIO] | None =
    None) -> None`; o padrão é `(sys.stdout, sys.stderr)`. O parâmetro existe
    para testabilidade.
  - Reconfigura cada fluxo para `encoding="utf-8"` e
    `errors="backslashreplace"`. Se o fluxo não expuser `reconfigure`, a função
    **não faz nada e não levanta**.
  - Chamada como **primeira linha** de `cli.main()`.
  - **Nada de `chcp`, `ctypes`, `PYTHONUTF8` ou `PYTHONIOENCODING`**: o programa
    configura o fluxo dele, nunca o terminal do usuário.
  - Alcance restrito ao `cli` principal por decisão A-5: os `main()` de
    `video_sampler`, `price_ocr` e `ocr_batch` **não** chamam a função —
    importá-la de `cli` seria importar para cima.
  - _Requisitos: 11.1, 11.2, 11.4_

- [ ] **7.2 Criar `tests/test_cli.py`**
  - Caso mínimo: `configure_output_encoding` recebendo um fluxo **sem**
    `reconfigure` não levanta exceção — prova que a degradação é silenciosa e
    não quebra o CLI.
  - _Requisitos: 5.7, 11.2, 11.4_

- [ ] **7.3 Portão de E6 — acentuação correta e números intactos**
  - Em console real: `market-analyzer --input data/reference/initial_data.csv`
    imprime `Algodão de isolamento acústico`, sem nenhum `?` no lugar de letra
    acentuada.
  - Redirecionado para arquivo: o conteúdo abre legível em UTF-8, com
    acentuação preservada.
  - Todos os números **idênticos** à linha de base. A **única** diferença
    admitida em relação ao portão P4 é a acentuação do nome do item passar a
    sair correta.
  - `pytest` → verde. Commitar.
  - _Requisitos: 7.6, 11.1, 11.3, 11.4_

---

## 8. E7 — README fiel ao projeto (Req. 9)

- [ ] **8.1 Reescrever o `README.md` nas onze seções da ordem de execução**
  - 1 O que é (pipeline offline de observação, Fase 1, limite do método
    declarado) · 2 Pré-requisitos (Python 3.10+ e, **em bloco separado do
    pip**, o binário do Tesseract, com link do instalador de Windows e
    `tesseract --version`) · 3 Instalação (venv, ativação,
    `python -m pip install -e ".[dev]"`, `market-analyzer --help`, mais a
    alternativa sem ativação anotada na tarefa 2.2) · 4 Suíte de testes
    (`pytest`) · 5 Linter (`ruff check .`) · 6 Exemplo real de CLI
    (`market-analyzer --input data/reference/initial_data.csv`, com a saída
    esperada transcrita) · 7 Estrutura de pastas · 8 Dados · 9 Comportamento de
    acentuação · 10 Git · 11 Documentos.
  - A estrutura de pastas da seção 7 deve bater **pasta a pasta** com a
    estrutura de destino de `structure.md` e com o disco, incluindo
    `data/reference/`.
  - A seção 8 explicita que `raw/` e `processed/` não são versionadas e que
    `fixtures/` e `reference/` são versionadas **por exceção deliberada**.
  - A seção 9 documenta a degradação `\uXXXX` para caractere irrepresentável.
  - **Sumir do documento:** `src/market_analyzer/storage`, `src/tests`, a
    afirmação de que o projeto não usa Git e qualquer menção a `src/data`.
  - _Requisitos: 2.7, 4.6, 5.6, 7.7, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6_

- [ ] **8.2 Executar o README literalmente, do início ao fim, em ambiente zerado**
  - Apagar `.venv/`, abrir um **PowerShell novo** na raiz e executar cada
    comando do documento exatamente como está escrito, sem recorrer a nada fora
    dele — exceto o download do instalador do Tesseract (bloqueio humano H-6).
  - Resultado esperado: suíte verde, `ruff check .` limpo e CLI executável
    reproduzindo a linha de base.
  - **Qualquer comando que exija ajuste é defeito do README**, não do operador:
    corrigir o documento e repetir a execução do zero. Commitar.
  - _Requisitos: 4.1, 4.7, 9.7, 9.8_

---

## 9. E8 — Fechamento documental (Req. 1.7, restrição transversal 5)

As três atualizações de documento abaixo tocam arquivos distintos e não
dependem umas das outras.

- [ ] **9.1 (P) Atualizar `validacao-inicial.md`**
  - Marcar V-04, V-13 a V-21 e V-24 como resolvidos no registro de alterações.
  - **Preservar** os caminhos `o/` e `src/data/` que são evidência de achado
    (V-06, V-16, V-17), acrescentando a cada um a localização atual ao lado.
  - _Requisitos: 1.7, 2.7_

- [ ] **9.2 (P) Atualizar `structure.md`**
  - Mover V-04, V-14 a V-17 e V-19 de "Pendências estruturais" para resolvidos.
  - Confirmar que nenhum caminho `o/` remanescente serve de instrução — pela
    varredura da tarefa 1.3, o único ajuste pendente é a baixa do V-14.
  - `data/reference/` já consta da estrutura de destino (A-3); nada a
    acrescentar ali.
  - _Requisitos: 1.7_

- [ ] **9.3 (P) Atualizar `tech.md`**
  - Marcar V-20 e V-21 como resolvidos nas pendências técnicas.
  - Registrar `pytest` como executor e `ruff` como linter na seção de stack e
    na seção de testes, substituindo a afirmação de que não há pytest, linter
    nem CI.
  - _Requisitos: 1.7_

- [ ] **9.4 Atualizar o `spec.json` conforme o fluxo SDD**
  - Fases e `ready_for_implementation` ajustados ao estado de conclusão da
    implementação.
  - _Requisitos: 10.5_

- [ ] **9.5 Portão final — tudo reexecutado a partir de um clone limpo**
  - `git clone . $env:TEMP\ma-verificacao` e, dentro do clone,
    `git status --porcelain` → **saída vazia** logo após o clone, sem arquivo
    aparecendo modificado sem mudança de conteúdo.
  - Instalar seguindo o README do clone, do zero.
  - `pytest` → verde. `ruff check .` → limpo.
  - `market-analyzer --input data/reference/initial_data.csv` → linha de base,
    com a acentuação correta.
  - `git ls-files | git check-ignore -v --no-index --stdin` → saída vazia.
  - Apagar o clone depois da verificação.
  - _Requisitos: 3.9, 9.8, 10.5, 10.6_

---

## Cobertura de requisitos

| Requisito | Critérios | Tarefas |
|---|---|---|
| 1 — Achatamento | 1.1–1.6 | ✅ já satisfeitos antes desta lista |
| 1 | 1.3, 1.7 | 1.1, 1.3, 9.1, 9.2, 9.3 |
| 2 — Dados fora do código | 2.1–2.7 | 4.1, 4.2, 4.3, 4.4, 4.5, 8.1, 9.1 |
| 3 — Versionamento | 3.1–3.7 | 4.3, 4.5 |
| 3 | 3.8–3.10 | 3.1, 3.2, 3.3, 9.5 |
| 4 — Ambiente | 4.1–4.3, 4.7 | 2.1, 2.2, 2.4, 5.3, 8.2 |
| 4 | 4.4–4.6 | 6.4, 6.7, 8.1 |
| 5 — Suíte de testes | 5.1–5.7 | 2.1, 2.4, 6.3, 7.2, 8.1 |
| 6 — Obsoletos | 6.1–6.5 | 5.1, 5.2, 5.3 |
| 7 — f-string e linter | 7.1–7.7 | 2.1, 2.4, 6.5, 6.6, 6.7, 6.8, 6.10, 7.3, 8.1 |
| 8 — Nome de frame | 8.1–8.6 | 6.2, 6.3, 6.5, 6.6, 6.10 |
| 9 — README | 9.1–9.8 | 8.1, 8.2, 9.5 |
| 10 — Ordem segura | 10.1–10.6 | 1.1, 2.4, 6.1 e todas as tarefas de portão |
| 11 — Encoding | 11.1–11.4 | 7.1, 7.2, 7.3 |
| Transversal 1 — camadas | — | 6.2, 6.4, 6.10 |
| Transversal 2 — comportamento | — | 2.3, 4.5, 6.10, 7.3 |
| Transversal 3 — idioma | — | 6.2, 6.4, 8.1 |
| Transversal 4 — Windows, piso 3.10 | — | 2.1, 2.2, 8.2 |
| Transversal 5 — registro vivo | — | 9.1 |

## Fora do escopo desta lista

Reafirmado para não voltar como sugestão durante a implementação: CI, Docker,
verificador de tipos, `ruff format`, reescrita dos testes `unittest` para
estilo pytest, reorganização de camadas, qualquer mudança em pré-processamento
de imagem, padrão de preço, estatística ou simulador, conteúdo das fixtures
(V-02), decodificação integral do vídeo (V-22) e envio dos commits para
`origin` — este último depende de chave SSH não configurada neste ambiente.
