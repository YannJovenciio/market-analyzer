# Validação inicial do projeto — Market Analyzer

> Documento-guia. Registra o estado real do projeto em **18/11/2026**, antes de
> qualquer correção. Serve de base para as especificações SDD
> (`.sdd/specs/`) e deve ser atualizado conforme os itens forem resolvidos.

---

## 1. Propósito

O projeto lê dados do mercado de um jogo a partir de gravações de tela, extrai
os preços por OCR, armazena a série histórica e analisa quando um item está
barato o suficiente para valer a compra.

Hoje ele é um **pipeline offline de observação**, não um agente autônomo:

```text
vídeo (.mp4)
   └─ video_sampler ─→ frames PNG
                          └─ price_ocr ─→ ocr_batch ─→ CSV
                                                        └─ csv_loader ─→ statistics
                                                                           └─ simulator ─→ cli
```

---

## 2. O que está certo

Vale registrar, porque é a base sobre a qual as correções vão ser feitas:

- **Separação em camadas correta.** `domain` / `ingestion` / `analysis` /
  `backtesting` / `cli`. Nenhuma camada importa para cima.
- **Domínio puro.** `MarketSample` e `BacktestTrade` são dataclasses
  congeladas, sem dependência de I/O.
- **Simulador sem efeito colateral.** `simulator.run()` é função pura,
  fácil de testar e de substituir.
- **Cada módulo de ingestão tem CLI própria** (`build_parser` / `main`),
  o que permite rodar as etapas isoladamente.
- **Análise inicial documentada** em `analise-inicial.md`, incluindo as
  limitações do método. Isso é raro e é um bom hábito.

---

## 3. Estado do ambiente (verificado)

| Item | Estado |
|---|---|
| Python | ✅ 3.12.10 (`C:\Program Files\Python312`) |
| Pillow | ✅ 13.0.0 |
| numpy | ✅ 2.5.4 |
| `pytesseract` | ❌ ausente |
| `imageio_ffmpeg` | ❌ ausente |
| **Tesseract (binário externo)** | ❌ não instalado |
| `pip install -e .` | ❌ nunca executado |
| Testes | ⚠️ 8 passam, 1 módulo não importa |
| Git | ✅ 1 commit (`35fdcc9 start repo`) |
| `.sdd/` | ❌ não existe |

Saída real do CLI com os dados atuais:

```text
Samples: 20   Minimum: 110037   Maximum: 220074
Mean: 154691.55   Median: 140745.00
Simulated trades: 2   Simulated profit: 179130.00
```

---

## 4. Achados

Severidade: 🔴 crítico · 🟡 médio · 🔵 baixo

### Grupo A — Dados e captura

#### 🔴 V-01 · Não existe material bruto no computador

O vídeo `Variação market 2026-11-16 125917.mp4` **não existe em lugar nenhum**
do perfil do usuário. O atalho versionado
(`20261116-1555-54.7150164.mp4.lnk`) aponta para:

```text
AppData\Local\Packages\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState\Recordings\
```

Essa é a pasta **temporária** da Ferramenta de Captura do Windows — o sistema
a limpa sozinho. Não há nenhum `frame_*.png` salvo.

**Impacto:** bloqueia qualquer trabalho de calibração e validação de OCR.
**Ação:** gravar novo material salvando **fora** da pasta temporária.

#### 🔴 V-02 · Não existem fixtures de imagem

Sem frames com o valor verdadeiro anotado à mão, não existe teste de regressão
de OCR possível. Qualquer mudança no pré-processamento é um tiro no escuro.

**Ação:** criar um conjunto de 10–20 frames rotulados, versionados
(exceção explícita no `.gitignore`).

#### 🟡 V-03 · Região de recorte fixa no código

`price_ocr.py:73` e `ocr_batch.py:79` trazem `(1410, 755, 1545, 805)` como
padrão. Isso amarra o projeto a uma resolução, um tema de UI e um layout de
janela específicos — nenhum deles documentado.

#### 🟡 V-04 · Atalho `.lnk` versionado

Um atalho do Windows apontando para uma pasta temporária foi commitado.
Não é portável, não resolve e não deveria estar no git.

#### 🟡 V-05 · O recorte pode mudar de significado em silêncio

`analise-inicial.md` registra que a tela mostra **duas** linhas de valor
(preço unitário e total). Com quantidade 1 elas coincidem. Se a quantidade
mudar, o mesmo recorte passa a ler outro número — sem erro, sem aviso.

