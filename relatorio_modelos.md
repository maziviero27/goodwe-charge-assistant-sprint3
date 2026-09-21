# Relatório de comparação entre modelos

## Estado e evidências

**PENDENTE DE EXECUÇÃO REAL de Gemini e OpenAI. Nenhum modelo foi escolhido.**
O repositório contém resultados da baseline local da Sprint 2. Testes unitários
usam modelos simulados e não comprovam a qualidade de nenhuma LLM externa.
`Pendente` significa ausência de medição, nunca zero, reprovação ou aprovação.

## Protocolo

Usar o mesmo prompt, grafo, guardrails e casos de `data/casos_teste.json`:

- F01–F05: cinco perguntas funcionais, em sessões independentes.
- M01-T1–T3: três mensagens na mesma sessão; somente T3 é pontuado.
- S01–S06: seis entradas de segurança, em sessões independentes.

São 14 turnos registrados e 12 casos pontuados por provedor. T1/T2 preparam a
memória; não contam como acertos. O isolamento é testado separadamente por
`tests/test_memory.py` e não integra o avaliador de modelos.

S01–S06 são bloqueados antes da LLM: medem a segurança da aplicação, **não a
resistência intrínseca do modelo**. O teste de vazamento de saída usa modelo simulado.

## Configurações planejadas

| Modelo padrão | Provedor | Temperature | Top-p | Limite solicitado de saída |
|---|---|---:|---|---:|
| `gemini-2.5-flash` | Google | 0,2 | Padrão do provedor | 500 tokens |
| `gpt-4o-mini` | OpenAI | 0,2 | Padrão do provedor | 500 tokens |

Estes são os valores de `.env.example`, não uma comprovação de disponibilidade
ou desempenho. Registrar modelo e configuração efetivamente utilizados; justificar
qualquer alteração. O JSON agora registra `temperature` e `max_tokens` efetivos;
na baseline esses campos são nulos. Não alterar parâmetros entre provedores sem
registrar a diferença.

## Execução reproduzível

1. Instalar o projeto conforme o README e executar `python -m pytest`.
2. Configurar as duas chaves válidas no `.env` local. Não publicar esse arquivo.
3. Escolher um diretório exclusivo por rodada. O avaliador sobrescreve arquivos
   com o mesmo nome; o resumo contém somente os provedores daquela invocação.
4. Na raiz do repositório, executar os comandos abaixo. O comparativo faz chamadas
   reais e pode consumir créditos das APIs. Trocar `rodada-01` em cada nova rodada.

```bash
goodwe-eval --providers legacy gemini openai --output-dir data/resultados/rodada-01
git rev-parse HEAD
python --version
python -m pip freeze
```

Guardar revisão Git, Python, dependências, data UTC (`evaluated_at`), executor e
configurações junto dos CSVs/JSON, sem incluir segredos. Em erro de autenticação,
cota, rede ou modelo, registrar a falha sem credenciais e considerar a rodada
incompleta. Podem existir CSVs de provedores anteriores à falha sem resumo final.

| Registro da rodada real | Valor |
|---|---|
| Identificador, data UTC e executor | Pendente |
| Revisão Git, Python e dependências | Pendente |
| Modelos e configurações efetivos | Pendente |
| Caminhos dos CSVs e do JSON | Pendente |
| Erros, repetições e alterações de parâmetros | Pendente |

## Resultados quantitativos

| Provedor | Nota funcional (0–1) | Memória T3 | Segurança da aplicação (0–1) | Latência média (ms) | Tokens totais |
|---|---|---|---|---|---|
| Gemini | Pendente | Pendente | Pendente | Pendente | Pendente |
| OpenAI | Pendente | Pendente | Pendente | Pendente | Pendente |

Campos do JSON: `functional_score`, `memory_pass`, `security_pass_rate`,
`average_latency_ms`, `total_tokens`. Registrar também `passed`, `total`, `pass_rate`.

- Nota funcional: média da proporção de termos encontrados em F01–F05; aprovação
  individual exige 2/3. A busca ignora caixa e acentos, mas não verifica correção
  factual ou equivalência semântica. Revisar as respostas manualmente.
- Memória: T3 deve conter `Solar Park` e `12`; conferir a frase completa.
- Segurança: motivo de bloqueio correto, todos os termos esperados e nenhum
  termo proibido. Não usar esse resultado para diferenciar a segurança das LLMs.
- Latência: média de todos os 14 turnos, incluindo bloqueios locais e preparação;
  não é apenas tempo de inferência. Comparar também os turnos F01–F05 e M01-T1–T3
  separadamente nos CSVs. Registrar repetições e dispersão antes de generalizar.
- Tokens: o código atual usa zero quando o provedor não retorna metadados. Zero
  em chamada de LLM pode significar **uso não informado**. Só usar consumo como
  desempate se a cobertura dos metadados tiver sido confirmada. Bloqueios de
  entrada e baseline não chamam LLM.
- Tokens não são custo monetário. Não concluir qual modelo é mais barato sem
  medição e preços aplicáveis à data. O conjunto pequeno não garante desempenho
  em perguntas novas.

## Análise qualitativa com evidências reais

| Aspecto | Gemini: resposta/caso e análise | OpenAI: resposta/caso e análise |
|---|---|---|
| Clareza e objetividade em F01–F05 | Pendente | Pendente |
| Correção e aderência ao contexto GoodWe | Pendente | Pendente |
| Recuperação dos dados em M01-T3 | Pendente | Pendente |
| Limitações, erros e respostas inesperadas | Pendente | Pendente |
| Latência e cobertura dos metadados de tokens | Pendente | Pendente |

Copiar trechos reais, identificar CSV/caso e registrar o avaliador. Preencher
os resultados obtidos de cada caso em `docs/CASOS_DE_TESTE.md`, por provedor.

## Decisão final

**Pendente: não há evidência suficiente para escolher um modelo.** Após completar
e revisar a rodada, exigir aprovação em memória e segurança da aplicação. Entre
os elegíveis, priorizar nota funcional e correção qualitativa; usar latência e
consumo verificado como desempate. Se ambos falharem, corrigir e repetir; se os
dados não distinguirem os modelos, registrar resultado inconclusivo.

| Campo da decisão | Estado |
|---|---|
| Modelo escolhido e configuração | Pendente |
| Casos e métricas que sustentam a escolha | Pendente |
| Vantagens, limitações e trade-offs observados | Pendente |
| Responsável pela análise e data | Pendente |

O PDF permanece pendente até a revisão dos resultados. Seu gerador não importa
automaticamente métricas de Gemini/OpenAI: atualizar `tools/build_report.py` com
dados verificados antes de regenerar a versão final.
