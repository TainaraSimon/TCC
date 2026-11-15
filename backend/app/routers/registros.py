from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Analise, Registro, Usuario
from app.schemas import RegistroCriar, RegistroEditar, RegistroResposta, TranscricaoResposta
from app.seguranca import usuario_logado
from app.servico_ia import ErroIA, LimiteIA, analisar_texto, transcrever_audio

router = APIRouter(prefix="/registros", tags=["Registros"])

EXTENSOES_AUDIO = {".webm", ".ogg", ".mp4", ".m4a", ".mp3", ".wav", ".flac"}
TAMANHO_MAXIMO_AUDIO = 25 * 1024 * 1024  # 25 MB, limite do Groq


def buscar_registro(id_registro: int, usuario: Usuario, db: Session) -> Registro:
    registro = db.get(Registro, id_registro)
    # RNF03: o usuário só acessa os próprios registros
    if registro is None or registro.id_usuario != usuario.id_usuario:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Registro não encontrado.")
    return registro


def analisar_registro(registro: Registro, db: Session) -> str | None:
    """RF09: analisa o texto do registro e salva o resultado.

    Se o serviço de IA falhar, o registro é mantido sem análise e a função
    devolve uma mensagem de aviso para o usuário (seção 7.4 do artigo).
    """
    try:
        resultado = analisar_texto(registro.conteudo_texto)
    except LimiteIA as erro:
        return f"O registro foi salvo, mas a análise não foi concluída. {erro}"
    except ErroIA:
        return "O registro foi salvo, mas a análise não foi concluída. Tente analisar novamente mais tarde."

    # RN07: cada registro tem no máximo uma análise; se já existir, ela é atualizada
    if registro.analise is None:
        registro.analise = Analise()
    registro.analise.sentimento = resultado["sentimento"]
    registro.analise.categorias = resultado["categorias"]
    registro.analise.categoria_predominante = resultado["categoria_predominante"]
    registro.analise.contexto = resultado["contexto"]
    registro.analise.resumo = resultado["resumo"]
    registro.analise.modelo = resultado["modelo"]
    registro.analise.data_analise = datetime.now(timezone.utc)
    db.commit()
    db.refresh(registro)
    return None


def montar_resposta(registro: Registro, aviso: str | None = None) -> RegistroResposta:
    resposta = RegistroResposta.model_validate(registro)
    resposta.aviso = aviso
    return resposta


@router.post("/transcrever", response_model=TranscricaoResposta, dependencies=[Depends(usuario_logado)])
def transcrever(audio: UploadFile):
    """RF04/RF05: transcreve o áudio gravado no navegador.

    O registro ainda não é salvo: o usuário confere o texto transcrito antes
    da análise (seção 7.4 do artigo). O áudio não é armazenado.
    """
    extensao = Path(audio.filename or "").suffix.lower()
    if extensao not in EXTENSOES_AUDIO:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Formato de áudio não suportado.")

    conteudo = audio.file.read()
    if not conteudo:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "O áudio está vazio.")
    if len(conteudo) > TAMANHO_MAXIMO_AUDIO:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "O áudio excede o limite de 25 MB.")

    try:
        texto = transcrever_audio(f"audio{extensao}", conteudo)
    except LimiteIA as erro:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, str(erro))
    except ErroIA:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Não foi possível transcrever o áudio. Tente novamente.")

    if not texto:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Não foi possível identificar fala no áudio.")
    return TranscricaoResposta(texto=texto)


@router.post("", response_model=RegistroResposta, status_code=status.HTTP_201_CREATED)
def criar_registro(
    dados: RegistroCriar,
    usuario: Usuario = Depends(usuario_logado),
    db: Session = Depends(get_db),
):
    """RF03/RF04: salva um registro por texto ou por voz (já transcrito e conferido) e o analisa."""
    registro = Registro(tipo=dados.tipo, conteudo_texto=dados.conteudo_texto, id_usuario=usuario.id_usuario)
    db.add(registro)
    db.commit()
    db.refresh(registro)

    aviso = analisar_registro(registro, db)  # RN06: a análise usa somente o texto
    return montar_resposta(registro, aviso)


@router.get("", response_model=list[RegistroResposta])
def listar_registros(usuario: Usuario = Depends(usuario_logado), db: Session = Depends(get_db)):
    """RF08: histórico de registros do usuário, do mais recente para o mais antigo."""
    consulta = (
        select(Registro)
        .where(Registro.id_usuario == usuario.id_usuario)
        .options(selectinload(Registro.analise))
        .order_by(Registro.data_hora.desc())
    )
    return db.scalars(consulta).all()


@router.get("/{id_registro}", response_model=RegistroResposta)
def consultar_registro(id_registro: int, usuario: Usuario = Depends(usuario_logado), db: Session = Depends(get_db)):
    return buscar_registro(id_registro, usuario, db)


@router.put("/{id_registro}", response_model=RegistroResposta)
def editar_registro(
    id_registro: int,
    dados: RegistroEditar,
    usuario: Usuario = Depends(usuario_logado),
    db: Session = Depends(get_db),
):
    """RF06: edita o texto do registro; a análise é refeita sobre o novo texto."""
    registro = buscar_registro(id_registro, usuario, db)
    registro.conteudo_texto = dados.conteudo_texto
    registro.analise = None  # a análise antiga não vale mais para o novo texto
    db.commit()
    db.refresh(registro)

    aviso = analisar_registro(registro, db)
    return montar_resposta(registro, aviso)


@router.post("/{id_registro}/analisar", response_model=RegistroResposta)
def reanalisar_registro(id_registro: int, usuario: Usuario = Depends(usuario_logado), db: Session = Depends(get_db)):
    """Tenta novamente a análise de um registro cuja análise falhou."""
    registro = buscar_registro(id_registro, usuario, db)
    aviso = analisar_registro(registro, db)
    if aviso:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, aviso)
    return montar_resposta(registro)


@router.delete("/{id_registro}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_registro(id_registro: int, usuario: Usuario = Depends(usuario_logado), db: Session = Depends(get_db)):
    """RF07: exclui o registro; a análise vinculada é excluída junto (RN08)."""
    registro = buscar_registro(id_registro, usuario, db)
    db.delete(registro)
    db.commit()