---

### Grupo B — Confiabilidade do OCR

#### 🔴 V-06 · O OCR já erra em 25% das amostras

Comparação entre `initial_data.csv` (transcrição manual) e
`src/data/processed/ocr_samples.csv` (saída da máquina):

| Linha | Manual | OCR | Erro |
|---|---:|---:|---|
| 6, 10, 17 | 140.745 | 140.74**6** | 5 → 6 |
| 11, 12 | 110.037 | 110.0**8**7 | 3 → 8 |

**5 de 20 divergem.** O `3 → 8` é falha clássica de binarização agressiva:
`price_ocr.py:36` usa limiar fixo (`255 if pixel > 110 else 0`), que fecha o
vão do dígito `3`.

#### 🔴 V-07 · Nenhuma leitura é verificada

O pipeline grava o que o OCR devolver, sem nenhuma defesa:

- não usa `image_to_data`, então **ignora a confiança** reportada pelo Tesseract;
- não valida faixa plausível de preço;
- não compara com a amostra anterior para detectar salto absurdo;
- `PRICE_PATTERN` (`price_ocr.py:8`) aceita `\b\d{6,9}\b`, então um total lido
  no lugar do unitário passa batido;
- `parse_price` pode casar **parcialmente** um texto ruidoso e devolver um
  número errado em vez de levantar erro.

**Princípio a adotar:** é melhor **falhar alto** do que gravar `110.087` calado.

#### 🟡 V-08 · Cobertura de testes desigual

| Módulo | Cobertura |
|---|---|
| `statistics`, `simulator` | ✅ razoável |
| `csv_loader` | ⚠️ só o caminho feliz |
| `parse_price` | ⚠️ 4 casos, nenhum com ruído real |
| `prepare_price_region`, `read_price` | ❌ nenhuma |
| `ocr_batch` | ❌ nenhuma |

Além disso, `tests/test_video_sampler.py` **não importa** por falta de
`imageio_ffmpeg` — ou seja, hoje ele nunca roda.

---

### Grupo C — Modelo de domínio e análise

#### 🔴 V-09 · O backtest produz um número que não significa nada

`Simulated profit: 179130.00` é ficção, por três motivos somados:

1. **Compra pelo preço médio.** Quem compra no mercado compra a **menor
   oferta**, não a média. Esse campo nem existe no modelo.
2. **Liquidez infinita.** `simulator.run()` assume que sempre há alguém
   vendendo naquele preço, naquele instante, na quantidade desejada.
3. **Parâmetros sobreajustados.** `buy_below=130000` / `sell_at=190000`
   (`cli.py:19,25`) vieram das hipóteses do `analise-inicial.md`, derivadas de
   **20 amostras de 3 minutos**. Qualquer limiar escolhido assim acerta no
   passado e erra no futuro.

#### 🔴 V-10 · O domínio modela uma fração do que a análise exige

`analise-inicial.md` lista o que precisa ser coletado. Confronto com
`domain/models.py`:

| Campo necessário | Existe? |
|---|---|
| preço unitário médio | ✅ |
| menor oferta | ❌ |
| maior oferta / faixa superior | ❌ |
| quantidade disponível | ⚠️ campo existe, nunca preenchido |
| taxa / comissão | ❌ |
| preço líquido | ❌ |
| tempo até a venda | ❌ |
| servidor / região / canal | ❌ |

#### 🟡 V-11 · Estatísticas abaixo do que o próprio plano pede

`statistics.summary()` entrega contagem, mínimo, máximo, média e mediana.
O plano pede **percentis, volatilidade e tempo em cada faixa** — nenhum existe.
Sem percentis não há como derivar limiares dos dados (ver V-09.3).

#### 🟡 V-12 · Taxa aplicada nas duas pontas

`simulator.py:22` cobra `fee_rate` sobre compra **e** venda. Na maioria dos
mercados de jogo apenas a venda é taxada.
**Pendente:** confirmar a regra real do jogo antes de calibrar qualquer coisa.

---

### Grupo D — Estrutura e ambiente

#### 🔴 V-13 · Ambiente não instalado

`pytesseract`, `imageio_ffmpeg` e o **binário do Tesseract** estão ausentes.
O Tesseract é um programa externo que o `pip` não instala — e o README não
menciona esse pré-requisito.

#### 🟡 V-14 · A pasta `o/`

O repositório git está em `market-analyzer/`, mas todo o conteúdo está em
`market-analyzer/o/`. Parece erro de digitação em um comando. Não há razão
para esse nível a mais.

