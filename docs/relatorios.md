# App `relatorios`

Este documento descreve como funciona o app `apps/relatorios`, como os relatórios são montados e como alterar layouts de PDF com segurança.

## 1. Visão geral

O app `relatorios` é responsável por:

- gerar relatórios tabulares em **PDF** e **XLSX**;
- gerar o PDF oficial de **encaminhamento individual**;
- aplicar filtros vindos da query string (`GET`);
- restringir acesso por perfil para relatórios administrativos.

Fluxo padrão:

1. view recebe requisição (`apps/relatorios/views.py`);
2. extrai filtros via `_extrair_filtros`;
3. chama função de dados em `apps/relatorios/reports/*.py`;
4. chama serviço de saída (`services/pdf.py` ou `services/xlsx.py`);
5. devolve `HttpResponse` com `Content-Disposition: attachment`.

## 2. Arquitetura por pastas

- `apps/relatorios/urls.py`: rotas dos relatórios.
- `apps/relatorios/views.py`: orquestra filtros, permissões, geração e resposta HTTP.
- `apps/relatorios/reports/`: consulta ORM e monta `colunas` + `linhas`.
- `apps/relatorios/services/pdf.py`: layout padrão de PDF tabular e documento simples.
- `apps/relatorios/services/encaminhamento_pdf.py`: layout completo do PDF oficial de encaminhamento.
- `apps/relatorios/services/xlsx.py`: layout padrão de XLSX.

## 3. Rotas disponíveis

Prefixo geral no projeto: `core/urls.py` registra `path('relatorios/', include('apps.relatorios.urls'))`.

Rotas finais:

- `GET /relatorios/alunos/pdf/`
- `GET /relatorios/alunos/xlsx/`
- `GET /relatorios/encaminhamentos/pdf/`
- `GET /relatorios/encaminhamentos/xlsx/`
- `GET /relatorios/encaminhamento/<pk>/pdf/`
- `GET /relatorios/horas/pdf/`
- `GET /relatorios/horas/xlsx/`
- `GET /relatorios/horas-por-aluno/pdf/`
- `GET /relatorios/horas-por-aluno/xlsx/`
- `GET /relatorios/consolidado/pdf/`

## 4. Controle de acesso

### 4.1 Decorators

Em `apps/relatorios/views.py`:

- `@login_required`: exige autenticação.
- `@relatorios_required`: só permite `superuser`, `DIRETOR` ou `ADMINISTRATIVO`.

### 4.2 Exceção importante

A view `encaminhamento_pdf(request, pk)` usa apenas `@login_required` (não usa `@relatorios_required`).

## 5. Como os dados são montados

Cada função em `apps/relatorios/reports/` retorna:

- `colunas`: lista com cabeçalhos;
- `linhas`: lista de listas (cada sublista = uma linha da tabela).

Funções:

- `relatorio_alunos_dados(filtros)`
- `relatorio_encaminhamentos_dados(filtros)`
- `relatorio_horas_dados(filtros)`
- `relatorio_horas_por_aluno_dados(filtros)`
- `relatorio_consolidado_dados()`

## 6. Filtros suportados

Extração central: `_extrair_filtros(request, campos)` em `views.py`.

### 6.1 Alunos

- `q`
- `matricula`
- `curso`
- `situacao`

### 6.2 Encaminhamentos

- `data_inicio`
- `data_fim`

### 6.3 Horas (detalhado)

- `data_inicio`
- `data_fim`
- `aluno_id`

### 6.4 Horas por aluno

- `data_inicio`
- `data_fim`

### 6.5 Consolidado

- sem filtros.

## 7. Geração de PDF tabular (layout padrão)

Arquivo: `apps/relatorios/services/pdf.py`, função `gerar_pdf_tabela(...)`.

Características principais:

- página `A4` em `portrait` (padrão) ou `landscape`;
- título com `Paragraph`;
- tabela com `repeatRows=1` (cabeçalho repete em quebra de página);
- estilo com `TableStyle`:
  - cabeçalho roxo (`#4F46E5`) com texto branco;
  - fonte `Helvetica/Helvetica-Bold`;
  - grid cinza;
  - listras alternadas nas linhas (`ROWBACKGROUNDS`).

## 8. Geração de XLSX (layout padrão)

