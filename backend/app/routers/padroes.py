from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Registro, Usuario
from app.schemas import PadroesResposta
from app.seguranca import usuario_logado
from app.servico_padroes import calcular_padroes

router = APIRouter(prefix="/padroes", tags=["Padrões emocionais"])


@router.get("", response_model=PadroesResposta)
def consultar_padroes(
    periodo: Literal["semana", "mes"] = "semana",
    quantidade: int = Query(default=6, ge=1, le=24, description="Quantos períodos mais recentes considerar"),
    usuario: Usuario = Depends(usuario_logado),
    db: Session = Depends(get_db),
):
    """RF10/RF11: frequência de cada categoria emocional por período e sua variação."""
    # RN09: os padrões usam apenas os registros do próprio usuário
    consulta = (
        select(Registro)
        .where(Registro.id_usuario == usuario.id_usuario)
        .options(selectinload(Registro.analise))
    )
    registros = db.scalars(consulta).all()
    return calcular_padroes(registros, periodo, quantidade)