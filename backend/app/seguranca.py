from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Usuario

# Argon2: gera automaticamente um salt aleatório para cada senha (RNF02)
hash_senha = PasswordHash.recommended()
esquema_bearer = HTTPBearer()


def gerar_hash(senha: str) -> str:
    return hash_senha.hash(senha)


def verificar_senha(senha: str, hash_salvo: str) -> bool:
    return hash_senha.verify(senha, hash_salvo)


def criar_token(id_usuario: int) -> str:
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiracao_minutos)
    dados = {"sub": str(id_usuario), "exp": expira_em}
    return jwt.encode(dados, settings.jwt_secret, algorithm="HS256")


def usuario_logado(
    credenciais: HTTPAuthorizationCredentials = Depends(esquema_bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    """RN01: identifica o usuário pelo token; sem token válido, a requisição é recusada."""
    erro = HTTPException(status.HTTP_401_UNAUTHORIZED, "Sessão inválida ou expirada. Faça login novamente.")
    try:
        dados = jwt.decode(credenciais.credentials, settings.jwt_secret, algorithms=["HS256"])
        id_usuario = int(dados["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise erro

    usuario = db.get(Usuario, id_usuario)
    if usuario is None:
        raise erro
    return usuario