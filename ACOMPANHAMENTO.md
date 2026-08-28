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

## Encontro 2 - 2026-08-26

**Etapa:** 1 - Ingestão heterogênea, metadados e indexação vetorial

### Relato individual - Patricia Oquendo Duran

- Criei arquivos .env, .gitignore
- Criem ambiente venv
- Analisei os arquivos da pasta data
- Criei um dicionário de dados para um melhor entendimentos dos arquivos. O dicionário ainda está em andamento.

### Relato individual - Diogo Oliveira Vieira

- Criei ambiente .env na minha máquina
- Pesquisas sobre como os arquivos serão utilizados e qual é a melhor maneira de implementar o RAG para realizar a leitura e a consulta desses diferentes formatos de arquivo.

### Resumo do dia (escrito em conjunto)

Definimos algumas perguntas possíveis para o RAG. Exemplos:

**vendas**

- Quais são os produtos do cliente com id xxx (para oferecer outros produtos)
- Quantas vendas foram estornadas esse mês xxx
- Quantas vendas por tipo de pagamento esse mês xxx
- Qual a forma de pagamento mais utilizada por ano
- Qual a região do país com maior faturamento
- Qual a filial do cliente xxxx com maior faturamento e menor faturamento nos últimos 3 meses

**suporte**

- Quais são os tickets abertos do cliente xxx
- Quais foram os logs gerados hoje pelo sistema

**produto**

- Quais clientes ficaram insatisfeitos com o atendimento
- Quais são as informações apresentadas no relatório dre gerencial

## **Entregamos hoje:**

- Iniciamos o projeto

## **Ficou pendente:**

- Ingestão heterogênea, metadados e indexação vetorial

## **Bloqueios em aberto:**

- Necessidade de pesquisa sobre como processar os arquivos para o RAG (tipos diferentes e com dados sensíveis)

## **Próximo passo (início do encontro 3):**

- Próximo passo: Pesquisar técnicas de processamento e processar arquivos

## **Uso de assistentes de IA:**

- Para pesquisas e geração das tabelas do dicionário de dados

---

## Encontro 3 - 2026-08-28

**Etapa:** 1 - Ingestão heterogênea, metadados e indexação vetorial

### Relato individual - Patricia Oquendo Duran

- Pesquisei sobre qual seria a melhor abordagem para processar os arquivos .txt para esse RAG. A pesquisa mostrou que seria ideal finalizar o dicionário de dados e verificar quais campos são utilizados em comum entre os arquivos e analisar quais deles seriam necessários para responder nossas perguntas e assim criar o arquivo schema da etapa 1. A pesquisa apontou também ser necessário mascarar os dados, que definirmos como sensíveis, antes de gerar os embedding do arquivo e-mails.txt por exemplo.
- Definimos que e-mail será mascarado
- Finalizei dicionário de dados
- Analisei campos para gerar o schema adequado, que será preenchido no processamento dos arquivos
- Fiz commit e pull request

### Relato individual - Diogo Oliveira

- Pesquisei as melhores abordagens para processar arquivos nos formatos CSV e JSONL, buscando definir a forma mais adequada de implementar o RAG para realizar a leitura, o processamento e a consulta das informações presentes nesses diferentes formatos.
- Definição de que os e-mails deverão ser mascarados durante o processamento.
- Finalização do dicionário de dados.
- Análise dos campos para definição do schema adequado, que será utilizado durante o processamento dos arquivos.
- commit e pull request.

### Resumo do dia (escrito em conjunto)

Pesquisamos como processar os diferentes tipos de arquivos ( txt e json) e iniciamos análise sobre quais campos farão parte do Schema da etapa 1

## **Entregamos hoje:**

Finalizamos dicionário
Geramos uma tabela para analisar quais campos os arquivos tem em comum e quais poderiam ser utilizados no schema

## **Ficou pendente:**

Geração do Schema e demais atividades da etapa 1

## **Bloqueios em aberto:**

Dificuldades na agilidade em definir e desenvolver as tarefas dessa etapa

## **Próximo passo (início do encontro 4):**

Definir os campos do schema, gerar o mesmo e processar os arquivos

## **Uso de assistentes de IA:**

Para gerar os dicionarios e tabela de comparação da utilização dos campos

---

## Encontro 4 - AAAA-MM-DD

**Etapa:** 2 - Busca híbrida e filtragem por metadados
**Etapa:** 3 - Síntese estruturada, evidência e guardrails de LGPD

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
