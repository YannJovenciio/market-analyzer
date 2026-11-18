# Requisitos — fundacao-projeto

> **Fase: requisitos gerados.** Aguardando revisão humana.
> Os requisitos abaixo estão em formato EARS. A descrição de origem foi
> preservada na seção "Contexto de origem" para não se perder.

## Introdução

Esta especificação corrige a **fundação** do repositório Market Analyzer antes
de qualquer trabalho de OCR ou de domínio. A organização **lógica** do código
está correta e é preservada; o que está defeituoso é a **disposição física**,
o **ambiente** e o **ferramental**.

### O que é "o sistema" nesta spec

Ao contrário das demais specs do roteiro, esta não descreve comportamento de
runtime do produto. Aqui, **o sistema é o repositório e o ambiente de
desenvolvimento**: a árvore de arquivos, o `pyproject.toml`, o `.gitignore`, a
suíte de testes, o linter e o README. Cada critério abaixo é um **resultado
verificável** — alguém precisa conseguir dizer "cumpriu" ou "não cumpriu"
executando um comando ou inspecionando um arquivo, sem debate.

### Linha de base verificada (18/11/2026)

Os critérios se apoiam neste estado real, medido antes de qualquer correção:

| Item | Estado medido |
|---|---|
| Repositório git | `market-analyzer/`, 1 commit (`35fdcc9 start repo`) |
| Conteúdo | ⚠️ **mudou durante a elaboração desta spec** — ver nota abaixo |
| Python | 3.12.10 disponível (piso declarado: 3.10) |
| `pytesseract`, `imageio_ffmpeg`, binário do Tesseract | ausentes |
| `pip install -e .` | nunca executado |
| Testes | 8 passam, 1 módulo não importa (`test_video_sampler.py`) |
| `.format()` | 21 usos em 5 arquivos; zero f-strings |
| Saída do CLI de referência | 20 amostras, mínimo 110037, máximo 220074 |

> **Nota sobre o achatamento (18/11/2026, durante a revisão).** O dono do
> projeto moveu manualmente o conteúdo de `o/` para a raiz do repositório
> **enquanto esta spec era redigida**. O estado medido passou a ser:
>
> - conteúdo na raiz de `market-analyzer/`;
> - `o/` ainda presente, contendo apenas um resto vazio de `.sdd/`;
> - **nada commitado:** 24 exclusões e 9 caminhos novos sem rastreamento.
>
> O Requisito 1 **continua valendo integralmente** e nenhum de seus critérios
> deve ser afrouxado. A movimentação foi feita fora do git, então a
> preservação de histórico (critério 1.3) ainda **não está garantida**: ela
> depende da detecção de renomeação no commit, que só funciona porque o
> conteúdo dos arquivos está intacto. Verificar com `git log --follow` depois
> de commitar, e não presumir.

---

## Requisitos

### Requisito 1 — Achatamento do repositório

**História de usuário:** Como desenvolvedor do projeto, quero todo o conteúdo na
raiz do repositório git, para que caminhos, comandos e ferramentas funcionem sem
um nível extra inexplicado, e para que o git enxergue o projeto que versiona.

#### Critérios de aceitação

1. O sistema DEVE manter todo o conteúdo do projeto na raiz do repositório git
   (`market-analyzer/`), sem nenhum diretório intermediário `o/`.
2. QUANDO o achatamento for concluído, o diretório `o/` NÃO DEVE existir, nem no
   índice do git nem no sistema de arquivos.
3. O sistema DEVE preservar o histórico git de cada arquivo movido, de modo que
   `git log --follow <arquivo>` continue alcançando o commit `35fdcc9`.
4. O diretório `.sdd/` DEVE subir junto com o restante do conteúdo e estar na
   raiz após o achatamento, com `.sdd/steering/` contendo `product.md`,
   `tech.md` e `structure.md`, e `.sdd/specs/fundacao-projeto/` contendo
   `requirements.md` e `spec.json`.
5. Os documentos de projeto (`README.md`, `analise-inicial.md`,
   `validacao-inicial.md`) DEVEM ficar na raiz do repositório.
6. QUANDO o achatamento for concluído, o sistema DEVE executar a suíte de testes
   e o CLI a partir da nova raiz com o mesmo resultado observado antes do
   achatamento.
