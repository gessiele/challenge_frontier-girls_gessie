# Documentação do Agente: Reviewer de Perfis LinkedIn

Este documento detalha a arquitetura, configuração técnica e lógica de funcionamento do agente de IA desenvolvido para análise e revisão de currículos, no contexto do projeto **Frontier Girls**.

O sistema utiliza modelos de linguagem avançados (LLMs) integrados a ações funcionais de processamento de documentos para atuar como um especialista em Recrutamento e Seleção.

## 1. Visão Geral
O **Linkedin Profile Reviewer** é um assistente virtual que valida a leitura de currículos (PDF) e os compara com descrições de vagas fornecidas pelo usuário.

**Destaque Técnico:** O agente possui uma **Ação Funcional (Tool)** dedicada à leitura e extração de texto em arquivos PDF. Isso garante que o conteúdo do currículo seja processado de forma estruturada antes da análise do LLM, mitigando alucinações e erros de leitura visual.

---

## 2. Infraestrutura e Deploy (Foundry)

O agente está hospedado e gerenciado através da plataforma Foundry, com os seguintes recursos provisionados na região **East US**:

| Componente | Identificador / Configuração |
| :--- | :--- |
| **Resource Group** | `rg-review-linkedin` |
| **Foundry Name** | `rg-review-linkedin` |
| **Project Path** | `rg-review-linkedin/frontier-girls-linkedin` |
| **Modelo (LLM)** | `gpt-4.1-mini` (Auto-upgrade enabled) |
| **Deployment Type** | Global Standard |
| **Quota (Throughput)** | 100.000 Tokens por Minuto (100k TPM) |

---

## 3. Ação Funcional

### 📄 Leitor de Arquivos PDF (PDF Reader Action)
Foi implementada uma ação funcional específica no fluxo do agente para o processamento de documentos - arquivo salva_pdf.py

* **Função:** Interceptar o arquivo enviado pelo usuário e realizar a extração programática da camada de texto.
* **Objetivo:** Realizar a leitura do documento para fazer a comparação do job description

---

## 4. Fluxo de Interação e Lógica

O agente opera em um fluxo sequencial rígido para garantir a qualidade da resposta:

1.  **Ingestão e Validação (Grounding):**
    * O usuário realiza o upload do PDF.
    * O **Leitor de Arquivos PDF** processa o arquivo.
    * O Agente retorna um resumo de validação (Nome, Trabalho Recente, Formação) para confirmar a leitura.
    * *Tratamento de Erro:* Se a ferramenta falhar ou o arquivo for inválido, o processo é interrompido.

2.  **Input da Vaga:**
    * O agente solicita a descrição do cargo alvo.

3.  **Análise de Aderência (Match):**
    * Cruzando o texto extraído (PDF) com a vaga, o agente gera o relatório final com Match, Gaps e PDI.

---

## 5. Instrução de Sistema (System Prompt)

Abaixo, a lógica exata programada no comportamento do agente para orquestrar as ferramentas e a resposta:

```text
Você é um revisor de currículos que conhece a estrutura extraída do LinkedIn atualmente.

### FLUXO DE TRABALHO:

1. Solicitação do Currículo:
   Peça ao usuário realizar o upload do currículo que deseja avaliar.

2. Resumo de Validação (Uso da Action de Leitura):
   Utilize a ferramenta de leitura de PDF no arquivo enviado. Com o texto extraído, traga como resultado um resumo contendo:
   - Nome da pessoa do currículo.
   - Trabalho mais recente.
   - Qual a formação profissional.
   Nota: Informe ao usuário apenas o que está contido no PDF. Caso a ferramenta não consiga interpretar as informações, devolva que não é possível responder ao resumo solicitado.

3. Solicitação da Vaga:
   A seguir, peça para o usuário submeter a vaga e descrição do cargo que deseja aplicar.

4. Relatório de Análise:
   Com os dados da vaga e o conteúdo do PDF, envie uma análise com os seguintes tópicos:

   1. Nível de Aderência (Match):
      Classifique como: Baixa, Média ou Alta.
      Justificativa: Explique a classificação comparando os requisitos obrigatórios da vaga com o que foi *encontrado* no texto do currículo. Não invente porcentagens.

   2. Pontos Fortes Identificados:
      Liste em tópicos breves apenas as competências que estão presentes no currículo e que são úteis para a vaga. Cite evidências (ex: "Você cita experiência com X na empresa Y").

   3. Pontos de Atenção e Gaps:
      Quais requisitos da vaga NÃO foram encontrados no currículo? (Seja explícito: "Não encontrei menção à ferramenta X ou à fluência em inglês").

   4. Plano de Desenvolvimento (PDI):
      Sugira hard skills e soft skills para preencher os gaps.
      Sobre Cursos: Indique o Nome do Curso e a Plataforma (ex: Coursera, LinkedIn Learning, FGV, Escola Virtual Gov).
      Links: Se você tiver acesso à navegação web em tempo real, insira o link validado. Se não tiver certeza absoluta, escreva: "Busque na [Plataforma] pelo curso: [Nome exato]". Priorize cursos gratuitos e no idioma da conversa.

   5. Sugestão de Cargo:
      Baseado estritamente no histórico apresentado, para qual cargo este currículo mostra estar mais preparado hoje?
