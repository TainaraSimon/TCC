"""RF10: identificação de padrões emocionais.

Os padrões são calculados a partir das análises já salvas: o sistema agrupa os
registros por período (semana ou mês), conta a frequência de cada categoria
emocional e compara o período mais recente com o anterior (seção 7.1 do artigo).
Também cruza as emoções com o contexto de cada registro (ex.: ansiedade + social).
"""
from datetime import date, timedelta

from app.servico_ia import CATEGORIAS

# Uma combinação emoção + contexto só é considerada padrão se aparecer em pelo menos 2 registros
MINIMO_PARA_PADRAO = 2


def inicio_do_periodo(dia: date, periodo: str) -> date:
    if periodo == "semana":
        return dia - timedelta(days=dia.weekday())  # segunda-feira da semana
    return dia.replace(day=1)  # primeiro dia do mês


def contagem_vazia() -> dict[str, int]:
    return {categoria: 0 for categoria in CATEGORIAS}


def mais_frequente(frequencia: dict[str, int]) -> str | None:
    categoria, total = max(frequencia.items(), key=lambda item: item[1])
    return categoria if total > 0 else None


def calcular_contextos(registros, inicios: set[date], periodo: str) -> list[dict]:
    """Conta quantas vezes cada emoção apareceu em cada contexto, nos períodos considerados."""
    contagem = {}
    for registro in registros:
        analise = registro.analise
        if analise is None or analise.contexto in (None, "outro"):
            continue
        dia = registro.data_hora.astimezone().date()
        if inicio_do_periodo(dia, periodo) not in inicios:
            continue
        for categoria in analise.categorias:
            chave = (categoria, analise.contexto)
            contagem[chave] = contagem.get(chave, 0) + 1

    padroes = [
        {"categoria": categoria, "contexto": contexto, "total": total}
        for (categoria, contexto), total in contagem.items()
        if total >= MINIMO_PARA_PADRAO
    ]
    padroes.sort(key=lambda item: item["total"], reverse=True)
    return padroes[:5]  # os 5 padrões mais frequentes


def calcular_padroes(registros, periodo: str, quantidade: int) -> dict:
    # 1. Agrupa os registros analisados por período
    grupos = {}
    for registro in registros:
        if registro.analise is None:
            continue
        dia = registro.data_hora.astimezone().date()
        inicio = inicio_do_periodo(dia, periodo)
        if inicio not in grupos:
            grupos[inicio] = {"inicio": inicio, "total_registros": 0, "frequencia": contagem_vazia()}
        grupo = grupos[inicio]
        grupo["total_registros"] += 1
        for categoria in registro.analise.categorias:
            if categoria in grupo["frequencia"]:
                grupo["frequencia"][categoria] += 1

    # 2. Mantém só os períodos mais recentes, em ordem cronológica
    periodos = [grupos[inicio] for inicio in sorted(grupos)][-quantidade:]

    # 3. Frequência total de cada categoria nesses períodos
    frequencia_geral = contagem_vazia()
    for grupo in periodos:
        grupo["predominante"] = mais_frequente(grupo["frequencia"])
        for categoria, total in grupo["frequencia"].items():
            frequencia_geral[categoria] += total

    # 4. Variação: compara o período mais recente com o período imediatamente anterior
    variacao = []
    if periodos:
        ultimo = periodos[-1]
        inicio_anterior = inicio_do_periodo(ultimo["inicio"] - timedelta(days=1), periodo)
        anterior = grupos.get(inicio_anterior, {"frequencia": contagem_vazia()})["frequencia"]
        for categoria in CATEGORIAS:
            variacao.append({
                "categoria": categoria,
                "anterior": anterior[categoria],
                "atual": ultimo["frequencia"][categoria],
                "diferenca": ultimo["frequencia"][categoria] - anterior[categoria],
            })

    # 5. Emoções x contextos nos mesmos períodos
    inicios = {grupo["inicio"] for grupo in periodos}

    return {
        "periodo": periodo,
        "total_analisados": sum(grupo["total_registros"] for grupo in periodos),
        "frequencia_geral": frequencia_geral,
        "mais_frequente": mais_frequente(frequencia_geral),
        "periodos": periodos,
        "variacao": variacao,
        "contextos": calcular_contextos(registros, inicios, periodo),
    }