7. SE um documento versionado citar um caminho com `o/` **como instrução ou
   referência operacional** (README, steering, specs), ENTÃO esse caminho DEVE
   ser atualizado para o caminho real pós-achatamento; o registro histórico em
   `validacao-inicial.md` PODE preservar os caminhos originais como evidência
   dos achados.

---

### Requisito 2 — Separação entre dados e código

**História de usuário:** Como desenvolvedor, quero dados fora do pacote Python,
para que o que é distribuído seja só código e o que é dado não vaze para dentro
da instalação.

#### Critérios de aceitação

1. O sistema DEVE manter dados fora do pacote Python distribuível: nenhum
   arquivo de dados (`.csv`, `.png`, `.mp4` e congêneres) DEVE residir sob
   `src/`.
2. O repositório DEVE conter, na raiz, os diretórios `data/raw/`,
   `data/processed/`, `data/fixtures/` e `data/reference/`, presentes em um
   clone limpo mesmo quando vazios.
3. `initial_data.csv` DEVE residir em `data/reference/` e **permanecer
   versionado**, por ser transcrição manual de referência — nem captura bruta,
   nem artefato descartável.
4. `ocr_samples.csv` DEVE residir em `data/reference/` e **permanecer
   versionado**. Decidido na revisão de 18/11/2026: junto com
   `initial_data.csv`, ele forma a **linha de base do achado V-06**
   (transcrição manual × saída do OCR, 5 divergências em 20 amostras). É contra
   esse par que a spec `ocr-confiavel` vai demonstrar melhora, de modo que
   descartá-lo eliminaria o único gabarito existente.
   - Corolário: `data/reference/` guarda material de referência estável e
     versionado, e por isso **não** é alcançado pelas regras de ignorar de
     `data/raw/` e `data/processed/`.
5. QUANDO o pacote for instalado (`python -m pip install -e .`), o sistema NÃO
   DEVE incluir nenhum arquivo de dados no pacote `market_analyzer`.
6. QUANDO o CLI for executado apontando para o CSV de referência no novo
   caminho, o sistema DEVE produzir os mesmos números da linha de base
   (20 amostras, mínimo 110037, máximo 220074).
7. Nenhum módulo, teste ou documento DEVE referenciar os caminhos antigos
   `src/data/` ou `src/market_analyzer/initial_data.csv` após a migração.

---

### Requisito 3 — Versionamento correto: ignorar, versionar e normalizar

**História de usuário:** Como desenvolvedor, quero regras de ignorar que
realmente valham no caminho pretendido, para que nenhum artefato gerado entre no
versionamento por acidente — e para que as fixtures rotuladas, que são gabarito
de teste, **não** sejam ignoradas.

#### Critérios de aceitação

1. O `.gitignore` DEVE residir na raiz do repositório e ancorar as regras de
   dados no caminho real (`/data/raw/`, `/data/processed/`), corrigindo a
   ancoragem defeituosa atual.
2. QUANDO um arquivo for criado em `data/raw/` ou `data/processed/`, o sistema
   DEVE mantê-lo fora do versionamento — verificável por `git status` não
   listá-lo e por `git check-ignore -v <arquivo>` apontar a regra responsável.
3. ONDE existirem fixtures rotuladas em `data/fixtures/`, o sistema DEVE
   versioná-las apesar da regra global que ignora `*.png`, por meio de exceção
   explícita, posicionada depois das regras de ignorar para ter efeito.
4. QUANDO um arquivo `.png` for colocado em `data/fixtures/`, `git check-ignore`
   DEVE indicar que ele **não** está ignorado; QUANDO o mesmo arquivo for
   colocado em `data/raw/`, DEVE indicar que **está**.
5. O arquivo `ocr_samples.csv` DEVE permanecer rastreado pelo git, em
   `data/reference/` (ver Requisito 2, critério 4). SE a regra de ignorar
   passar a alcançá-lo em qualquer caminho, ENTÃO a regra está errada e DEVE
   ser corrigida — não o inverso.
   - `git check-ignore -v data/reference/ocr_samples.csv` DEVE indicar que ele
     **não** está ignorado.
6. O `.gitignore` DEVE continuar ignorando artefatos de ambiente e ferramenta
   (`__pycache__/`, `*.py[cod]`, `*.egg-info/`, `.venv/`, `.pytest_cache/`,
   `.ruff_cache/`) e mídia fora de `data/fixtures/`.