#### 🟡 V-15 · README desatualizado em três pontos

| Afirma | Realidade |
|---|---|
| `src/market_analyzer/storage` | não existe |
| testes em `src/tests` | estão em `o/tests` |
| "não depende de um repositório Git" | já tem git, 1 commit |

#### 🟡 V-16 · Dados misturados com código

`initial_data.csv` está **dentro do pacote Python**
(`src/market_analyzer/`), e `src/data/` está dentro da pasta de distribuição
do setuptools (`where = ["src"]`). Dados não pertencem a `src/`.

#### 🟡 V-17 · `.gitignore` não faz o que pretende

As regras `data/raw/` e `data/processed/` contêm barra no meio, então o git as
ancora na pasta do próprio `.gitignore` → `o/data/...`. O caminho real é
`o/src/data/processed/`. Por isso `ocr_samples.csv` foi versionado apesar da
regra existir.

#### 🟡 V-18 · `.sdd/` não existe

O `CLAUDE.md` define o fluxo Spec-Driven (steering → requirements → design →
tasks → implementação), mas ele nunca foi inicializado neste projeto.

#### 🔵 V-19 · `market_analyser.py` é dívida sem motivo

Shim de compatibilidade com a grafia britânica, num projeto com **1 commit**.
Não há histórico para preservar.

#### 🔵 V-20 · Sem ferramentas de desenvolvimento

Não há `[project.optional-dependencies]`, pytest, linter, formatador nem CI.

#### 🔵 V-21 · Acentos quebram no console

A saída do CLI sai como `Algod?o de isolamento ac?stico` no terminal do
Windows (cp1252).

#### 🔵 V-22 · `video_sampler` decodifica o vídeo inteiro

Para pegar 1 frame a cada 10 s, percorre todos os frames sequencialmente e
carrega cada um na memória. Tolerável nesta escala, ineficiente em volume.

#### 🟡 V-24 · Sem `.gitattributes`, quebras de linha não normalizadas

Descoberto em 18/11/2026, ao simular o commit do achatamento. O git avisou em
7 arquivos:

```text
warning: LF will be replaced by CRLF the next time Git touches it
```

Não existe `.gitattributes` no repositório, então a conversão de fim de linha
fica a cargo da configuração local de cada máquina (`core.autocrlf`).

**Por que importa aqui:** em uma máquina Windows só, é inofensivo. Mas **o jogo
está em outra máquina** (ver H-1), e qualquer sessão de trabalho fora deste
ambiente — ou em Linux — produziria *diffs fantasma*: arquivos marcados como
modificados sem que ninguém tenha editado uma linha.

**Correção:** `.gitattributes` com `* text=auto` normaliza LF no repositório e
deixa cada checkout usar o fim de linha nativo. Incluído no escopo de
`fundacao-projeto`.

---

### Grupo E — Escopo e risco

#### ✅ V-23 · Escopo definido: duas fases (decidido em 18/11/2026)

| Fase | Escopo | Estado |
|---|---|---|
| **Fase 1 — Observador** | Capturar, ler por OCR, registrar, analisar e **recomendar**. A execução fica com o humano. | 🚧 em andamento |
| **Fase 2 — Executor** | Dar ao programa a capacidade de executar a compra. | ⏸️ adiada até a Fase 1 estar confiável |

**Por que faseado:** a Fase 1 concentra todo o trabalho difícil e todo o valor
— ler a tela com confiabilidade, modelar menor oferta e quantidade, derivar
limiares dos dados e ter um backtest que não minta. Executar é a parte trivial
depois disso. O caminho inverso produziria um bot executando decisões que
ainda não se sabe se são boas.

**Consequência arquitetural (vale para todas as specs da Fase 1):**
manter uma **fronteira explícita entre decidir e executar**. O núcleo produz
uma *recomendação* como dado; quem a consome é um adaptador na borda. Assim a
Fase 2 vira um adaptador novo e não uma reescrita — mesmo desenho que o README
já prevê para a futura GUI.

**Risco reconhecido:** fasear **adia** a questão de termos de serviço da
Fase 2, não a elimina. A decisão de entrar na Fase 2 deve ser retomada
explicitamente quando chegar a hora, não herdada por inércia.

---

## 5. Resumo por prioridade