Arquivo: `apps/relatorios/services/xlsx.py`, função `gerar_xlsx_tabela(...)`.

Características:

- 1 planilha por arquivo;
- cabeçalho com fundo `4F46E5`, fonte branca e negrito;
- borda fina em todas as células;
- largura de coluna fixa em `15`.

## 9. PDF oficial de encaminhamento (layout dedicado)

Arquivo: `apps/relatorios/services/encaminhamento_pdf.py`, função `gerar_pdf_encaminhamento(encaminhamento)`.

Esse PDF não usa o layout tabular genérico. Ele monta manualmente:

- blocos de título e linhas separadoras;
- grid de dados pessoais do aluno;
- quadro de curso/ano;
- quadro de horas (1º ao 4º ano, total e média);
- blocos textuais de declaração e encaminhamento;
- bloco de assinatura e protocolo.

Helpers do mesmo arquivo:

- `_format_cep`
- `_format_data`
- `_format_horas_minutos`
- `_horas_por_ano` (calcula horas por ano do curso usando `Horas` e `data_ingresso`).

## 10. Como alterar layout de PDF

### 10.1 Alterar todos os relatórios tabulares

Edite `apps/relatorios/services/pdf.py` em `gerar_pdf_tabela`.

Pontos de customização mais comuns:

- tamanho/orientação: `pagesize`;
- margens: `SimpleDocTemplate(...Margin=...)`;
- tipografia: `fontSize`, `fontName`, `ParagraphStyle`;
- cores: `BACKGROUND`, `TEXTCOLOR`;
- espaçamento: `TOPPADDING`, `BOTTOMPADDING`, `Spacer`;
- bordas/grades: `GRID`;
- zebra striping: `ROWBACKGROUNDS`.

Impacto: qualquer view que chama `gerar_pdf_tabela` herdará a mudança.

### 10.2 Alterar somente o PDF de encaminhamento

Edite `apps/relatorios/services/encaminhamento_pdf.py`.

Pontos típicos:

- ordem dos blocos no array `elements`;
- textos fixos (declaração, protocolo, etc.);
- largura das colunas (`colWidths`) em cada `Table`;
- estilos (`ParagraphStyle`, `TableStyle`);
- conteúdo calculado (horas por ano e formatações).

Impacto: apenas `GET /relatorios/encaminhamento/<pk>/pdf/`.

### 10.3 Criar um novo layout sem quebrar os existentes

Estratégia recomendada:

1. criar uma nova função no `services/pdf.py` (ex.: `gerar_pdf_tabela_moderno`);
2. manter `gerar_pdf_tabela` intacto;
3. ajustar apenas a view do relatório que deve usar o novo layout.

Assim você evita regressão visual nos demais relatórios.

### 10.4 Checklist de alteração visual

Após editar layout:

1. validar PDFs em dados reais curtos e longos;
2. testar quebra de página e repetição de cabeçalho;
3. testar `portrait` e `landscape` onde aplicável;
4. conferir acentuação, datas e duração de horas;
5. confirmar nome do arquivo no download (`Content-Disposition`).

## 11. Como adicionar um novo relatório

Passo a passo:

1. criar função de dados em `apps/relatorios/reports/novo_relatorio.py`;
2. exportar no `apps/relatorios/reports/__init__.py`;
3. criar view em `apps/relatorios/views.py`;
4. registrar rota em `apps/relatorios/urls.py`;
5. opcional: criar versão XLSX além de PDF;
6. ligar botão/link no template de origem com os filtros necessários.

## 12. Referências rápidas de código

- `apps/relatorios/views.py`: fluxo das views, filtros e permissões.
- `apps/relatorios/urls.py`: endpoints.
- `apps/relatorios/reports/alunos.py`: dados de alunos.
- `apps/relatorios/reports/encaminhamentos.py`: dados de encaminhamentos.
- `apps/relatorios/reports/horas.py`: dados de horas e horas por aluno.
- `apps/relatorios/reports/consolidado.py`: agregados gerais.
- `apps/relatorios/services/pdf.py`: layout PDF padrão.
- `apps/relatorios/services/encaminhamento_pdf.py`: layout PDF oficial.
- `apps/relatorios/services/xlsx.py`: layout XLSX.