7. SE um arquivo já rastreado passar a casar com uma regra de ignorar, ENTÃO o
   sistema DEVE removê-lo do índice explicitamente, já que `.gitignore` não
   afeta arquivos já rastreados.
8. O repositório DEVE conter um `.gitattributes` na raiz que normalize as
   quebras de linha dos arquivos de texto (`* text=auto`), de modo que o
   conteúdo versionado use LF e cada checkout use o fim de linha nativo da
   máquina. *(V-24, descoberto em 18/11/2026 ao simular o commit do
   achatamento: o git avisou `LF will be replaced by CRLF` em 7 arquivos.)*
9. QUANDO o repositório for clonado em uma máquina com configuração de
   `core.autocrlf` diferente da atual, o sistema NÃO DEVE apresentar arquivos
   como modificados sem que seu conteúdo tenha mudado — verificável por
   `git status` limpo logo após um clone.
10. ONDE existirem arquivos binários versionados (fixtures `.png`), o
    `.gitattributes` DEVE marcá-los como binários, para que nenhuma conversão
    de fim de linha os corrompa.

---

### Requisito 4 — Ambiente instalável e reprodutível

**História de usuário:** Como desenvolvedor em máquina limpa, quero um caminho
de instalação único e documentado, para chegar a um ambiente capaz de rodar
testes e linter sem adivinhação.

#### Critérios de aceitação

1. QUANDO um desenvolvedor executa `python -m pip install -e .[dev]` em uma
   máquina com ambiente limpo e Python 3.10 ou superior, o sistema DEVE instalar
   todas as dependências necessárias para rodar a suíte de testes e o linter,
   sem nenhum passo manual adicional exceto o binário do Tesseract.
2. O `pyproject.toml` DEVE declarar `[project.optional-dependencies]` com um
   grupo `dev` contendo ao menos `pytest` e `ruff`, com versão mínima declarada
   para cada um.
3. O sistema DEVE manter `requires-python = ">=3.10"` como piso e permanecer
   instalável no Python 3.12 do ambiente atual.
4. SE o binário do Tesseract não estiver disponível no PATH, ENTÃO o sistema
   DEVE falhar com mensagem que identifique o Tesseract como pré-requisito
   externo não instalável por `pip` e indique onde obter as instruções de
   instalação.
5. SE `pytesseract` ou `imageio_ffmpeg` não estiverem instalados, ENTÃO o módulo
   que depende deles DEVE falhar com mensagem acionável nomeando a dependência
   ausente, sem impedir a importação dos demais módulos do pacote.
6. A documentação de instalação DEVE tratar o Tesseract como passo de primeira
   classe, separado do `pip`, acompanhado de um comando de verificação objetivo
   (`tesseract --version`).
7. QUANDO a instalação for concluída, o comando `market-analyzer --help` DEVE
   executar sem erro.

---

### Requisito 5 — Suíte de testes executável por inteiro

**História de usuário:** Como desenvolvedor, quero que todos os módulos de teste
realmente rodem, para ter rede de segurança antes de mexer em sintaxe e
estrutura.

#### Critérios de aceitação

1. QUANDO a suíte de testes é executada, o sistema DEVE coletar e executar todos
   os módulos de `tests/`, sem que nenhum falhe por erro de importação.
2. QUANDO a suíte é executada após `python -m pip install -e .[dev]`,
   `tests/test_video_sampler.py` DEVE executar seus casos e passar, encerrando a
   situação atual em que o módulo nunca roda.
3. O sistema DEVE executar os testes existentes, escritos com `unittest`, por
   meio do `pytest`, sem exigir reescrita dos casos.
4. ENQUANTO o binário do Tesseract não estiver instalado (bloqueio humano H-6),
   a suíte DEVE concluir sem falha: os testes que exigem o binário DEVEM ser
   pulados explicitamente, com motivo declarado na saída, em vez de falharem.
5. QUANDO a suíte é executada após as correções, o número de testes executados
   DEVE ser maior que a linha de base de 8, e nenhum DEVE falhar.
6. O sistema DEVE expor um comando único de execução da suíte, funcional a
   partir da raiz do repositório e documentado no README.
7. SE um teste depender de escrita em disco, ENTÃO ele DEVE usar diretório
   temporário, nunca caminho fixo dentro do projeto.

---

### Requisito 6 — Remoção de artefatos obsoletos

**História de usuário:** Como desenvolvedor, quero o repositório livre de
arquivos que não resolvem nem servem a nada, para que ninguém perca tempo
tentando entender por que existem.

