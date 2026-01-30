# Convênios e Estágios

Aplicação web em **Python/Django** para gestão acadêmica e de usuários, com foco em convênios e estágios. Utiliza templates server-side, assets estáticos e **Tailwind CSS** para o front-end.

---

## Visão geral

O projeto organiza o domínio em apps Django:

- **`apps/academico/`** — Alunos, cursos e faculdades (CRUD, listagens, detalhes).
- **`apps/usuarios/`** — Autenticação por **CPF**, usuários e papéis (roles).
- **`apps/contrapartida/`** — Módulo de contrapartida.
- **`core/`** — Configuração central (settings, URLs, templatetags, utils).

Cada perfil de usuário tem um dashboard próprio após o login. O banco padrão em desenvolvimento é **SQLite** (`db.sqlite3`).

---

## Funcionalidades principais

### Papéis (roles)

| Papel | Descrição |
|-------|-----------|
| **Diretor** | Acesso ao dashboard do diretor. |
| **Aluno** | Perfil vinculado a um registro de Aluno (curso, matrícula, dados pessoais); dashboard do aluno. |
| **Secretaria** | Acesso ao dashboard da secretaria. |
| **Administrativo** | Acesso ao dashboard administrativo. |

Autenticação é feita por **CPF** (campo `USERNAME_FIELD` do modelo de usuário).

### Módulo acadêmico

- **Faculdades** — Cadastro e listagem.
- **Cursos** — Vinculados a faculdades, com duração em semestres.
- **Alunos** — Vinculados a um usuário (1:1) e opcionalmente a um curso; matrícula, data de ingresso, situação (Ativo/Inativo), endereço, etc. Cálculo de semestre atual a partir da data de ingresso.

### Outros

- Login/logout e redirecionamento por perfil.
- Django Admin em `/admin/`.
- Layout base compartilhado (navbar, footer), páginas de listagem com paginação.

---

## Pré-requisitos

- **Python 3** (recomendado: ambiente virtual)
- **Node.js** e **npm** (para build do Tailwind CSS)
- **Django 6.0.1** (e dependências em `requirements.txt`)

---

## Comandos rápidos

### Ambiente Python

```bash
# Criar e ativar ambiente virtual (exemplo)
python -m venv venv
source venv/bin/activate   # Linux/macOS
# ou: venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superusuário (login por CPF no admin)
python manage.py createsuperuser

# Subir o servidor de desenvolvimento
python manage.py runserver
```

O servidor fica em **http://127.0.0.1:8000/** por padrão.

### Migrações

```bash
# Criar migrações após alterar models
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate
```

### Front-end (Tailwind CSS)

```bash
# Instalar dependências
npm install

# Build do CSS (uma vez)
npm run build:css

# Watch do CSS durante o desenvolvimento
npm run watch:css
```

### Outros

```bash
# Shell Django
python manage.py shell

# Coletar arquivos estáticos (para deploy)
python manage.py collectstatic
```

---

## Estrutura resumida

```
.
├── apps/
│   ├── academico/     # Alunos, cursos, faculdades
│   ├── contrapartida/ # Contrapartida
│   └── usuarios/      # Autenticação e usuários (roles)
├── core/              # Settings, URLs, templatetags
├── static/            # CSS, JS, imagens (Tailwind)
├── templates/         # Base, dashboard, includes, login
├── manage.py
├── requirements.txt
├── package.json       # Scripts Tailwind
└── tailwind.config.js
```

---

## Documentação adicional

- **`docs/estrutura.md`** — Estrutura detalhada, models e relações.
- **`docs/development.md`** — Guia do desenvolvedor, convenções de branches e contribuição.

---

## Licença

Conforme definido no repositório do projeto.
