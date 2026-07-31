<div align="center">

# 📚 SynapseEdu

### Hub Inteligente de Recursos Educacionais

Sistema completo para cadastro, organização e catalogação de materiais didáticos, com um assistente de IA que sugere descrição e tags automaticamente a partir do título do material.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-black?logo=fastapi)
![React](https://img.shields.io/badge/React-v18-61DAFB?logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Licença](https://img.shields.io/badge/Licença-Educacional-informational)

**[🌐 Aplicação em produção](https://synapse-edu-one.vercel.app)** · **[📄 Documentação da API (Swagger)](https://synapseedu.onrender.com/docs)**

</div>

---

> [!NOTE]
> O backend está hospedado no free tier do Render. Após um período de inatividade, a primeira requisição pode levar alguns segundos a mais enquanto o serviço reinicia.

## 📋 Descrição do Projeto

O **SynapseEdu** foi desenvolvido em resposta a um desafio técnico fullstack de gerenciamento de materiais didáticos. O sistema centraliza o acervo de recursos educacionais de uma equipe de conteudistas — vídeos, PDFs e links — e usa um LLM para **acelerar a catalogação**: a partir de um título e tipo de material, a IA sugere uma descrição pedagógica e até 3 tags relevantes, que o conteudista pode aceitar ou editar livremente.

## 🚀 Funcionalidades Principais

- 📇 **CRUD completo de recursos** — cadastro, listagem paginada, edição e exclusão, com campos Título, Descrição, Tipo (Vídeo/PDF/Link), URL e Tags.
- ✨ **Smart Assist (IA)** — botão "Gerar Descrição com IA" que consulta um LLM (Groq) e preenche automaticamente Descrição e até 3 Tags, com base no Título e Tipo informados.
- ⏳ **Feedback visual em tempo real** — estado de carregamento dedicado enquanto a IA processa a resposta, sem travar o restante do formulário.
- 🛟 **Tratamento de erro resiliente** — se a IA falhar ou demorar, o formulário continua editável manualmente, sem bloquear o cadastro.
- 🩺 **Health check com verificação real de banco** — `/health` testa a conexão ao PostgreSQL, não apenas se o processo está de pé.
- 📝 **Logs estruturados** das interações com a IA (título, uso de tokens, latência), no formato `[INFO] AI Request: Title=..., TokenUsage=..., Latency=...`.
- 🎨 **Identidade visual própria** — interface inspirada em fichários de catálogo de biblioteca, com paleta e tipografia autorais (ver `frontend/src/index.css`).

## 🧪 Testes de Software

### Testes Unitários — pytest (`backend/tests/test_ai_service.py`)

Cobrem o serviço de IA (`app/services/ai_service.py`) de forma isolada, com a API da Groq **mockada** — sem chamadas de rede reais, execução rápida e determinística.

| # | Teste | Descrição | Tipo |
|---|---|---|---|
| 01 | `test_generate_description_success` | Fluxo feliz: retorna `description` e `tags` corretamente a partir de uma resposta JSON válida | válido |
| 02 | `test_generate_description_truncates_tags_to_three` | Garante que, mesmo se a IA devolver mais de 3 tags, apenas as 3 primeiras são retornadas | regra de negócio |
| 03 | `test_generate_description_invalid_json_raises_ai_service_error` | Resposta que não é JSON válido levanta `AIServiceError`, nunca uma exceção crua | edge case |
| 04 | `test_generate_description_api_failure_raises_ai_service_error` | Falha de rede/API na chamada à Groq também é convertida em `AIServiceError` | edge case |

```bash
cd backend
pytest -v
```

### Integração Contínua (CI)

Pipeline no GitHub Actions (`.github/workflows/ci.yml`), disparado a cada push/PR na branch `main`:

1. `flake8` — lint estático
2. `black --check` — verificação de formatação
3. `pytest` — execução dos testes unitários

> [!WARNING]
> Testes de integração end-to-end (frontend ↔ backend real) não foram incluídos neste sprint — a suíte atual cobre a camada de serviço de IA, que é a peça mais crítica e mais isolável do sistema. CRUD e Smart Assist foram validados manualmente ponta a ponta em ambiente local, via Docker e em produção.

## 🛠️ Tecnologias e Linguagens

| Camada | Tecnologia | Função |
|---|---|---|
| **Backend** | Python 3.12 + FastAPI | API REST, validação automática, docs interativas (`/docs`) |
| **Backend** | SQLAlchemy + Alembic | ORM e migrations versionadas do banco |
| **Backend** | Pydantic / pydantic-settings | Validação de payloads e configuração via `.env` |
| **Banco de Dados** | PostgreSQL (Neon) | Persistência gerenciada em nuvem, com SSL |
| **IA** | Groq API (`llama-3.3-70b-versatile`) | Geração de descrição e tags via LLM (Gemini suportado como alternativa opcional) |
| **Frontend** | React 18 + Vite | SPA com HMR — pasta `/frontend`, porta `5173` |
| **Frontend** | Tailwind CSS v4 | Estilização via tokens de design (`@theme`) |
| **Testes** | pytest + pytest-mock | Testes unitários com mocks, sem dependência de rede |
| **CI** | GitHub Actions | Lint + formatação + testes a cada push |
| **Infraestrutura** | Docker + Docker Compose | Orquestração local de backend, frontend e banco |

## 📦 Bibliotecas e Frameworks

**Backend:**
- `fastapi` — framework web assíncrono para a API REST
- `sqlalchemy` — ORM para o PostgreSQL
- `alembic` — migrations versionadas do schema do banco
- `pydantic-settings` — leitura tipada de variáveis de ambiente
- `psycopg2-binary` — driver de conexão com o PostgreSQL
- `groq` — SDK oficial para consumo da API de IA
- `python-dotenv` — carregamento do arquivo `.env` em desenvolvimento
- `pytest` / `pytest-mock` — testes unitários com mocks

**Frontend:**
- `axios` — cliente HTTP centralizado (`src/api/client.js`)
- `lucide-react` — ícones vetoriais leves
- `tailwindcss` — utilitários de estilo e tokens de design customizados

## 🏗️ Arquitetura

Documentação arquitetural completa em [`Documentação/`](./Documentação), incluindo ADRs, Modelo de Dados, Modelo C4 (Contexto, Container, Componente e Vista de Implantação), Contrato da API e Engenharia de Prompt.

```
[Navegador] --HTTPS--> [Vercel: Frontend React]
                              │
                    HTTPS/REST (CORS liberado)
                              │
                              ▼
                 [Render: Backend FastAPI (Docker)]
                         │              │
                    SQL/SSL          HTTPS
                         │              │
                         ▼              ▼
                 [Neon: PostgreSQL]  [Groq API]
```

## ⚙️ Pré-requisitos e Instalação

### Requisitos

- [Python](https://www.python.org/) 3.12+
- [Node.js](https://nodejs.org/) v18+
- [Docker](https://www.docker.com/) e Docker Compose (opcional, mas recomendado)
- [Git](https://git-scm.com/)

### Clonar o Repositório

```bash
git clone https://github.com/SEU_USUARIO/SynapseEdu.git
cd SynapseEdu
```

### Instalação via Docker (Recomendado)

```bash
echo "GROQ_API_KEY=sua_chave_aqui" > .env
docker compose up --build
```

O Docker sobe automaticamente três containers — backend (aplicando as migrations via Alembic antes de iniciar), frontend e um PostgreSQL local isolado:

- Frontend em `http://localhost:5173`
- Backend em `http://localhost:8000`

### Instalação Manual

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # preencha DATABASE_URL e GROQ_API_KEY
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env       # confirme VITE_API_BASE_URL
npm run dev
```

## 🔑 Variáveis de Ambiente

Detalhamento completo em [`Documentação/Variaveis_de_Ambiente.pdf`](./Documentação/Variaveis_de_Ambiente.pdf).

Crie `backend/.env` baseado em `backend/.env.example`:

```env
DATABASE_URL=postgresql://usuario:senha@host:5432/banco
GROQ_API_KEY=gsk_sua_chave_aqui
GEMINI_API_KEY=                 # opcional
ENVIRONMENT=development
```

Crie `frontend/.env` baseado em `frontend/.env.example`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

Para uso via Docker Compose, crie um `.env` na **raiz** do projeto:

```env
GROQ_API_KEY=gsk_sua_chave_aqui
```

> [!WARNING]
> Nunca suba nenhum arquivo `.env` para o repositório. Todos já estão listados no `.gitignore` — apenas os arquivos `.env.example` são versionados, como referência.

## 📖 Instruções de Uso

1. Acesse a aplicação (local ou [em produção](https://synapse-edu-one.vercel.app)).
2. Clique em **"Novo recurso"**, preencha Título, Tipo e URL.
3. Clique em **"Gerar Descrição com IA"** para preencher Descrição e Tags automaticamente — ou preencha manualmente.
4. Salve. O recurso aparece na listagem paginada, com edição e exclusão disponíveis em cada ficha.

## 🌐 Deploy

| Serviço | Plataforma | Detalhe |
|---|---|---|
| Frontend | [Vercel](https://vercel.com) | Build estático via Vite |
| Backend | [Render](https://render.com) | Web Service via Docker; migrations aplicadas automaticamente no `entrypoint.sh` |
| Banco de Dados | [Neon](https://neon.tech) | PostgreSQL gerenciado, compartilhado entre dev local (fora do Docker) e produção |

CORS restrito explicitamente às origens de desenvolvimento e produção — a API **não** usa `allow_origins=["*"]`.

## 🌿 Gitflow

```
main
 └── feature/nome-da-feature
 └── fix/nome-do-bug
 └── docs/nome-da-atualizacao
```

Padrão de commits semânticos ([Conventional Commits](https://www.conventionalcommits.org/)):

```
feat: adiciona endpoint de exclusão de recursos
fix: corrige truncamento de tags no smart assist
docs: atualiza contrato da API com endpoints de update e delete
test: adiciona testes unitarios para o ai_service
chore: atualiza dependencias do backend
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit: `git commit -m 'feat: minha nova feature'`
4. Push: `git push origin feature/minha-feature`
5. Abra um Pull Request para `main`

## 📄 Licença

Projeto desenvolvido para fins de avaliação técnica.