#### Critérios de aceitação

1. O repositório NÃO DEVE conter o atalho
   `src/market_analyzer/20261116-1555-54.7150164.mp4.lnk`, nem rastreado pelo
   git nem presente no disco — ele aponta para pasta temporária do Windows, não
   é portável e não resolve.
2. O repositório NÃO DEVE conter o módulo
   `src/market_analyzer/market_analyser.py`, shim de grafia britânica sem
   histórico a preservar.
3. QUANDO a remoção for concluída, `git ls-files` NÃO DEVE listar nenhum dos
   dois arquivos.
4. SE algum módulo, teste ou documento referenciar `market_analyser`, ENTÃO a
   referência DEVE ser corrigida para `market_analyzer.cli` ou removida antes da
   exclusão do arquivo.
5. QUANDO o shim for removido, o ponto de entrada de console
   `market-analyzer = "market_analyzer.cli:main"` DEVE continuar funcionando.

---

### Requisito 7 — Interpolação por f-string verificada por linter

**História de usuário:** Como desenvolvedor, quero uma convenção de interpolação
única e **verificada por ferramenta**, para que ela se sustente sem depender de
revisão humana.

#### Critérios de aceitação

1. O sistema NÃO DEVE conter nenhuma chamada a `str.format()` para interpolação
   imediata no pacote: os 21 usos atuais — `cli.py` (9), `csv_loader.py` (3),
   `ocr_batch.py` (5), `price_ocr.py` (1), `video_sampler.py` (3) — DEVEM ser
   convertidos em f-string ou absorvidos pelas funções de contrato do
   Requisito 8.
2. O `pyproject.toml` DEVE configurar o `ruff` com a regra `UP032` ativada.
3. QUANDO `ruff check .` é executado a partir da raiz, o sistema DEVE terminar
   sem nenhuma violação, incluindo `UP032`.
4. SE um novo uso de `.format()` para interpolação imediata for introduzido,
   ENTÃO `ruff check` DEVE falhar apontando `UP032`, com arquivo e linha.
5. ONDE houver exceção legítima à convenção — template que é contrato entre
   módulos, ou formatação preguiçosa de `logging` — o sistema DEVE resolvê-la
   por extração de função ou pelo estilo `%s` do próprio logger, e NÃO por
   supressão pontual com `# noqa`.
6. QUANDO o CLI for executado com o CSV de referência antes e depois da
   migração, o sistema DEVE produzir o mesmo texto e os mesmos valores — a
   migração é de sintaxe, não de comportamento.
7. O sistema DEVE expor um comando único de execução do linter, documentado no
   README e funcional a partir da raiz.

---

### Requisito 8 — Nome de frame como contrato único

**História de usuário:** Como desenvolvedor, quero que o formato do nome de
frame tenha uma definição só, para que escritor e leitor nunca saiam de sincronia
em silêncio.

#### Critérios de aceitação

1. O sistema DEVE ter uma **única** definição do formato do nome de frame
   (`frame_{segundos:06.1f}s.png`), exposta como par de funções
   `frame_name(seconds) -> str` e `frame_seconds(path) -> float` em um módulo
   compartilhado.
2. `video_sampler` DEVE escrever o nome do frame por meio de `frame_name()` e
   `ocr_batch` DEVE lê-lo por meio de `frame_seconds()`; nenhum dos dois DEVE
   conter o literal do formato nem a expressão regular correspondente.
3. QUANDO `frame_seconds(frame_name(t))` é avaliado para qualquer `t` válido, o
   sistema DEVE devolver `t` na precisão do formato (uma casa decimal), e esse
   ida-e-volta DEVE estar coberto por teste automatizado.
4. SE o nome do arquivo não corresponder ao formato, ENTÃO `frame_seconds()`
   DEVE levantar `ValueError` com mensagem contendo o nome recebido.
5. QUANDO frames forem ordenados para processamento, a ordenação DEVE ser pelo
   valor numérico de segundos, e não lexicográfica pelo nome.
   *Motivo verificado:* o padding de `{:06.1f}` sustenta a ordem lexicográfica
   até `9999.9` (`frame_9999.9s.png`); a partir de `10000.0` o nome passa a ter
   7 dígitos e `frame_10000.0s.png` ordena **antes** de `frame_9999.9s.png`.
   O limite é ~2 h 46 min de gravação. O código atual já ordena por valor
   numérico; este critério existe para que isso não se perca na refatoração.