| # | ID | Achado | Sev. | Bloqueado por |
|---|---|---|---|---|
| 1 | V-13 | Ambiente não instalado | 🔴 | — |
| 2 | V-14, 15, 16, 17 | Estrutura: pasta `o/`, README, dados em `src/`, gitignore | 🟡 | — |
| 3 | V-18 | Inicializar SDD | 🟡 | — |
| 4 | V-23 | ~~Definir escopo (observador × executor)~~ **decidido: 2 fases** | ✅ | — |
| 5 | V-01 | Gravar material novo | 🔴 | ação humana |
| 6 | V-02 | Criar fixtures rotuladas | 🔴 | V-01 |
| 7 | V-06, 07 | Endurecer o OCR | 🔴 | V-02 |
| 8 | V-10 | Expandir o modelo de domínio | 🔴 | V-01 |
| 9 | V-11 | Percentis e volatilidade | 🟡 | V-10 |
| 10 | V-09, 12 | Refazer o simulador | 🔴 | V-10 |
| 11 | V-08, 20 | Testes e ferramental | 🟡 | — |
| 12 | V-03, 04, 05, 19, 21, 22 | Ajustes menores | 🔵 | — |

**Trabalho que não depende das gravações:** itens 1, 2, 3, 11 e boa parte do 12.
Pode começar hoje.

---

## 6. Especificações SDD sugeridas

Divisão proposta, com as dependências entre elas:

```text
fundacao-projeto ──┬─→ captura-confiavel ──→ ocr-confiavel ───┐
                   │                                          ├─→ backtest-realista
                   └─→ dominio-mercado ──→ analise-estatistica┘
```

| Spec | Escopo | Cobre | Bloqueada? |
|---|---|---|---|
| `fundacao-projeto` | Estrutura de pastas, ambiente, README, gitignore, ferramental, testes | V-13 a V-22 | não |
| `captura-confiavel` | Fluxo de gravação, nomenclatura, armazenamento, fixtures, região configurável | V-01 a V-05 | ação humana |
| `ocr-confiavel` | Confiança, faixa de sanidade, detecção de salto, falha explícita | V-06, V-07, V-08 | `captura-confiavel` |
| `dominio-mercado` | Menor oferta, quantidade, taxa, preço líquido | V-10 | `captura-confiavel` |
| `analise-estatistica` | Percentis, volatilidade, tempo em faixa, limiares derivados | V-11 | `dominio-mercado` |
| `backtest-realista` | Compra na menor oferta, limite por quantidade, taxa correta | V-09, V-12 | `dominio-mercado` |

Sugestão de início: `/sdd:steering` e depois `/sdd:spec-init` para
`fundacao-projeto`.

---

## 7. Divisão de trabalho

O projeto é tocado em dupla. A divisão segue um critério simples: **o que só
um humano com acesso ao jogo pode fazer fica com o dono do projeto; o resto
fica com a IA.** Os dois lados correm em paralelo.

### 7.1 Só o humano pode fazer

Estes itens são bloqueios reais — nenhuma quantidade de código os resolve.

| ID | Tarefa | Destrava | Detalhe |
|---|---|---|---|
| **H-1** | **Gravar material novo** ⏳ *adiado* | V-01, V-02 | Salvar **fora** da pasta temporária da Ferramenta de Captura. Idealmente em `data/raw/`. Gravar em **horários e dias diferentes**, não uma sessão só — a série atual tem 3 minutos e não representa nada. **O jogo está em outra máquina**, então o material chega em lote, não sob demanda. Planejar sempre com a trilha livre em paralelo. |
| **H-2** | **Confirmar a regra de taxa** | V-12 | Só a venda é taxada, ou compra e venda? Percentual fixo? Tem piso ou teto? |
| **H-3** | **Confirmar o que a tela mostra** | V-10 | A tela exibe a **menor oferta individual** e a **quantidade disponível**, ou só a faixa de preço e a média? Isso define se o modelo expandido é viável por OCR. |
| **H-4** | **Informar resolução e tema de UI** | V-03 | Resolução da tela, modo janela/tela cheia, escala do Windows. A região de recorte depende disso. |
| **H-5** | **Rotular as fixtures** | V-02 | Para cada frame escolhido, anotar à mão o valor verdadeiro. É o gabarito — sem ele não existe teste de OCR. |
| **H-6** | **Instalar o Tesseract** | V-13 | Instalador externo. A IA fornece o comando; a execução precisa de aprovação. |
| **H-7** | **Aprovar cada fase do SDD** | — | Requirements → Design → Tasks. Inerente ao método, não é burocracia. |

### 7.2 Fica com a IA

