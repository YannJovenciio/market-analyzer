# Produto — Market Analyzer

## Propósito

Ler o mercado de um jogo a partir de **gravações de tela**, extrair os preços por
OCR, montar uma série histórica e analisar **quando um item está barato o
bastante para valer a compra**.

A ferramenta observa a tela gravada. Ela não acessa o jogo, não consulta API e
não tem visibilidade do que acontece entre duas atualizações do mercado. Toda
conclusão que ela produz é derivada do que foi visto no vídeo — e essa limitação
é parte do produto, não um detalhe de implementação.

## Valor

Preço de item em mercado de jogo oscila bastante e rápido. Olhar a tela e
decidir "no olho" não escala e não deixa registro. O valor da ferramenta é
transformar observação casual em **série histórica com limiares derivados dos
próprios dados**, para que a decisão de comprar deixe de ser palpite.

## Escopo: duas fases (decidido em 18/11/2026)

Esta é a **restrição central do produto**. Toda decisão de design responde a ela.

| Fase | Escopo | Estado |
|---|---|---|
| **Fase 1 — Observador** | Capturar, ler por OCR, registrar, analisar e **recomendar**. A execução da compra fica com o humano. | Em andamento |
| **Fase 2 — Executor** | Dar ao programa a capacidade de executar a compra. | Adiada até a Fase 1 estar confiável |

**Por que faseado:** a Fase 1 concentra todo o trabalho difícil e todo o valor —
ler a tela com confiabilidade, modelar menor oferta e quantidade, derivar
limiares dos dados e ter um backtest que não minta. Executar é trivial depois
disso. O caminho inverso produziria um bot executando decisões que ainda não se
sabe se são boas.

### Fronteira entre decidir e executar

Regra arquitetural que vale para **toda** funcionalidade da Fase 1:

> O núcleo produz uma **recomendação como dado**. Quem consome essa recomendação
> é um **adaptador na borda** — hoje a CLI que imprime, amanhã uma GUI, e só
> então, eventualmente, um executor.

Consequência prática: nenhum código de decisão pode agir. Se um módulo de
análise chamar algo que mexe no mundo, a fronteira foi violada. Assim a Fase 2
vira um adaptador novo, não uma reescrita.

**Risco reconhecido:** fasear **adia** a questão de termos de serviço da Fase 2,
não a elimina. Entrar na Fase 2 deve ser uma decisão retomada explicitamente,
nunca herdada por inércia.

## Capacidades centrais (Fase 1)

1. **Capturar** — amostrar frames de uma gravação em intervalo fixo.
2. **Ler** — extrair o preço por OCR de uma região recortada do frame.
3. **Registrar** — gravar a série em CSV com timestamp, item e origem.
4. **Analisar** — estatísticas descritivas sobre a série.
5. **Simular** — backtest de uma estratégia de compra e venda.
6. **Recomendar** — apresentar o resultado ao humano, que decide e age.

## Princípios de produto

- **Falhar alto é melhor que registrar errado.** Um preço silenciosamente
  incorreto contamina toda a série e todas as conclusões derivadas dela. Diante
  de uma leitura duvidosa, a resposta correta é erro explícito, não o
  melhor palpite.
- **Limiar vem dos dados, não da intuição.** Qualquer faixa de "barato" ou
  "caro" precisa ser derivada da distribuição observada. Limiar escolhido à mão
  acerta no passado e erra no futuro.
- **Um número só vale se significar algo.** Resultado de simulação sem
  premissa declarada é ficção com aparência de medição.
- **A limitação do método é documentada junto com o resultado.** O hábito já
  existe em `analise-inicial.md` e deve ser mantido.

## Estado real (não presuma que funciona)

Documentado em `validacao-inicial.md` (18/11/2026), 23 achados catalogados:

- **O OCR erra em 25% das amostras** — 5 de 20 divergem da transcrição manual
  (V-06). Confusões de dígito típicas de binarização com limiar fixo.
- **Nenhuma leitura é verificada** (V-07) — a confiança reportada pelo Tesseract
  é ignorada, não há faixa de sanidade nem detecção de salto.
- **O material bruto não existe mais** (V-01) — o vídeo-fonte foi gravado na
  pasta temporária da Ferramenta de Captura do Windows e foi apagado pelo
  sistema. Não há frames salvos nem fixtures rotuladas (V-02).
- **O backtest atual produz um número sem significado** (V-09) — compra pelo
  preço médio em vez da menor oferta, assume liquidez infinita e usa limiares
  sobreajustados a 20 amostras de 3 minutos.
- **O ambiente não está instalado** (V-13) — `pytesseract`, `imageio_ffmpeg` e o
  binário do **Tesseract** estão ausentes.

A série de referência existente tem **20 amostras cobrindo 3 minutos de uma
única sessão**. Ela serve para exercitar o pipeline, não para concluir nada
sobre o mercado.

## Perguntas em aberto

Estes pontos são **desconhecidos**. Não devem ser inferidos, chutados nem
tratados como resolvidos em nenhuma spec até resposta humana:

- **Qual é a regra de taxa do mercado?** Só a venda é taxada, ou compra e venda?
  Percentual fixo? Tem piso ou teto? (H-2 / V-12 — o simulador hoje cobra nas
  duas pontas, sem confirmação.)
- **O que a tela realmente mostra?** Exibe a menor oferta individual e a
  quantidade disponível, ou apenas a faixa de preço e a média? Isso define se o
  modelo de domínio expandido é viável por OCR. (H-3 / V-10)
- **Qual resolução e tema de UI foram usados na gravação?** A região de recorte
  depende disso e hoje está fixa no código, sem contexto. (H-4 / V-03)
- **Qual é o jogo**, e quais são as regras do seu mercado. Não documentado.

## Divisão de trabalho

O projeto é tocado em dupla, com um critério simples: **o que só um humano com
acesso ao jogo pode fazer fica com o dono do projeto; o resto fica com a IA.**

- **Humano (H-1 a H-7):** gravar material novo, rotular fixtures, responder as
  perguntas em aberto, instalar o Tesseract, aprovar cada fase do SDD.
- **IA (C-1 a C-7):** estrutura, ambiente, condução do SDD, endurecimento do
  OCR, expansão de domínio/estatística/simulador, testes.

Os dois lados correm em paralelo. Nada do que a IA faz hoje depende das
gravações; nada do que o humano faz hoje depende do código. Detalhe completo na
seção 7 de `validacao-inicial.md`.

## Roteiro de especificações

```text
fundacao-projeto ──┬─→ captura-confiavel ──→ ocr-confiavel ───┐
                   │                                          ├─→ backtest-realista
                   └─→ dominio-mercado ──→ analise-estatistica┘
```

`fundacao-projeto` é a única sem bloqueio e é o ponto de partida.
