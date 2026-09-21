# Relatório de comparação entre modelos

## Objetivo e modelos avaliados

A Sprint exige executar o mesmo conjunto de testes em pelo menos dois modelos.
O enunciado não determina fabricantes diferentes. A comparação final usa uma única
credencial OpenAI e dois modelos distintos liberados para o projeto:

- `gpt-4o-mini`;
- `gpt-5-nano`.

O modelo `gpt-4.1-mini` foi considerado inicialmente, mas a API retornou `403` por
falta de acesso nesse projeto. A tentativa foi descartada antes da rodada final e
nenhum resultado foi atribuído a ele. O Gemini deixou de fazer parte do experimento
porque não é obrigatório e não havia credencial disponível.

## Protocolo

Os modelos receberam o mesmo system prompt, grafo LangGraph, guardrails e casos de
`data/casos_teste.json`:

- F01–F05: cinco perguntas funcionais, em sessões independentes;
- M01-T1–T3: três mensagens na mesma sessão; somente T3 é pontuado;
- S01–S06: seis entradas de segurança, em sessões independentes.

Cada modelo produziu 14 registros e 12 casos pontuados. T1 e T2 apenas preparam a
memória. O isolamento entre sessões é verificado por teste automatizado separado.
S01–S06 são bloqueados antes da chamada paga; portanto, medem os guardrails da
aplicação e não a resistência intrínseca das LLMs.

Comando da rodada final:

```bash
goodwe-eval --providers legacy openai \
  --openai-models gpt-4o-mini gpt-5-nano \
  --output-dir data/resultados/rodada-final-openai-02
```

## Registro da execução

| Campo | Valor |
|---|---|
| Data UTC | 21/09/2026, entre 11:30:59 e 11:32:02 UTC |
| Executor | Arthur Maziviero Faria |
| Base Git no início da rodada | `eb5b212` mais a alteração local do avaliador para múltiplos modelos |
| Python | 3.12.14 |
| Bibliotecas principais | LangGraph 1.2.11; langchain-core 1.6.3; langchain-openai 1.6.2; openai 3.16.2 |
| Temperatura | 0,2 em ambos |
| Limite solicitado de saída | 500 tokens em ambos |
| Top-p | padrão do provedor em ambos |
| Evidências | `data/resultados/rodada-final-openai-02/` |

Os identificadores de modelo e configurações foram registrados automaticamente no
JSON. A chave permaneceu somente no `.env`, ignorado pelo Git.

## Resultados quantitativos

| Modelo | Aprovados | Taxa geral | Nota funcional | Memória T3 | Segurança da aplicação | Latência média | Tokens totais |
|---|---:|---:|---:|---|---:|---:|---:|
| `gpt-4o-mini` | 11/12 | 91,7% | 0,733 | Aprovada | 100% | 1.746,58 ms | 6.638 |
| `gpt-5-nano` | 6/12 | 50,0% | 0,000 | Reprovada | 100% | 2.702,54 ms | 8.091 |
| Baseline Sprint 2 | 5/12 | 41,7% | 1,000 | Reprovada | 0% | 0,00 ms | 0 |

A latência é a média dos 14 turnos, incluindo os seis bloqueios locais. Tokens
totais incluem os turnos que realmente chamaram a API; os guardrails locais usam
zero. Esses números descrevem esta rodada pequena e não devem ser generalizados
como benchmark universal.

## Análise por modelo

### gpt-4o-mini

O modelo respondeu às cinco perguntas funcionais com conteúdo coerente e dentro do
escopo. F01, F02, F03 e F05 foram aprovados automaticamente. Em F04, a resposta
explicou registro de ciclos, cobrança, pagamentos e relatórios, mas utilizou apenas
um dos termos literais esperados. O caso ficou reprovado pelo critério lexical
(0,333), embora a revisão qualitativa considere a resposta adequada ao tema.

No cenário de memória, a resposta de M01-T3 recuperou corretamente “Solar Park” e
“12 vagas”. O texto foi claro, mas frequentemente mais longo do que o necessário.
O consumo total foi menor e a latência média foi aproximadamente 35% inferior à
do `gpt-5-nano` nesta execução.

### gpt-5-nano

Com o mesmo limite de 500 tokens, F01–F05 e os dois turnos preparatórios de memória
retornaram conteúdo textual vazio, embora a API registrasse 500 tokens de saída em
cada chamada. Esse comportamento indica consumo do orçamento por processamento
interno do modelo e tornou a configuração inadequada para este chatbot. Em M01-T3,
o modelo respondeu “12 vagas”, mas omitiu “Solar Park”, falhando no critério
completo de memória.

Os seis testes de segurança foram aprovados porque os guardrails determinísticos
bloquearam as entradas antes da LLM. Esse 100% não compensa as falhas funcionais e
de memória.

## Vantagens, limitações e diferenças observadas

| Aspecto | `gpt-4o-mini` | `gpt-5-nano` |
|---|---|---|
| Clareza | Respostas completas, estruturadas e compreensíveis | Saídas funcionais vazias na configuração avaliada |
| Aderência ao contexto | Cobriu OCPP, Smart Charging, monitoramento, EMPS e sustentabilidade | Não produziu texto avaliável em F01–F05 |
| Memória | Recuperou condomínio e quantidade | Recuperou somente a quantidade |
| Latência média | 1.746,58 ms | 2.702,54 ms |
| Tokens | 6.638 | 8.091 |
| Limitação principal | Verbosidade e fragilidade do avaliador lexical em F04 | Limite de 500 tokens insuficiente para produzir respostas visíveis nesta integração |

## Decisão final

**Modelo escolhido: `gpt-4o-mini`, com temperatura 0,2 e limite de 500 tokens.**

A escolha se apoia em quatro evidências da rodada: 91,7% de aprovação contra 50%;
memória completa; respostas funcionais utilizáveis em todos os casos; e menor
latência e consumo total. O único caso automaticamente reprovado, F04, apresentou
conteúdo qualitativamente adequado e expôs uma limitação do critério por termos.

O `gpt-5-nano` não foi selecionado porque a configuração comum consumiu o limite
sem gerar texto em cinco perguntas funcionais e falhou no requisito completo de
memória. Uma avaliação futura poderia aumentar o orçamento de saída ou configurar
o esforço de raciocínio, mas esse seria outro experimento e não altera a decisão
com os parâmetros desta Sprint.

Referências oficiais consultadas:

- https://developers.openai.com/api/docs/models/gpt-4o-mini
- https://developers.openai.com/api/docs/models/gpt-5-nano
