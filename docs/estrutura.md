# Estrutura do Projeto

## Visao geral
Projeto web em Python/Django para gestao academica/usuarios, com templates server-side, assets estaticos e build de CSS via Tailwind.

## Tecnologias
- Python 3 (projeto Django)
- Django 6.0.1
- SQLite (db.sqlite3)
- HTML (templates)
- CSS/JS/imagens (static)
- Tailwind CSS 3.4.x (build via CLI)
- Node.js/npm (scripts de build do CSS)
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
│   │   │   ├── 0002_aluno_data_ingresso.py
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
│   ├── templatetags
│   │   ├── __init__.py
│   │   └── formatters.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── formatters.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .cursor
│   └── rules
│       ├── RULES.md
│       ├── RULES.mdc
│       └── STYLE.mdc
├── docs
│   └── estrutura.md
├── scripts
├── static
│   ├── css
│   │   ├── main.css
│   │   ├── tailwind.css
│   │   └── tailwind.input.css
│   ├── img
│   │   └── favicon.png
│   └── js
│       └── main.js
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
├── package.json
├── package-lock.json
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env
├── .gitignore
├── tailwind.config.js
└── .vscode
    └── settings.json
```

## Organizacao por apps
- apps/academico: dominio academico (aluno, curso, faculdade), com models, views, urls, forms e templates proprios.
- apps/usuarios: autenticacao/usuarios, com models, views, urls e forms.

## Models e relacoes
### apps/usuarios
- User (Custom User): estende AbstractUser, autentica por CPF (USERNAME_FIELD = "cpf") e possui papel (role) com valores DIRETOR, ADMINISTRATIVO, ALUNO, SECRETARIA.
- CustomUserManager: gerencia criacao de usuarios e superusuarios com base em CPF.

### apps/academico
- Faculdade: entidade basica com nome; possui relacao 1:N com Curso.
- Curso: pertence a uma Faculdade (ForeignKey) e expõe `faculdade.cursos`.
- Aluno: vinculado a um User (OneToOne) e opcionalmente a um Curso (ForeignKey), expondo `user.aluno` e `curso.alunos`.

### Relacoes entre apps
- apps/academico.Aluno -> apps/usuarios.User (OneToOne): cada aluno corresponde a um usuario do sistema.
- apps/usuarios.User pode ter um Aluno associado via `user.aluno`.

## Templates e estaticos
- templates/: layout base, dashboard e includes compartilhados; templates de login em templates/registration.
- apps/*/templates: templates especificos de cada app (padrao Django).
- static/: arquivos estaticos (css, js, imagens).

## Observacoes
- O projeto usa SQLite local (db.sqlite3) para desenvolvimento.
- Configuracoes principais ficam em core/settings.py.
- Ha um ambiente virtual em venv/, node_modules/ e metadados de git em .git/ (nao listados na arvore por serem gerados/local).
