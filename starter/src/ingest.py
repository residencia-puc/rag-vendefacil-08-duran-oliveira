import logging
import sys
import uuid
from pathlib import Path
from typing import Callable

# preparando o "caminho de busca" do Python
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from langchain_community.document_loaders import (
    CSVLoader, JSONLoader, TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import DATA_DIR, INDEX_DIR, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, CONFIDENCIALIDADE_PADRAO
from schema import ChunkMetadata, TipoFonte

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Loaders por formato
def _carregar_csv(caminho: str) -> list[Document]:
    return CSVLoader(caminho, encoding="utf-8").load()

def _carregar_json(caminho: str) -> list[Document]:
    return JSONLoader(caminho, jq_schema=".", text_content=False).load()

def _carregar_jsonl(caminho: str) -> list[Document]:
    return JSONLoader(caminho, jq_schema=".", json_lines=True, text_content=False).load()

def _carregar_markdown(caminho: str) -> list[Document]:
    return UnstructuredMarkdownLoader(caminho).load()

def _carregar_pdf(caminho: str) -> list[Document]:
    return PyPDFLoader(caminho).load()

def _carregar_txt(caminho: str) -> list[Document]:
    return TextLoader(caminho, encoding="utf-8").load()

LOADERS: dict[str, Callable[[str], list[Document]]] = {
    ".csv": _carregar_csv,
    ".json": _carregar_json,
    ".jsonl": _carregar_jsonl,
    ".md": _carregar_markdown,
    ".pdf": _carregar_pdf,
    ".txt": _carregar_txt,
}

def detectar_fonte(caminho: Path) -> TipoFonte:
    return TipoFonte(caminho.suffix.lstrip("."))

# Chunking adaptativo por tipo de fonte
def _chunk_markdown(docs: list[Document]) -> list[Document]:
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "h1"), ("##", "h2")])
    resultado: list[Document] = []
    for doc in docs:
        resultado.extend(splitter.split_text(doc.page_content))
    return resultado

def _chunk_texto_corrido(docs: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_documents(docs)

def chunkar(docs: list[Document], fonte: TipoFonte) -> list[Document]:
    match fonte:
        case TipoFonte.markdown:
            return _chunk_markdown(docs)
        case TipoFonte.csv | TipoFonte.json | TipoFonte.jsonl:
            # cada registro (linha de CSV, objeto JSON) já é uma unidade
            # semântica própria — não faz sentido recortar por tamanho aqui.
            return docs
        case _:
            return _chunk_texto_corrido(docs)

# Enriquecimento de metadados
def _construir_metadata(
    chunk: Document, fonte: TipoFonte, arquivo: str, doc_id: str, posicao: int
) -> ChunkMetadata:
    return ChunkMetadata(
        doc_id=doc_id,
        chunk_id=str(uuid.uuid4()),
        fonte=fonte,
        arquivo_origem=arquivo,
        confidencialidade=CONFIDENCIALIDADE_PADRAO,
        pagina=chunk.metadata.get("page"),
        posicao_no_doc=posicao,
    )

def enriquecer_metadados(
    chunks: list[Document], fonte: TipoFonte, arquivo: str, doc_id: str
) -> list[Document]:
    for i, chunk in enumerate(chunks):
        metadata = _construir_metadata(chunk, fonte, arquivo, doc_id, i)
        chunk.metadata.update(metadata.model_dump(mode="json"))
    return chunks

# Orquestração da ingestão
def _listar_arquivos_suportados(data_dir: Path) -> list[Path]:
    return [p for p in data_dir.rglob("*") if p.suffix in LOADERS]

def _processar_arquivo(caminho: Path) -> list[Document]:
    fonte = detectar_fonte(caminho)
    docs = LOADERS[caminho.suffix](str(caminho))
    chunks = chunkar(docs, fonte)
    doc_id = str(uuid.uuid4())
    return enriquecer_metadados(chunks, fonte, caminho.name, doc_id)

def ingerir_diretorio(data_dir: str = DATA_DIR) -> list[Document]:
    todos_chunks: list[Document] = []
    arquivos = _listar_arquivos_suportados(Path(data_dir))
    logger.info("Encontrados %d arquivos suportados em %s", len(arquivos), data_dir)

    for caminho in arquivos:
        try:
            chunks = _processar_arquivo(caminho)
            todos_chunks.extend(chunks)
            logger.info("Processado %s: %d chunks", caminho.name, len(chunks))
        except Exception:
            logger.exception("Falha ao processar %s — arquivo ignorado", caminho.name)

    logger.info("Ingestão concluída: %d chunks no total", len(todos_chunks))
    return todos_chunks

# Indexação FAISS
def construir_e_salvar_index(chunks: list[Document], index_dir: str = INDEX_DIR) -> FAISS:
    if not chunks:
        raise ValueError("Nenhum chunk para indexar — verifique se data/ contém arquivos suportados.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_dir)
    logger.info("Index salvo em %s", index_dir)
    return vectorstore

if __name__ == "__main__":
    chunks = ingerir_diretorio()
    construir_e_salvar_index(chunks)
