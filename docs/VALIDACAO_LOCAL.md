# Validação local da revisão

Validação realizada em 20/09/2026 por Codex, a pedido do usuário. Não atribui
autoria, execução manual ou participação acadêmica a nenhum integrante.

Base da revisão: commit `33decaf` do repositório original. O núcleo LangGraph,
os prompts, os adaptadores e os casos JSON foram preservados.

## Ambiente

- Windows, Python 3.12.14; ambiente virtual novo, instalado com `pip install -e ".[dev]"`.
- langgraph 1.2.11; langchain-core 1.6.3; langchain-openai 1.6.2.
- langchain-google-genai 4.4.0; pytest 9.1.1; reportlab 5.0.1.
- Nenhuma chamada de Gemini/OpenAI; testes com modelos simulados e baseline local.

## Comandos e resultados obtidos

```text
python -m pytest
14 passed

goodwe-eval --providers legacy --output-dir tmp/validacao-legacy
legacy/regras-if-elif-sprint2: 5/12 (41.7%)
```

Os 12 testes originais verificam memória, isolamento, guardrails e comportamento
legado. Os dois testes novos verificam a contagem do avaliador e o registro da
configuração efetiva via CLI, usando um modelo simulado.

A baseline gerou 14 registros: cinco funcionais aprovados, terceiro turno de
memória reprovado e seis casos de segurança reprovados. Os dois primeiros turnos
de memória são preparação e não entram nos 12 pontuados. Isso reproduz as taxas
do arquivo histórico `data/resultados/resumo_modelos.json`, preservado sem alterações.
Os novos arquivos temporários não substituem as evidências históricas.

O relatório foi regenerado por `python tools/build_report.py` e suas quatro
páginas foram renderizadas e conferidas visualmente. Gemini/OpenAI continuam
marcados como pendentes. Nenhuma métrica ou escolha de LLM foi acrescentada.

## Limites e pendências

- CI preparada em `.github/workflows/tests.yml`, sem secrets de provedores.
  Execução no GitHub ainda não confirmada; aprovação local não é aprovação remota.
- Acesso de escrita ao GitHub é necessário para publicar esta revisão.
- Comparativo real: chaves válidas, acesso aos modelos, execução, análise e decisão.
- Turma, participação de cada integrante e link do vídeo: confirmação pelo grupo.
- Resultados de modelos reais exigem atualização posterior do relatório Markdown
  e do gerador/PDF, mantendo os CSVs e a configuração da rodada como evidências.
