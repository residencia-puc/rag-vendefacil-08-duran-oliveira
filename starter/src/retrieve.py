import logging
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from openai import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import INDEX_DIR, EMBEDDING_MODEL, OPENROUTER_API_KEY, LLM_MODEL
from schema import FiltroMetadados

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Normalização de texto
def normalizar(texto: str) -> str:
    """Remove acentos, colapsa espaços e baixa a caixa — usado tanto para normalizar o que o LLM extrai quanto os valores reais do vocabulário, para que a comparação entre os dois seja robusta a variações de digitação."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", sem_acento).strip().lower()

# Vocabulário fechado — extraído do índice já construído
def carregar_vectorstore(index_dir: str = INDEX_DIR) -> FAISS:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

def extrair_vocabulario_fechado(vectorstore: FAISS) -> dict[str, list[str]]:
    fontes, departamentos, confidencialidades = set(), set(), set()
    for doc in vectorstore.docstore._dict.values():
        fontes.add(doc.metadata.get("fonte"))
        departamentos.add(doc.metadata.get("departamento"))
        confidencialidades.add(doc.metadata.get("confidencialidade"))

    return {
        "fonte": sorted(f for f in fontes if f),
        "departamento": sorted(d for d in departamentos if d),
        "confidencialidade": sorted(c for c in confidencialidades if c),
    }

# Query Analyzer — extração de filtro via LLM com saída estruturada
_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)


def _montar_prompt(pergunta: str, vocabulario: dict[str, list[str]]) -> str:
    return f"""
    Você extrai filtros de metadados de perguntas sobre uma base de conhecimento corporativa. Responda APENAS com um JSON válido, sem texto adicional.

    Campos possíveis e seus valores válidos (use EXATAMENTE um destes valores, ou omita/null o campo se a pergunta não mencionar isso):

    - fonte: {vocabulario['fonte']}
    - departamento: {vocabulario['departamento']}
    - confidencialidade: {vocabulario['confidencialidade']}

    Regras:
    - NUNCA invente um valor fora das listas acima.
    - Se a pergunta não indicar claramente um filtro, deixe o campo como null.
    - Formato de saída: {{"fonte": null, "departamento": null, "confidencialidade": null}}

    Pergunta: "{pergunta}"
"""

def _chamar_llm(pergunta: str, vocabulario: dict[str, list[str]]) -> str:
    resposta = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": _montar_prompt(pergunta, vocabulario)}],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return resposta.choices[0].message.content

def _validar_contra_vocabulario(
    filtro_bruto: FiltroMetadados, vocabulario: dict[str, list[str]]
) -> FiltroMetadados:
    """Descarta qualquer valor que o LLM tenha devolvido e que não exista de fato no vocabulário — segunda linha de defesa contra alucinação, mesmo com o prompt já restringindo os valores possíveis."""
    dados = filtro_bruto.model_dump()
    for campo, valores_validos in vocabulario.items():
        valor = dados.get(campo)
        if valor is None:
            continue
        valores_normalizados = {normalizar(v): v for v in valores_validos}
        valor_normalizado = normalizar(valor)
        if valor_normalizado in valores_normalizados:
            dados[campo] = valores_normalizados[valor_normalizado]  # forma canônica
        else:
            logger.warning(
                "LLM retornou valor fora do vocabulário para '%s': '%s' — descartando",
                campo, valor,
            )
            dados[campo] = None
    return FiltroMetadados(**dados)

def extrair_filtro(pergunta: str, vocabulario: dict[str, list[str]]) -> FiltroMetadados:
    try:
        conteudo_json = _chamar_llm(pergunta, vocabulario)
        filtro_bruto = FiltroMetadados.model_validate_json(conteudo_json)
    except Exception:
        logger.exception("Falha ao extrair filtro via LLM — prosseguindo sem filtro")
        return FiltroMetadados()

    return _validar_contra_vocabulario(filtro_bruto, vocabulario)

if __name__ == "__main__":
    vectorstore = carregar_vectorstore()
    vocabulario = extrair_vocabulario_fechado(vectorstore)
    logger.info("Vocabulário fechado: %s", vocabulario)

    perguntas_teste = [
        "Quais tickets de atendimento falam sobre reembolso?",
        "Documentos restritos sobre segurança",
        "O que existe sobre RH em arquivos PDF?",
    ]
    for pergunta in perguntas_teste:
        filtro = extrair_filtro(pergunta, vocabulario)
        logger.info("Pergunta: %s → Filtro: %s", pergunta, filtro.model_dump())
