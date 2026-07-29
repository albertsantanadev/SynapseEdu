from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# ── Engine ──────────────────────────────────────────────
# Ponto único de conhecimento sobre "onde está o banco".
# Gerencia um pool de conexões reutilizáveis (não abre uma
# conexão TCP nova a cada query).
engine = create_engine(settings.database_url)

# ── Session factory ─────────────────────────────────────
# SessionLocal não é uma Session em si — é uma "fábrica" que,
# quando chamada (SessionLocal()), cria uma nova Session.
# autocommit=False e autoflush=False: nós quem decidimos
# explicitamente quando dar commit, nunca o SQLAlchemy sozinho.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ── Base declarativa ─────────────────────────────────────
# Toda classe de app/db/models.py vai herdar dessa Base.
# É o que permite ao SQLAlchemy saber "essas classes Python
# representam tabelas".
Base = declarative_base()


# ── Dependency para o FastAPI ────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