| ID | Tarefa | Cobre | Depende de |
|---|---|---|---|
| **C-1** | Estrutura: achatar `o/`, separar `data/` de `src/`, corrigir `.gitignore` e README | V-14 a V-17, V-19 | — |
| **C-2** | Ambiente: `pyproject` com deps de dev, pytest, lint, instruções de instalação | V-13, V-20 | — |
| **C-3** | Conduzir o SDD: steering e specs | V-18 | — |
| **C-4** | Endurecer o OCR: confiança, faixa de sanidade, detecção de salto, falha explícita | V-06, V-07 | H-1, H-5 |
| **C-5** | Expandir domínio, estatísticas e simulador | V-09 a V-12 | H-2, H-3 |
| **C-6** | Cobertura de testes e fixtures automatizadas | V-08 | H-5 |
| **C-7** | Ajustes menores | V-04, V-05, V-21, V-22 | — |

### 7.3 O que roda agora, em paralelo

```text
Humano ──→ H-1 (gravar) ──→ H-5 (rotular) ─────────┐
           H-2, H-3, H-4 (responder)                │
                                                     ├──→ C-4, C-5, C-6
IA ──────→ C-1, C-2, C-3, C-7 (não bloqueados) ────┘
```

Nada do que a IA faz hoje depende das gravações. Nada do que o humano faz
hoje depende do código. Os dois lados se encontram quando `fundacao-projeto`
estiver fechada e o material bruto existir.

---

## 8. Perguntas em aberto

1. **Onde estão as capturas de tela?** Não encontrei nenhuma imagem nem o
   vídeo original. Se estiverem em pen drive, nuvem ou outra máquina, o
   caminho destrava V-01 e V-02.
2. **Qual é a regra de taxa do mercado do jogo?** Só venda, ou compra e
   venda? Percentual fixo? (V-12)
3. ~~**O escopo é observador ou executor?**~~ ✅ **Respondido em 18/11/2026:**
   duas fases, observador primeiro. Ver V-23.
4. **A tela mostra a menor oferta individual** ou só a faixa de preço e a
   média? Isso define se V-10 é viável por OCR. (V-10)
5. **Qual a resolução e o tema de UI** usados na gravação? Necessário para
   documentar a região de recorte. (V-03)

---

## 9. Registro de alterações

| Data | Alteração |
|---|---|
| 18/11/2026 | Versão inicial — 23 achados catalogados, nenhum corrigido |
| 18/11/2026 | **V-23 decidido:** projeto em duas fases (observador → executor). Fronteira decidir/executar vira restrição arquitetural. |
| 18/11/2026 | Seção 7 adicionada: divisão de trabalho humano (H-1 a H-7) × IA (C-1 a C-7). |
| 18/11/2026 | `.sdd/steering/` criado (bootstrap): `product.md`, `tech.md`, `structure.md`. Aprovado como Source of Truth. |
| 18/11/2026 | **Convenção decidida:** migrar de `.format()` para f-string, com exceção para template-contrato; regra verificada por `ruff UP032`. Entra no escopo de `fundacao-projeto`. |
| 18/11/2026 | Requisitos de `fundacao-projeto` gerados e aprovados — 11 requisitos, 74 critérios EARS. Cinco pontos de decisão resolvidos. |
| 18/11/2026 | Design de `fundacao-projeto` gerado e aprovado — 9 decisões, sequência E0–E8 com portões. A-2 (flexibilizar Req. 2.7 para preservar evidência) e A-3 (`data/reference/` no steering) aprovados; A-7 (helper de *skip*) adiado para `ocr-confiavel`. |
| 18/11/2026 | Tarefas de `fundacao-projeto` geradas e aprovadas — 39 tarefas, 8 portões. Spec pronta para implementação. |
| 18/11/2026 | **Correção verificada:** a auditoria do Req. 3.7 exige `git check-ignore --no-index`. Sem a flag, o git não reporta arquivo já rastreado como ignorado e o portão passaria sempre, sem provar nada — justamente o caso do `ocr_samples.csv`, que originou o requisito. |
| 18/11/2026 | **Achatamento executado manualmente** pelo dono do projeto, fora do git. Conteúdo de `o/` movido para a raiz; `o/` removido. Preservação de histórico a verificar após o commit. |
| 18/11/2026 | **V-24 adicionado:** sem `.gitattributes`, quebras de linha não normalizadas. Descoberto ao simular o commit. Entra no escopo de `fundacao-projeto`. |
