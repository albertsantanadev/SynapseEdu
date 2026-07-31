# SynapseEdu — Hub Inteligente de Recursos Educacionais

Aplicação fullstack para cadastro e catalogação de materiais didáticos, com um assistente de IA ("Smart Assist") que sugere descrição e tags automaticamente a partir do título do material.

🔗 **Aplicação em produção:** https://synapse-edu-one.vercel.app
🔗 **API (backend):** https://synapseedu.onrender.com/docs

> Nota: o backend está hospedado no free tier do Render — a primeira requisição após um período de inatividade pode levar alguns segundos a mais enquanto o serviço "acorda".

---

## Sobre o projeto

Desenvolvido como resposta ao Desafio Técnico Fullstack de gerenciamento de materiais didáticos. O sistema permite que conteudistas cadastrem, editem e removam recursos educacionais (vídeos, PDFs e links), e usa um LLM para gerar descrições e tags sugeridas, reduzindo o trabalho manual de catalogação.

## Funcionalidades

- CRUD completo de recursos, com listagem paginada
- **Smart Assist**: geração automática de descrição e até 3 tags via IA, a partir do título e tipo do material
- Tratamento de erro amigável caso a IA falhe, sem bloquear o cadastro manual
- Health check com verificação real de conexão ao banco (`/health`)
- Logs estruturados das interações com a IA (título, uso de tokens, latência)

## Stack tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy, Pydantic / pydantic-settings, Alembic |
| Banco de dados | PostgreSQL (Neon, gerenciado) |
| IA | Groq API (`llama-3.3-70b-versatile`) — Gemini suportado como alternativa opcional |
| Frontend | React 18, Vite, Tailwind CSS v4, axios |
| Testes | pytest + pytest-mock (testes unitários mockados do serviço de IA) |
| CI | GitHub Actions (flake8, black, pytest) |
| Containerização | Docker + Docker Compose |
| Deploy | Render (backend, via Docker) + Vercel (frontend) |

## Arquitetura

A documentação arquitetural completa está na pasta [`Documentação/`](./Documentação), incluindo:

- **ADRs** — decisões de arquitetura registradas com contexto, decisão e consequências (framework escolhido, UUID vs Integer, provedor de IA, ambiente do banco, etc.)
- **Modelo C4** — diagramas de Contexto, Container, Componente e Vista de Implantação
- **Modelo de Dados** — estrutura da tabela `resources`
- **Contrato da API** — todos os endpoints REST
- **Engenharia de Prompt** — especificação do system prompt usado no Smart Assist

Resumo da arquitetura de implantação:

```
[Navegador] --HTTPS--> [Vercel: Frontend React]
                              |
                    HTTPS/REST (CORS liberado)
                              |
                              v
                    [Render: Backend FastAPI (Docker)]
                         |              |
                    SQL/SSL         HTTPS
                         |              |
                         v              v
                  [Neon: PostgreSQL] [Groq API]
```

## Como rodar localmente (sem Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # preencha DATABASE_URL e GROQ_API_KEY
alembic upgrade head
uvicorn app.main:app --reload
```

A API sobe em `http://127.0.0.1:8000` — documentação interativa em `/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env      # confirme VITE_API_BASE_URL
npm run dev
```

A aplicação sobe em `http://localhost:5173`.

## Como rodar com Docker

```bash
# na raiz do projeto
echo "GROQ_API_KEY=sua_chave_aqui" > .env
docker compose up --build
```

Isso sobe três containers: backend (aplica migrations automaticamente ao iniciar), frontend (servido via Nginx) e um PostgreSQL local isolado — nenhuma credencial de produção é necessária para rodar o ambiente completo localmente. Ver [ADR-05](./Documentação/Adr_s.pdf) para o raciocínio por trás dessa escolha.

Acesse `http://localhost:5173`.

## Variáveis de ambiente

Detalhamento completo em [`Documentação/Variaveis_de_Ambiente.pdf`](./Documentação/Variaveis_de_Ambiente.pdf). Resumo:

**`backend/.env`**
```env
DATABASE_URL=postgresql://usuario:senha@host:5432/banco
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=       # opcional
ENVIRONMENT=development
```

**`frontend/.env`**
```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

**`.env`** (raiz, usado pelo `docker-compose.yml`)
```env
GROQ_API_KEY=gsk_...
```

Nenhum desses arquivos é versionado — todos cobertos pelo `.gitignore`. Apenas `.env.example` é versionado, como referência.

## Testes

```bash
cd backend
pytest -v
```

Os testes cobrem o `ai_service.py` com mocks (sem chamadas reais à Groq): caminho feliz, truncamento de tags para 3, resposta em JSON inválido e falha de comunicação com a API.

## CI/CD

Pipeline no GitHub Actions (`.github/workflows/ci.yml`) roda a cada push/PR na branch `main`:
1. `flake8` — lint
2. `black --check` — formatação
3. `pytest` — testes unitários

## Deploy

- **Backend**: Render, Web Service via Docker, aplicando `alembic upgrade head` automaticamente no `entrypoint.sh` antes de subir o servidor. Porta injetada dinamicamente via variável `PORT`.
- **Frontend**: Vercel, build estático via Vite.
- **Banco de dados**: Neon (PostgreSQL gerenciado), compartilhado entre desenvolvimento local (fora do Docker) e produção.
- **CORS**: restrito explicitamente às origens de desenvolvimento e produção — não usa `allow_origins=["*"]`.

## Estrutura de pastas

Árvore completa em [`Documentação/Estrutura_de_pastas_atual.pdf`](./Documentação/Estrutura_de_pastas_atual.pdf).

```
SynapseEdu/
├── backend/    # FastAPI, SQLAlchemy, Alembic, testes
├── frontend/   # React, Vite, Tailwind
├── Documentação/
├── .github/workflows/ci.yml
└── docker-compose.yml
```

## Licença

Projeto desenvolvido para fins de avaliação técnica.