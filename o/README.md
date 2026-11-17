# Market Analyzer

Ferramenta modular para analisar historico de precos, testar estrategias em
dados historicos e preparar futuras fontes de coleta.

## Arquitetura

- `src/market_analyzer/domain`: modelos e contratos de negocio.
- `src/market_analyzer/ingestion`: entrada de CSV, video e OCR.
- `src/market_analyzer/analysis`: estatisticas e indicadores.
- `src/market_analyzer/backtesting`: simulacoes sem efeitos externos.
- `src/market_analyzer/storage`: persistencia local e futuros adaptadores.
- `src/market_analyzer/cli.py`: interface de linha de comando.
- `src/tests`: testes automatizados.
- `src/data`: dados locais de desenvolvimento; capturas brutas nao devem ser versionadas.

A interface grafica sera adicionada futuramente como um adaptador separado,
consumindo os mesmos servicos do nucleo.

## Execucao durante o desenvolvimento

```powershell
python -m pip install -e .
market-analyzer --help
```

O projeto ainda nao inicializa nem depende de um repositorio Git. Isso sera
feito quando a estrutura inicial estiver validada.

