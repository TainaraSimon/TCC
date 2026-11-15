from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401  (carrega as tabelas antes de criá-las)
from app.config import settings
from app.database import Base, engine
from app.routers import auth, padroes, registros


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    # Cria as tabelas no banco, caso ainda não existam
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="API - Introspect", lifespan=ciclo_de_vida)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(registros.router)
app.include_router(padroes.router)


@app.get("/saude", tags=["Sistema"])
def saude():
    return {"status": "ok"}