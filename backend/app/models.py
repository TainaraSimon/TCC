from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)  # RN02
    senha: Mapped[str] = mapped_column(String(255))  # hash com salt (RNF02)

    registros: Mapped[list["Registro"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")


class Registro(Base):
    __tablename__ = "registro"
    __table_args__ = (CheckConstraint("tipo IN ('texto', 'voz')", name="ck_registro_tipo"),)  # RN04

    id_registro: Mapped[int] = mapped_column(primary_key=True)
    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    tipo: Mapped[str] = mapped_column(String(10))
    conteudo_texto: Mapped[str] = mapped_column(Text)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario", ondelete="CASCADE"))  # RN03

    usuario: Mapped[Usuario] = relationship(back_populates="registros")
    # RN07: no máximo uma análise por registro / RN08: excluída junto com o registro
    analise: Mapped[Optional["Analise"]] = relationship(back_populates="registro", cascade="all, delete-orphan")


class Analise(Base):
    __tablename__ = "analise"

    id_analise: Mapped[int] = mapped_column(primary_key=True)
    data_analise: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    sentimento: Mapped[str] = mapped_column(String(10))
    categoria_predominante: Mapped[Optional[str]] = mapped_column(String(20))
    contexto: Mapped[Optional[str]] = mapped_column(String(20))  # área da vida ligada ao relato
    categorias: Mapped[list[str]] = mapped_column(ARRAY(String(20)))
    resumo: Mapped[str] = mapped_column(Text)
    modelo: Mapped[str] = mapped_column(String(100))
    id_registro: Mapped[int] = mapped_column(
        ForeignKey("registro.id_registro", ondelete="CASCADE"), unique=True  # RN07
    )

    registro: Mapped[Registro] = relationship(back_populates="analise")