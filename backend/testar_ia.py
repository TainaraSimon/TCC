"""Testa a integração com o Groq pelo terminal.

Uso (dentro de C:\\TCC\\backend, com o ambiente virtual ativo):
    python testar_ia.py modelos
    python testar_ia.py analisar "Hoje tive um dia cansativo no trabalho..."
    python testar_ia.py transcrever "caminho\\do\\audio.m4a"
"""
import json
import sys
from pathlib import Path

from app.servico_ia import ErroIA, analisar_texto, cliente, transcrever_audio


def mostrar(dados):
    print(json.dumps(dados, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    comando = sys.argv[1]
    try:
        if comando == "modelos":
            for modelo in cliente.models.list().data:
                print(modelo.id)

        elif comando == "analisar" and len(sys.argv) > 2:
            mostrar(analisar_texto(" ".join(sys.argv[2:])))

        elif comando == "transcrever" and len(sys.argv) > 2:
            arquivo = Path(sys.argv[2])
            if not arquivo.is_file():
                print("Arquivo não encontrado:", arquivo)
                return
            texto = transcrever_audio(arquivo.name, arquivo.read_bytes())
            print("Transcrição:", texto)
            print("\nAnálise:")
            mostrar(analisar_texto(texto))

        else:
            print(__doc__)
    except ErroIA as erro:
        print("Erro na IA:", erro)


if __name__ == "__main__":
    main()