from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class TipoFonte(str, Enum):
    csv = "csv"
    json = "json"
    jsonl = "jsonl"
    markdown = "md"
    pdf = "pdf"
    txt = "txt"

class ChunkMetadata(BaseModel):
    doc_id: str
    chunk_id: str
    fonte: TipoFonte
    arquivo_origem: str
    departamento: Optional[str] = None
    data_documento: Optional[date] = None
    confidencialidade: Optional[str] = "interno"
    pagina: Optional[int] = None
    posicao_no_doc: int
    