6. A localização do par de funções DEVE respeitar a regra de dependência das
   camadas: fica em `ingestion`, sem que `domain` passe a importar qualquer
   coisa e sem que outra camada importe para cima.

---

### Requisito 9 — README fiel ao projeto

**História de usuário:** Como pessoa chegando ao projeto, quero um README que
descreva o que de fato existe, para conseguir instalar e rodar sem descobrir por
tentativa e erro que o documento mente.

#### Critérios de aceitação

1. O README NÃO DEVE citar `src/market_analyzer/storage`, que não existe.
2. O README DEVE apontar os testes para `tests/` na raiz, e não para
   `src/tests`.
3. O README NÃO DEVE afirmar que o projeto não usa Git; DEVE refletir que o
   repositório existe.
4. O README DEVE descrever a estrutura de pastas correspondente à estrutura de
   destino de `structure.md`, e essa descrição DEVE corresponder, pasta a pasta,
   ao que existe no disco após as correções.
5. O README DEVE conter, em sequência copiável e executável: instalação com
   `[dev]`, instalação do Tesseract como passo separado com verificação,
   execução da suíte, execução do linter e execução do CLI com exemplo real
   apontando para o CSV de referência.
6. O README DEVE registrar a separação entre `data/raw/`, `data/processed/` e
   `data/fixtures/`, explicitando que as fixtures rotuladas são versionadas por
   exceção deliberada.
7. Todo comando citado no README DEVE ser executável exatamente como escrito, a
   partir da raiz do repositório.
8. QUANDO um desenvolvedor seguir o README do início ao fim em máquina limpa, o
   sistema DEVE chegar a suíte verde e CLI executável sem recorrer a informação
   fora do documento, exceto o download do instalador do Tesseract.

---

### Requisito 10 — Ordem segura de execução da fundação

**História de usuário:** Como responsável pela correção, quero que cada mudança
parta de uma base verificada, para não trocar sintaxe em arquivo que não tem
rede de teste.

#### Critérios de aceitação

1. O sistema DEVE estar instalável (Requisito 4) e com a suíte completa
   executável e verde (Requisito 5) **antes** de qualquer alteração de sintaxe
   prevista no Requisito 7.
2. SE a suíte não estiver verde, ENTÃO a migração de `.format()` para f-string
   NÃO DEVE ser iniciada.
3. ENQUANTO `tests/test_video_sampler.py` não executar de fato, o sistema NÃO
   DEVE sofrer alteração em `video_sampler.py` — é o arquivo sem rede de teste e
   o risco principal desta spec.
4. O achatamento do Requisito 1 DEVE ser executado por operação que preserve o
   histórico (`git mv` ou equivalente), e nunca por cópia seguida de exclusão.
5. QUANDO cada etapa da fundação for concluída, o sistema DEVE permitir
   verificar o estado por comando objetivo — suíte verde, `ruff check` limpo,
   `git status` sem alteração não intencional — de modo que a etapa seguinte
   parta de base verificada.
6. SE qualquer etapa deixar a suíte vermelha, ENTÃO essa etapa DEVE ser
   corrigida ou revertida antes de qualquer etapa seguinte.

---

### Requisito 11 — Saída do CLI legível no console

**História de usuário:** Como usuário no Windows, quero ler o nome do item sem
caracteres trocados, para que a saída sirva de informação e não de charada.

> **Confirmado na revisão de 18/11/2026.** Este requisito cobre o achado V-21,
> atribuído a `fundacao-projeto` em `tech.md` e listado em `spec.json`. Não
> constava da lista de 8 itens da descrição de origem e por isso foi levantado
> para decisão; **fica nesta spec** — é problema de ambiente e de borda, que é
> exatamente o escopo da fundação.

#### Critérios de aceitação

1. QUANDO o CLI é executado em terminal Windows cuja codificação padrão não é
   UTF-8 (cp1252), o sistema DEVE imprimir o texto acentuado corretamente
   (ex.: `Algodão de isolamento acústico`), sem substituir caracteres por `?`.
2. O sistema DEVE tratar a codificação da saída na borda (`cli`), sem exigir que
   o usuário altere a codepage do terminal manualmente.
3. QUANDO a saída for redirecionada para arquivo, o conteúdo DEVE permanecer
   legível, com acentuação preservada.
