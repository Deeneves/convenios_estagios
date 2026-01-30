# Guia do Desenvolvedor

Este documento descreve a estrutura do projeto, convenções de branches Git e como contribuir para o Convênios e Estágios.

---

## 1. Estrutura de pastas

### Visão geral

```
.
├── apps/                    # Aplicações Django (domínios)
│   ├── academico/           # Domínio acadêmico (aluno, curso, faculdade)
│   └── usuarios/            # Autenticação e usuários
├── core/                    # Configuração central do projeto
├── docs/                    # Documentação
├── static/                  # Assets estáticos (CSS, JS, imagens)
├── templates/               # Templates globais e compartilhados
├── manage.py
├── requirements.txt
├── tailwind.config.js
└── package.json
```

### `apps/` — Aplicações Django

Cada app em `apps/` representa um domínio ou módulo funcional:

- **`apps/academico/`** — Alunos, cursos, faculdades: models, views, forms, URLs e templates próprios em `apps/academico/templates/academico/`.
- **`apps/usuarios/`** — Autenticação, usuários e papéis (DIRETOR, ADMINISTRATIVO, ALUNO, SECRETARIA): models, views, forms e URLs.

Estrutura típica de um app:

```
apps/<nome_app>/
├── __init__.py
├── admin.py          # Registro no Django Admin
├── apps.py           # Configuração do app
├── forms.py          # Formulários
├── migrations/       # Migrações do banco
├── models.py
├── tests.py
├── urls.py           # Rotas do app
├── views.py
└── templates/       # Opcional: templates específicos do app
    └── <nome_app>/
        └── *.html
```

Novos domínios devem ser criados como novos apps em `apps/` e registrados em `core/settings.py` (`INSTALLED_APPS`) e em `core/urls.py`.

### `templates/` — Templates globais

- **`templates/base.html`** — Layout base (HTML, navbar, footer).
- **`templates/includes/`** — Partes reutilizáveis: `navbar.html`, `footer.html`, `pagination.html`.
- **`templates/dashboard/`** — Páginas iniciais por perfil: `aluno_home.html`, `diretor_home.html`, `secretaria_home.html`, `administrativo_home.html`.
- **`templates/registration/`** — Login e demais views de autenticação do Django.

Templates específicos de um app ficam em `apps/<app>/templates/<app>/` para evitar colisão de nomes.

### `core/` — Núcleo do projeto

- **`core/settings.py`** — Configurações (DB, apps, estáticos, etc.).
- **`core/urls.py`** — Roteamento principal (inclui as URLs dos apps).
- **`core/templatetags/`** — Template tags customizadas (ex.: formatters).
- **`core/utils/`** — Utilitários compartilhados.

### `static/`

- **`static/css/`** — `tailwind.input.css` (fonte) e `main.css` (saída/build).
- **`static/js/`** — `main.js` e scripts gerais.
- **`static/img/`** — Imagens e favicon.

Build do Tailwind: `npm run build` (ver `package.json`).

---

## 2. Convenções de branches Git

O fluxo é baseado em branches de curta duração a partir de `main`, com nomes padronizados.

### Tipos de branch

| Prefixo   | Uso |
|----------|-----|
| `feature/` | Nova funcionalidade ou melhoria. Ex.: `feature/cadastro-convenio`. |
| `bugfix/`  | Correção de bug. Ex.: `bugfix/login-cpf-vazio`. |
| `hotfix/`  | Correção urgente em produção (quando houver deploy). Ex.: `hotfix/erro-500-login`. |
| `docs/`    | Apenas documentação. Ex.: `docs/development-guide`. |
| `refactor/`| Refatoração sem mudança de comportamento. Ex.: `refactor/views-aluno`. |

### Regras

1. **Base:** sempre criar a branch a partir de `main` atualizado:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/nome-descritivo
   ```

2. **Nome da branch:** minúsculas, palavras separadas por hífen, prefixo + descrição curta:
   - `feature/lista-convenios`
   - `bugfix/validacao-cpf`
   - `docs/atualiza-readme`

3. **Commits:** mensagens claras em português; preferir imperativo (“Adiciona validação de CPF” em vez de “Adicionando…”).

4. **Integração:** as alterações entram em `main` via Pull Request (ou Merge Request), após revisão quando aplicável.

---

## 3. Contribuições

### Antes de começar

1. Garanta que o projeto rode localmente:
   - Python 3, venv ativado, `pip install -r requirements.txt`
   - `npm install` e `npm run build` para o Tailwind
   - Migrações aplicadas: `python manage.py migrate`
2. Consulte `docs/estrutura.md` para modelos e relações e `.cursor/rules/STYLE.mdc` para estilo de código e UI.

### Fluxo de contribuição

1. **Crie uma branch** a partir de `main` usando o prefixo adequado (`feature/`, `bugfix/`, etc.).
2. **Desenvolva e teste** localmente (incluindo testes em `apps/*/tests.py` se existirem).
3. **Commit** com mensagens objetivas.
4. **Abra um Pull Request** para `main`:
   - Título claro (ex.: “Feature: cadastro de convênios”).
   - Descrição do que foi feito e, se for bug, como reproduzir.
   - Referência a issue relacionada, se houver.
5. **Revisão:** mantenha o PR atualizado com `main` e atenda a eventual feedback.
6. **Merge:** após aprovação, o merge em `main` segue a política do repositório (squash ou merge commit, conforme definido pelo time).

### Boas práticas

- **Código:** siga o estilo do projeto (Django, Tailwind, português em UI e comentários). Use class-based views quando fizer sentido.
- **Templates:** reaproveite `templates/base.html` e `templates/includes/`; mantenha a paleta e componentes descritos em STYLE.mdc.
- **Testes:** ao adicionar ou alterar comportamento, inclua ou atualize testes em `tests.py` do app correspondente.
- **Migrations:** não edite migrações já aplicadas; gere novas com `python manage.py makemigrations`.
- **Documentação:** atualize `docs/` (por exemplo `docs/estrutura.md` ou este guia) se a estrutura ou o fluxo mudar.

### Resumo rápido

| Ação | Comando / convenção |
|------|----------------------|
| Nova funcionalidade | Branch `feature/nome-descritivo` |
| Correção de bug | Branch `bugfix/nome-descritivo` |
| Só documentação | Branch `docs/nome-descritivo` |
| Integrar em main | Pull Request → revisão → merge |

Para mais detalhes da estrutura e tecnologias, veja `docs/estrutura.md`.
