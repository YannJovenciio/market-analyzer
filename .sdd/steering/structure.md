# Estrutura — Market Analyzer

> **Atenção antes de usar este documento como mapa.** A organização **lógica**
> descrita na primeira metade está correta e deve ser preservada. A disposição
> **física** atual tem defeitos conhecidos, listados no fim em "Pendências
> estruturais". Não tome o que está lá por convenção vigente, e não replique.

## Organização lógica (preservar)

O pacote é dividido por **responsabilidade no pipeline**, não por tipo de
artefato:

| Camada | Responsabilidade | Conhece |
|---|---|---|
| `domain` | Modelos e contratos de negócio | nada |
| `ingestion` | Entrada: vídeo, frame, OCR, CSV | `domain` |
| `analysis` | Estatísticas e indicadores sobre a série | `domain` |
| `backtesting` | Simulação sem efeito externo | `domain` |
| `cli` | Orquestração e saída para o humano | todos |

**Regra de dependência:** o sentido é sempre para dentro. `domain` não importa
ninguém. Nenhuma camada importa para cima. `cli` é o único ponto que amarra as
outras, e é também a borda onde a recomendação sai para o mundo — ver a
fronteira decidir/executar em `tech.md`.

## Fluxo do pipeline

```text
vídeo (.mp4)
   └─ video_sampler ─→ frames PNG
                          └─ price_ocr ─→ ocr_batch ─→ CSV
                                                        └─ csv_loader ─→ statistics
                                                                           └─ simulator ─→ cli
```

Cada etapa é um módulo com CLI própria, executável isoladamente. A fronteira
entre etapas é sempre um **artefato em disco** (frames, CSV) ou uma lista de
objetos de domínio — nunca estado compartilhado em memória.

## Onde colocar coisa nova

- **Novo conceito de negócio** (menor oferta, preço líquido, recomendação) →
  `domain/models.py`, como dataclass congelada, sem I/O.
- **Nova fonte de entrada** (SQLite, outra captura, outro formato de CSV) →
  `ingestion/`, convertendo para modelos de domínio na fronteira.
- **Nova medida sobre a série** (percentil, volatilidade, tempo em faixa) →
  `analysis/`.
- **Nova regra de simulação** → `backtesting/`, mantendo a função pura.
- **Nova forma de apresentar ao humano** (GUI, relatório) → **adaptador novo na
  borda**, consumindo os mesmos serviços. Não é motivo para mexer no núcleo.
- **Teste** → `tests/`, espelhando a área testada.

## Convenções de nomenclatura

- **Módulos e pacotes:** `snake_case`, nome que descreve a etapa
  (`video_sampler`, `price_ocr`, `ocr_batch`, `csv_loader`).
- **Frames amostrados:** `frame_{segundos:06.1f}s.png`, ex. `frame_0010.0s.png`.
  O timestamp faz parte do nome e é **relido** por expressão regular na etapa
  seguinte — o nome do arquivo é contrato entre etapas, não enfeite.
- **Colunas de CSV em português:** `timestamp,item,preco_medio,origem_video,observacao`.
  Expansão prevista pela análise inicial acrescenta `menor_oferta`,
  `maior_oferta`, `quantidade_disponivel`, `taxa`, `preco_liquido`.
  Identificadores Python permanecem em inglês; a conversão acontece no
  `csv_loader` (`preco_medio` → `average_price`, `origem_video` → `source`).
- **Timestamps em ISO 8601** com segundos, tanto no CSV quanto nos nomes de
  recorte temporal.
- **CSV lido com `encoding="utf-8-sig"`** (tolera BOM) e escrito com
  `encoding="utf-8"`, sempre com `newline=""`.

## Separação entre código, dados e documentos

Três categorias distintas, que não devem se misturar:

- **Código** — o pacote Python.
- **Dados** — material bruto (`data/raw/`: vídeos e frames, nunca versionados) e
  derivados (`data/processed/`: CSVs gerados). **Dados não pertencem a `src/`.**
  Exceção deliberada: **fixtures de OCR rotuladas**, que são gabarito de teste e
  precisam ser versionadas com exceção explícita no `.gitignore`.
- **Documentos de projeto** — `README.md`, `analise-inicial.md`,
  `validacao-inicial.md`, na raiz.

`validacao-inicial.md` é o registro vivo do estado real e dos achados pendentes;
ele deve ser atualizado conforme os itens forem resolvidos.

## Pendências estruturais (defeitos, não padrões)

Itens de `validacao-inicial.md` a serem corrigidos na spec `fundacao-projeto`.
**Nenhum deles é convenção do projeto. Não imite.**

| ID | Defeito | Correção prevista |
|---|---|---|
| **V-14** | **A pasta `o/`.** O repositório git está em `market-analyzer/`, mas todo o conteúdo caiu em `market-analyzer/o/` por provável erro de digitação. Não há nenhuma razão para esse nível a mais. | Achatar: o conteúdo de `o/` sobe para a raiz do repositório. Inclui este diretório `.sdd/`. |
| **V-16** | **Dados dentro de `src/`.** `initial_data.csv` está dentro do próprio pacote Python, e `src/data/` cai dentro da pasta de distribuição do setuptools. | Mover para `data/` fora de `src/`. |
| **V-17** | **`.gitignore` com regras mal ancoradas.** `data/raw/` e `data/processed/` contêm barra no meio, então o git as ancora na pasta do próprio `.gitignore`, e não no caminho real dos dados. Por isso um CSV gerado acabou versionado. | Reescrever as regras ancoradas corretamente, com exceção explícita para as fixtures rotuladas. |
| **V-19** | **`market_analyser.py` é shim inútil.** Compatibilidade com a grafia britânica em um projeto de 1 commit — não há histórico a preservar. | Remover. |
| **V-15** | **README desatualizado em três pontos:** cita `storage/` que não existe, aponta os testes para `src/tests` quando estão em `tests/`, e afirma que o projeto não usa Git quando já há repositório. | Reescrever junto com a correção da estrutura. |
| **V-04** | **Atalho `.lnk` versionado** apontando para pasta temporária do Windows. Não é portável e não resolve. | Remover do versionamento. |

### Estrutura de destino

Depois de `fundacao-projeto`, o repositório deve ficar assim — pastas, não
arquivos:

```text
market-analyzer/
├─ src/market_analyzer/     # só código
│  ├─ domain/ ingestion/ analysis/ backtesting/
│  └─ cli.py
├─ tests/                   # espelha as camadas
├─ data/                    # fora de src/
│  ├─ raw/                  # vídeos e frames — não versionado
│  ├─ processed/            # CSVs gerados — não versionado
│  └─ fixtures/             # frames rotulados — VERSIONADO (exceção)
├─ .sdd/                    # steering e specs
├─ pyproject.toml
├─ README.md
└─ *.md                     # documentos de análise e validação
```
