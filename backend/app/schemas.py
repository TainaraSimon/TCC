from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# ---------- Usuário ----------

class UsuarioCadastro(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=100)


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class UsuarioResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: int
    nome: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Registros ----------

class RegistroEditar(BaseModel):
    conteudo_texto: str = Field(max_length=10000)

    @field_validator("conteudo_texto")
    @classmethod
    def nao_vazio(cls, valor: str) -> str:  # RN05
        valor = valor.strip()
        if not valor:
            raise ValueError("O registro não pode ser salvo com o conteúdo vazio.")
        return valor


class RegistroCriar(RegistroEditar):
    tipo: Literal["texto", "voz"]  # RN04


class TranscricaoResposta(BaseModel):
    texto: str


class AnaliseResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data_analise: datetime
    sentimento: str
    categorias: list[str]
    categoria_predominante: str | None
    contexto: str | None  # nulo nas análises feitas antes da Etapa 9
    resumo: str


class RegistroResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_registro: int
    data_hora: datetime
    tipo: str
    conteudo_texto: str
    analise: AnaliseResposta | None
    aviso: str | None = None  # preenchido quando a análise não pôde ser concluída


# ---------- Padrões ----------

class PeriodoPadrao(BaseModel):
    inicio: date
    total_registros: int
    frequencia: dict[str, int]
    predominante: str | None


class VariacaoCategoria(BaseModel):
    categoria: str
    anterior: int
    atual: int
    diferenca: int


class PadraoContexto(BaseModel):
    categoria: str
    contexto: str
    total: int


class PadroesResposta(BaseModel):
    periodo: str
    total_analisados: int
    frequencia_geral: dict[str, int]
    mais_frequente: str | None
    periodos: list[PeriodoPadrao]
    variacao: list[VariacaoCategoria]
    contextos: list[PadraoContexto]