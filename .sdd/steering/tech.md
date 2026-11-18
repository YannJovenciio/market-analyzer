# Tecnologia — Market Analyzer

## Stack

- **Python 3.10+** declarado em `pyproject.toml` (`requires-python`); ambiente de
  desenvolvimento atual roda 3.12. Escreva para 3.10 como piso.
- **Empacotamento:** setuptools com *src layout*, pacote descoberto em `src/`.
  Entry point de console declarado em `[project.scripts]`.
- **Imagem e vídeo:** Pillow para recorte e pré-processamento; numpy para o
  buffer de frame; `imageio-ffmpeg` para decodificar o vídeo.
- **OCR:** `pytesseract`, que é apenas um invólucro — ele exige o **binário do
  Tesseract instalado no sistema**, fora do alcance do `pip`.
- **Testes:** `unittest` da biblioteca padrão. Não há pytest, linter, formatador
  nem CI configurados (V-20).

### Pré-requisito externo que quebra a instalação ingênua

`python -m pip install -e .` **não é suficiente**. Sem o executável do Tesseract
no PATH, todo o caminho de OCR falha em tempo de execução. Qualquer instrução de
instalação precisa tratar isso como passo de primeira classe, separado das
dependências Python.

Estado verificado em 18/11/2026: `pytesseract`, `imageio_ffmpeg` e o binário do
Tesseract **ausentes**; `pip install -e .` nunca executado (V-13).

## Decisões arquiteturais

### 1. Camadas com dependência em sentido único

```text
              cli            ← borda: orquestra e entrega ao humano
               │
     ┌─────────┼─────────┐
     ↓         ↓         ↓
 ingestion  analysis  backtesting
     └─────────┼─────────┘
               ↓
            domain          ← núcleo: não importa ninguém
```

Leia as setas como "importa". `domain` não importa ninguém. `ingestion`,
`analysis` e `backtesting` importam `domain` e **não importam uns aos outros**.
`cli` é o único ponto que conhece as três e as amarra.

**Nenhuma camada importa para cima.** Essa separação está correta hoje e deve
ser preservada.

Verificação rápida da regra: se um módulo de `analysis` precisar importar algo
de `ingestion`, ou se `domain` precisar importar qualquer coisa do projeto, a
regra foi violada — o que falta provavelmente é um conceito novo em `domain`.

### 2. Domínio puro

Modelos são `@dataclass(frozen=True)` sem nenhuma dependência de I/O, de
biblioteca de imagem ou de formato de arquivo. Um modelo de domínio não sabe que
existe CSV, vídeo ou Tesseract.

### 3. Lógica de decisão como função pura

O simulador é uma função que recebe amostras e parâmetros e devolve resultado —
sem escrever arquivo, sem imprimir, sem estado global. Isso o torna testável e
substituível, e é o que sustenta a fronteira decidir/executar.

### 4. Fronteira explícita entre decidir e executar

Restrição que vem do escopo em duas fases (ver `product.md`):

> O núcleo produz **recomendação como dado**; adaptadores na borda consomem.

Em termos de código: funções de análise e de decisão retornam valores, nunca
agem. Toda saída para o mundo — imprimir, gravar arquivo, futuramente desenhar
GUI ou executar ordem — mora na borda (`cli` hoje). A GUI já prevista no README
segue o mesmo desenho: adaptador novo consumindo os mesmos serviços, não
reescrita.

### 5. Cada etapa do pipeline tem CLI própria

Os módulos de ingestão (`video_sampler`, `price_ocr`, `ocr_batch`) expõem cada
um seu `build_parser()` / `main()`. Isso permite rodar, inspecionar e depurar
cada etapa isoladamente, sem executar o pipeline inteiro. Padrão a manter em
novas etapas.

### 6. Falha explícita sobre leitura duvidosa

Princípio técnico derivado de V-06/V-07: é melhor **falhar alto** do que gravar
um valor errado em silêncio. Hoje o pipeline não cumpre isso — grava o que o
OCR devolver, sem checar confiança, faixa plausível ou salto em relação à
amostra anterior, e o parser pode casar parcialmente um texto ruidoso. Endurecer
esse caminho é trabalho previsto na spec `ocr-confiavel`.

## Convenções de código

Observadas no código atual e a seguir em código novo:

- **Type hints modernos em toda assinatura pública:** `int | None`, `list[Path]`,
  `tuple[list[BacktestTrade], MarketSample | None]`. Sem `Optional`/`List` de
  `typing`.
- **`pathlib.Path` para caminho**, nunca string. Vale também em `argparse`
  (`type=Path`).
