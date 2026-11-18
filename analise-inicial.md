# Análise inicial — Algodão de isolamento acústico

## Objetivo

Criar uma base histórica para identificar momentos de preço baixo, estimar a volatilidade e testar uma estratégia de compra e venda simulada.

## Fonte analisada

- **Vídeo:** `Variação market 2026-11-16 125917.mp4`
- **Local:** mesma pasta deste documento
- **Duração:** aproximadamente 192,5 segundos
- **Amostragem inicial:** 1 frame a cada 10 segundos
- **Quantidade de amostras:** 20
- **Tela:** detalhes do item no mercado, com faixa de preço e preço unitário médio

## Série observada

| Tempo | Preço unitário médio |
|---:|---:|
| 00s | 171.453 |
| 10s | 120.273 |
| 20s | 120.273 |
| 30s | 120.273 |
| 40s | 140.745 |
| 50s | 120.273 |
| 60s | 120.273 |
| 70s | 156.099 |
| 80s | 140.745 |
| 90s | 110.037 |
| 100s | 110.037 |
| 110s | 171.453 |
| 120s | 171.453 |
| 130s | 220.074 |
| 140s | 220.074 |
| 150s | 140.745 |
| 160s | 220.074 |
| 170s | 120.273 |
| 180s | 199.602 |
| 190s | 199.602 |

## Observações preliminares

- **Mínimo observado:** 110.037.
- **Máximo observado:** 220.074.
- **Amplitude observada:** 110.037.
- O preço permaneceu em algumas faixas por mais de uma atualização de 10 segundos.
- Houve retornos rápidos para valores acima de 170.000.
- As duas linhas de valor na tela representam preço unitário e total para quantidade 1; não devem ser contadas como duas observações.
- A série ainda é pequena e representa apenas uma sessão de aproximadamente três minutos.
- Os valores foram transcritos a partir dos frames; o OCR automático ainda não foi aplicado.

## Hipóteses para teste

Estas são apenas hipóteses iniciais, não regras definitivas:

- Faixa de oportunidade forte: preço abaixo de 130.000.
- Faixa de oportunidade moderada: entre 130.000 e 160.000.
- Faixa de referência alta: acima de 190.000.
- O preço de venda precisa considerar taxas, tempo de permanência e disponibilidade real.
- Uma compra só deve ser considerada quando houver margem líquida suficiente sobre o preço de referência.

## Dados que ainda precisam ser coletados

Para cada atualização do mercado:

- data e hora real;
- preço unitário médio;
- menor oferta disponível;
- maior oferta ou faixa superior visível;
- quantidade disponível em cada faixa;
- preço de venda/contato, se disponível;
- taxas e comissão;
- quantidade comprada ou vendida;
- tempo até a venda;
- resultado líquido;
- servidor, região ou canal, se aplicável;
- identificação da gravação de origem.

## Formato futuro recomendado

Cada leitura deve poder ser armazenada com estas colunas:

```text
timestamp,item,preco_medio,menor_oferta,maior_oferta,
quantidade_disponivel,taxa,preco_liquido,origem_video,observacao
```

## Próximos passos

1. Repetir gravações em horários diferentes e em dias diferentes.
2. Extrair frames automaticamente a cada 10 segundos.
3. Aplicar OCR somente nas regiões de preço e quantidade.
4. Validar o OCR manualmente contra uma amostra dos frames.
5. Salvar os dados em CSV ou SQLite.
6. Calcular mediana, percentis, volatilidade e tempo em cada faixa.
7. Fazer backtesting com compra e venda simuladas.
8. Definir limites de risco antes de qualquer ação em ambiente real.

## Limitações

Esta análise observa apenas a tela gravada. Ela não confirma o funcionamento interno do mercado, não mede todas as ofertas entre duas atualizações e não comprova que uma oferta permaneceria disponível tempo suficiente para ser adquirida.
