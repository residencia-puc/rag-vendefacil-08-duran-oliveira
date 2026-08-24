# Acompanhamento - Mini Desafio RAG VendeFácil

**Integrante 1:** Patricia Oquendo Duran - [@patriciaduran](https://github.com/patriciaduran)
**Integrante 2:** Diogo Oliveira Vieira - [@Diogooliveira10](https://github.com/Diogooliveira10)

**Repositório:** `rag-vendefacil-08-duran-oliveira`

---

## Como preencher

- Um bloco por encontro, em **ordem cronológica** - o encontro mais recente vai no **fim** do arquivo.
- O relato individual é escrito **pelo próprio integrante**, em primeira pessoa. Não escreva pelo colega.
- Escrever entre **17:30 e 17:40**. `commit` + `push` até as **18:00**, mesmo que o dia não tenha fechado.
- Mensagem de commit: `acompanhamento: AAAA-MM-DD`

**Um relato útil responde:** o que eu implementei, qual decisão técnica eu tomei e por quê, onde travei, e como (ou se) resolvi.

<details>
<summary>Exemplo de relato individual bom × ruim</summary>

❌ _"Trabalhei na parte de ingestão junto com meu colega. Avançamos bastante e conseguimos carregar os arquivos."_

✅ _"Implementei os loaders de CSV e JSONL em `src/ingest.py`. Decidi serializar cada linha do `customers.csv` como frase em linguagem natural em vez de manter o formato separado por vírgula, porque nos primeiros testes de similaridade os chunks CSV crus não recuperavam nada - o embedding não separa campo de valor. Travei ~40 min no `tickets.jsonl`: o `state` estava indo para o texto do chunk mas não para os metadados, então o filtro voltava vazio. Resolvi movendo a extração para antes da criação do `Document`. Usei o Claude para gerar o esqueleto do parser de JSONL; ajustei o schema de metadados na mão."_

</details>

---

## Encontro 1 - 2026-08-24

**Etapa:** 1 - Ingestão heterogênea, metadados e indexação vetorial

### Relato individual - Patricia Oquendo Duran

- Aceitei convite para organização "residencia-puc"
- Clonei repositório
- Configurei minha identidade (nome e e-mail)
- Iniciei arquivo ACOMPANHAMENTO.md
- Criei branch feature/puc1
- Fiz Pull Request para main

### Relato individual - Diogo Oliveira

- Criei da Organization
- Fiz o Fork do repositório base
- Adicionei os membros para o repositória
- CClonei repositório
- Configurei minha identidade (nome e e-mail)
- Iniciei arquivo ACOMPANHAMENTO.md
- Criei branch feature/puc2
- Fiz Pull Request para main

### Resumo do dia (escrito em conjunto)

## **Entregamos hoje:**

- Ambiente configurado para iniciarmos o projeto.

## **Ficou pendente:**

- Iniciar a primeira etapa do projeto.

## **Bloqueios em aberto:**

-

## **Próximo passo (início do encontro 2):**

- Realizar a etapa 1 e dividir as tarefas do grupo.

## **Uso de assistentes de IA:**

- Até o momento não foi utilizada.

---

## Encontro 2 - AAAA-MM-DD

**Etapa:** 2 - Busca híbrida e filtragem por metadados

### Relato individual - [Nome do Integrante 1]

### Relato individual - [Nome do Integrante 2]

### Resumo do dia (escrito em conjunto)

## **Entregamos hoje:**

## **Ficou pendente:**

## **Bloqueios em aberto:**

## **Próximo passo (início do encontro 3):**

## **Uso de assistentes de IA:**

---

## Encontro 3 - AAAA-MM-DD

**Etapa:** 3 - Síntese estruturada, evidência e guardrails de LGPD

### Relato individual - [Nome do Integrante 1]

### Relato individual - [Nome do Integrante 2]

### Resumo do dia (escrito em conjunto)

## **Entregamos hoje:**

## **Ficou pendente:**

## **Bloqueios em aberto:**

## **Próximo passo (início do encontro 4):**

## **Uso de assistentes de IA:**

---

## Encontro 4 - AAAA-MM-DD

**Etapa:** 4 - Avaliação (RAG Triad), interface e relatório

### Relato individual - [Nome do Integrante 1]

### Relato individual - [Nome do Integrante 2]

### Resumo do dia (escrito em conjunto)

## **Entregamos hoje:**

## **Ficou pendente:**

## **Bloqueios em aberto:**

## **Preparação para o Demo Day:**

## **Uso de assistentes de IA:**

---

_TIC em Trilhas · PUC-Rio · Instituto ECOA · MCTI Futuro · Softex_