4. SE um caractere não puder ser representado no fluxo de saída, ENTÃO o sistema
   DEVE degradar de forma previsível e documentada, nunca corrompendo o restante
   da linha.

---

## Restrições transversais

Valem para todos os requisitos acima e não são negociáveis dentro desta spec:

1. O sistema DEVE preservar a **organização lógica** em camadas
   (`domain` / `ingestion` / `analysis` / `backtesting` / `cli`) e a regra de
   dependência em sentido único. Esta spec corrige disposição física, ambiente e
   ferramental — **não** reorganiza camadas.
2. O sistema NÃO DEVE alterar o comportamento observável do pipeline: nenhuma
   mudança em pré-processamento de imagem, padrão de preço, estatísticas ou
   regras do simulador pertence a esta spec.
3. O sistema DEVE manter identificadores, docstrings e mensagens de programa em
   **inglês**, e documentação de projeto e nomes de coluna de CSV em
   **português**, conforme `tech.md` e `structure.md`.
4. O ambiente de referência para verificação é **Windows com PowerShell**, com o
   Python 3.12 instalado; o código permanece escrito para o piso 3.10.
5. O sistema DEVE manter `validacao-inicial.md` atualizado conforme os achados
   desta spec forem resolvidos — é o registro vivo do estado real.

---

## Fora de escopo

Registrado explicitamente para que não volte como sugestão:

| Item | Por quê |
|---|---|
| **V-22** — decodificação integral do vídeo | Marcado como baixa prioridade em `tech.md`, sem spec atribuída. É otimização, não fundação. |
| **Conteúdo** das fixtures rotuladas (V-02) | Bloqueado por H-1/H-5 (gravar e rotular). Esta spec cria a pasta e a regra de versionamento; o conteúdo vem depois. |
| CI, Docker, verificador de tipos, formatador automático | Não constam do escopo de origem. Esta spec entrega instalação, testes e linter. |
| Reescrita dos testes de `unittest` para estilo `pytest` | O `pytest` é adotado como executor; os casos existentes permanecem como estão. |
| Endurecimento do OCR (V-06, V-07), região de recorte (V-03, V-05) | Specs `ocr-confiavel` e `captura-confiavel`. |
| Domínio, estatística e backtest (V-09 a V-12) | Specs `dominio-mercado`, `analise-estatistica`, `backtest-realista`. Dependem de respostas humanas (H-2, H-3). |
| Perguntas em aberto sobre o jogo (taxa, o que a tela mostra, resolução) | Bloqueios humanos H-2 a H-4. Não devem ser inferidos aqui. |

---

## Rastreabilidade — achado → requisito

| Achado | Descrição curta | Requisito(s) |
|---|---|---|
| V-04 | Atalho `.lnk` versionado | 6 |
| V-13 | Ambiente não instalado (Tesseract, `pytesseract`, `imageio_ffmpeg`) | 4, 5 |
| V-14 | Pasta `o/` | 1, 10 |
| V-15 | README desatualizado em três pontos | 9 |
| V-16 | Dados misturados com código | 2 |
| V-17 | `.gitignore` mal ancorado | 3 |
| V-18 | `.sdd/` inexistente | 1 (item 4 — garante que não se perca no achatamento) |
| V-19 | Shim `market_analyser.py` | 6 |
| V-20 | Sem ferramentas de desenvolvimento | 4, 5, 7 |
| V-21 | Acentos quebrados no console | 11 |
| V-24 | Sem `.gitattributes`, quebras de linha não normalizadas | 3 (critérios 8 a 10) |
| V-22 | Decodificação integral do vídeo | fora de escopo |
| V-02 (parcial) | Fixtures precisam ser versionadas | 2, 3 (pasta e regra; conteúdo bloqueado) |
| Convenção 18/11 | f-string com exceção de template-contrato | 7, 8 |

---

## Decisões da revisão — resolvidas em 18/11/2026

Os cinco pontos levantados na geração foram decididos pelo dono do projeto.
Ficam registrados com o resultado para não serem reabertos por inércia.

