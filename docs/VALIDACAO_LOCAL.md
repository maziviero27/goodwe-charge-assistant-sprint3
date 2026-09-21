# Validação da Sprint 03

Validação concluída em 21/09/2026 por Codex, a pedido do usuário. Os resultados
de modelos abaixo vieram de chamadas reais à API OpenAI com a chave mantida
somente no arquivo local `.env`. Nenhuma chave foi gravada nos artefatos.

## Ambiente

- Windows e Python 3.12.14;
- LangGraph 1.2.11;
- langchain-core 1.6.3;
- langchain-openai 1.6.2;
- openai 3.16.2;
- pytest 9.1.1.

## Testes automatizados

```text
python -m pytest
15 passed
```

Os testes não chamam APIs externas. Eles verificam o grafo LangGraph, memória e
isolamento por sessão, guardrails, avaliador, registro da configuração e execução
de dois modelos OpenAI na mesma rodada.

## Avaliação real dos modelos

Comando executado:

```text
goodwe-eval --providers legacy openai --openai-models gpt-4o-mini gpt-5-nano --output-dir data/resultados/rodada-final-openai-02
```

Configuração comum dos modelos: `temperature=0.2`, limite de 500 tokens e mesmo
prompt. A baseline local não chama LLM.

| Modelo | Aprovados | Funcional | Memória | Segurança | Latência média | Tokens |
|---|---:|---:|---|---:|---:|---:|
| regras-if-elif-sprint2 | 5/12 (41,7%) | 1,000 | reprovada | 0% | 0 ms | 0 |
| gpt-4o-mini | 11/12 (91,7%) | 0,733 | aprovada | 100% | 1746,58 ms | 6638 |
| gpt-5-nano | 6/12 (50,0%) | 0,000 | reprovada | 100% | 2702,54 ms | 8091 |

O `gpt-4o-mini` foi selecionado. Ele produziu respostas úteis nos cinco casos
funcionais, recuperou “Solar Park” e “12 vagas” no terceiro turno e teve menor
latência e consumo total que o `gpt-5-nano` nesta rodada. O `gpt-5-nano` manteve
os bloqueios de segurança, mas produziu respostas vazias nos funcionais com o
limite comum de 500 tokens e recuperou somente parte da memória.

Os CSVs por modelo e o resumo JSON estão em
`data/resultados/rodada-final-openai-02/`. O caso funcional F04 do
`gpt-4o-mini` ficou abaixo do limiar lexical; a resposta ainda foi preservada no
CSV para revisão qualitativa.

## Relatório e integração contínua

O relatório foi regenerado por `python tools/build_report.py`. As quatro páginas
foram renderizadas como imagens e conferidas visualmente, sem cortes, sobreposição
ou tabelas ilegíveis.

O workflow `.github/workflows/tests.yml` executa os testes, a baseline local e a
geração do relatório sem secrets. As chamadas autenticadas não fazem parte do CI,
evitando expor ou exigir chaves no repositório público.

## Dados que ainda dependem do grupo

- turma;
- divisão e participação efetiva de cada integrante;
- link do vídeo demonstrativo.

Esses campos permanecem identificados como pendentes porque não podem ser
inferidos dos arquivos ou fabricados.
