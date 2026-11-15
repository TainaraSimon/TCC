from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.schemas import Token, UsuarioCadastro, UsuarioLogin, UsuarioResposta
from app.seguranca import criar_token, gerar_hash, usuario_logado, verificar_senha

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/cadastro", response_model=UsuarioResposta, status_code=status.HTTP_201_CREATED)
def cadastrar(dados: UsuarioCadastro, db: Session = Depends(get_db)):
    """RF01 - Cadastrar usuário."""
    email = dados.email.lower()

    # RN02: não pode existir mais de um usuário com o mesmo e-mail
    existente = db.scalar(select(Usuario).where(Usuario.email == email))
    if existente:
        raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um usuário cadastrado com este e-mail.")

    usuario = Usuario(nome=dados.nome.strip(), email=email, senha=gerar_hash(dados.senha))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=Token)
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    """RF02 - Realizar login."""
    usuario = db.scalar(select(Usuario).where(Usuario.email == dados.email.lower()))
    if usuario is None or not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "E-mail ou senha incorretos.")
    return Token(access_token=criar_token(usuario.id_usuario))


@router.get("/me", response_model=UsuarioResposta)
def dados_do_usuario(usuario: Usuario = Depends(usuario_logado)):
    """Retorna os dados do usuário logado (usado pela interface)."""
    return usuario