| # | Ponto | Decisão |
|---|---|---|
| 1 | Destino de `initial_data.csv` | **`data/reference/`**, versionado. Descartada a alternativa de deixá-lo solto na raiz de `data/`: os irmãos são subpastas, e um arquivo solto não comunica por que ele é versionado e os vizinhos não. |
| 2 | `ocr_samples.csv` | **Versionado em `data/reference/`.** Rejeitada a proposta original de "manter no disco sem rastrear" — isso o faria desaparecer em um clone novo e ficar invisível para qualquer outra pessoa, o pior dos dois mundos. Ou é evidência e se versiona, ou é descartável e se apaga. É evidência: forma com `initial_data.csv` a linha de base do V-06. |
| 3 | Caminhos `o/` em `validacao-inicial.md` | **Preservar como evidência histórica**, atualizando apenas caminhos que sirvam de instrução. Reescrever a evidência de um achado destruiria o achado. |
| 4 | Requisito 11 (V-21, acentos no console) | **Mantido nesta spec.** É problema de ambiente e de borda, exatamente o escopo da fundação, e é barato. O aviso "a confirmar" no corpo do requisito fica sem efeito. |
| 5 | Onde mora `frame_name()` / `frame_seconds()` | **Adiado para o design**, como proposto. O requisito fixa que a definição é única e compartilhada; o módulo exato é decisão da fase seguinte. |

---

## Contexto de origem

> Preservado da fase de inicialização, sem alteração de conteúdo.

### Descrição do projeto

Corrigir a fundação do repositório **Market Analyzer** antes de qualquer
trabalho de OCR ou análise.

A organização lógica do código está correta e deve ser preservada; o que está
defeituoso é a disposição física, o ambiente e o ferramental. Enquanto essa
base não estiver firme, qualquer trabalho de OCR ou domínio é construído sobre
terreno instável.

### Escopo pretendido

1. **Achatar a pasta `o/`** — mover todo o conteúdo para a raiz do repositório
   git em `market-analyzer/`, incluindo o próprio `.sdd/`, que não pode ficar
   para trás na correção.
2. **Separar dados de código** — tirar `initial_data.csv` de dentro do pacote
   Python e `src/data/` de dentro de `src/`; criar `data/raw/`,
   `data/processed/` e `data/fixtures/`.
3. **Reescrever o `.gitignore`** com regras ancoradas corretamente, e com
   exceção explícita para as fixtures rotuladas, que **precisam** ser
   versionadas por serem gabarito de teste.
4. **Tornar o ambiente instalável e reprodutível** — `optional-dependencies`
   de desenvolvimento, `pytest`, `ruff`, e instruções que tratem o binário do
   **Tesseract** como passo de primeira classe, separado do `pip`.
5. **Migrar `.format()` para f-string** com a regra `ruff UP032` ativada,
   extraindo `frame_name()` / `frame_seconds()` como par de funções
   compartilhadas entre `video_sampler` e `ocr_batch`, que hoje duplicam o
   conhecimento do formato do nome de frame.
6. **Garantir que a suíte de testes rode inteira**, incluindo
   `test_video_sampler.py`, que hoje nem importa por falta de
   `imageio_ffmpeg`.
7. **Remover** o shim `market_analyser.py` e o atalho `.lnk` versionado.
8. **Reescrever o README**, hoje errado em três pontos.

### Achados de origem

Corresponde aos achados **V-04** e **V-13 a V-22** de `validacao-inicial.md`.

### Posição no roteiro

```text
fundacao-projeto ──┬─→ captura-confiavel ──→ ocr-confiavel ───┐
                   │                                          ├─→ backtest-realista
                   └─→ dominio-mercado ──→ analise-estatistica┘
```

É a **única spec sem bloqueio**: não depende do material bruto (H-1) nem das
respostas do dono do projeto sobre o jogo (H-2 a H-4). Roda em paralelo ao
trabalho humano de gravar material novo.

### Pontos a resolver na fase de requisitos

Registrados na inicialização; endereçados nos Requisitos 10 e 2/3:

- **Ordem de execução importa.** A migração para f-string toca
  `video_sampler.py`, que hoje **não tem teste que rode**. O ambiente precisa
  ser consertado e a suíte precisa estar verde **antes** da mudança de
  sintaxe — trocar sintaxe em arquivo sem rede é barato e custa caro.
  → Requisito 10.
- **O achatamento de `o/` deve preservar o histórico do git** (`git mv`, não
  copiar e apagar), já que o repositório tem commit anterior.
  → Requisitos 1.3 e 10.4.
- **As fixtures ainda não existem** (V-02, bloqueada por H-1). Esta spec cria
  a pasta e a regra de versionamento; o conteúdo vem depois.
  → Requisitos 2.2 e 3.3.