- **f-string para interpolação imediata** em mensagens de erro e saída de CLI.
  Decidido em 18/11/2026, substituindo o uso de `.format()` que existia em todo
  o código anterior. Motivo: mais curta, mais rápida e elimina a dessincronia
  entre placeholder e argumento. Não há restrição de compatibilidade, já que o
  piso é Python 3.10.
  - **Exceção — template que é contrato:** quando o formato de uma string é
    lido de volta por outro módulo, ele não vira f-string inline. Vira um par
    de funções no mesmo lugar (`frame_name()` / `frame_seconds()`), para que
    escritor e leitor compartilhem a definição e o ida-e-volta seja testável.
    Ver "Nomenclatura" em `structure.md`.
  - **Exceção — formatação preguiçosa:** se um dia entrar `logging`, usar o
    estilo `%s` do próprio logger, que só formata se o nível estiver ativo.
  - A regra é **verificada pelo linter** (`ruff`, `UP032`), não confiada à
    revisão humana. Convenção documentada não se sustenta; convenção
    verificada sim.
- **`argparse` com `build_parser()` separado de `main()`.** `build_parser()`
  devolve o parser configurado e nada mais; `main()` faz o parse e orquestra.
  Facilita testar o parser sem executar o programa.
- **Validação de argumento no topo da função, levantando `ValueError`** com
  mensagem descritiva, antes de qualquer trabalho. Exemplos: intervalo de
  amostragem positivo, coordenadas de recorte dentro da imagem, `buy_below`
  menor que `sell_at`, taxa entre 0 e 1.
- **Erros de contexto são encadeados** com `raise ... from error`, convertendo
  falha de baixo nível em mensagem acionável (dependência ausente, binário não
  encontrado, linha de CSV inválida com número da linha).
- **Docstrings curtas, de uma linha**, só quando o nome não basta. Sem
  docstring cerimonial em função óbvia.
- **Idioma:** identificadores, docstrings e mensagens de programa em **inglês**;
  o esquema de CSV e a documentação do projeto em **português**. Ao ler ou
  escrever CSV, os nomes de coluna são os em português (ver `structure.md`).
- **Guarda `if __name__ == "__main__": main()`** em todo módulo executável.
- **Importação tardia de dependência pesada ou opcional** dentro da função que
  precisa dela, para transformar ausência em mensagem clara em vez de erro de
  importação do pacote inteiro.

## Testes

- `unittest` com classes `XTests(unittest.TestCase)`, um arquivo por área.
- Arquivos temporários via `tempfile.TemporaryDirectory()`, nunca escrita em
  caminho fixo do projeto.
- **Cobertura hoje é desigual** (V-08): estatística e simulador razoáveis;
  `csv_loader` só no caminho feliz; `parse_price` com 4 casos e nenhum ruído
  real; `prepare_price_region`, `read_price` e `ocr_batch` sem nenhum teste. E
  `test_video_sampler.py` **nem importa**, por falta de `imageio_ffmpeg` — ou
  seja, hoje nunca roda.
- **Não existe teste de regressão de OCR**, porque não existem fixtures
  rotuladas (V-02). Criá-las é pré-requisito de qualquer mudança no
  pré-processamento de imagem — sem gabarito, ajustar limiar é tiro no escuro.

## Pendências técnicas conhecidas

Não são o estado desejado. Estão aqui para não serem tomadas por convenção:

| Item | Problema | Spec prevista |
|---|---|---|
| Região de recorte fixa no código (V-03) | `(1410, 755, 1545, 805)` como padrão amarra o projeto a uma resolução, tema e layout não documentados | `captura-confiavel` |
| Binarização por limiar fixo (V-06) | Limiar único fecha o vão de alguns dígitos e produz leitura errada | `ocr-confiavel` |
| Leitura não verificada (V-07) | Sem confiança do Tesseract, sem faixa de sanidade, sem detecção de salto; padrão de preço largo demais aceita o número errado | `ocr-confiavel` |
| Domínio incompleto (V-10) | Faltam menor oferta, quantidade efetivamente preenchida, taxa, preço líquido, tempo até a venda, servidor/canal | `dominio-mercado` |
| Estatística rasa (V-11) | Sem percentis, volatilidade ou tempo em faixa — logo, sem como derivar limiar dos dados | `analise-estatistica` |
| Backtest irreal (V-09, V-12) | Compra pela média em vez da menor oferta, liquidez infinita, taxa cobrada nas duas pontas sem confirmação da regra | `backtest-realista` |
| Sem ferramental de dev (V-20) | Sem `optional-dependencies`, pytest, linter, formatador ou CI | `fundacao-projeto` |
| Acentuação no console (V-21) | Saída sai corrompida no terminal do Windows em cp1252 | `fundacao-projeto` |
| Decodificação integral do vídeo (V-22) | Percorre todos os frames para amostrar 1 a cada 10 s; tolerável nesta escala | baixa prioridade |
