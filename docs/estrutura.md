# Estrutura do Projeto

## Visao geral
Projeto web em Python/Django para gestao academica/usuarios, com templates server-side e assets estaticos.

## Tecnologias
- Python 3 (projeto Django)
- Django 6.0.1
- SQLite (db.sqlite3)
- HTML (templates)
- CSS/JS/imagens (static)
- Docker (Dockerfile)

## Estrutura de pastas
```
.
├── apps
│   ├── academico
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   └── academico
│   │   │       ├── aluno_cadastro_usuario.html
│   │   │       ├── aluno_detail.html
│   │   │       ├── aluno_form.html
│   │   │       ├── aluno_list.html
│   │   │       ├── curso_detail.html
│   │   │       ├── curso_form.html
│   │   │       ├── curso_list.html
│   │   │       ├── faculdade_detail.html
│   │   │       ├── faculdade_form.html
│   │   │       └── faculdade_list.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── usuarios
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── migrations
│       │   ├── 0001_initial.py
│       │   ├── 0002_alter_user_managers.py
│       │   └── __init__.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── core
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docs
│   └── estrutura.md
├── static
│   ├── css
│   ├── img
│   └── js
├── templates
│   ├── base.html
│   ├── dashboard
│   │   ├── administrativo_home.html
│   │   ├── aluno_home.html
│   │   ├── diretor_home.html
│   │   └── secretaria_home.html
│   ├── includes
│   │   ├── footer.html
│   │   ├── navbar.html
│   │   └── pagination.html
│   └── registration
│       └── login.html
├── db.sqlite3
├── manage.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env
├── .gitignore
└── .vscode
    └── settings.json
```

## Organizacao por apps
- apps/academico: dominio academico (aluno, curso, faculdade), com models, views, urls, forms e templates proprios.
- apps/usuarios: autenticacao/usuarios, com models, views, urls e forms.

## Templates e estaticos
- templates/: layout base, dashboard e includes compartilhados; templates de login em templates/registration.
- apps/*/templates: templates especificos de cada app (padrao Django).
- static/: arquivos estaticos (css, js, imagens).

## Observacoes
- O projeto usa SQLite local (db.sqlite3) para desenvolvimento.
- Configuracoes principais ficam em core/settings.py.
- Ha um ambiente virtual em venv/ e metadados de git em .git/ (nao listados na arvore por serem gerados/local).
