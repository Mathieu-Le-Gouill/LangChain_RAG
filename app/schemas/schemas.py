from app.config.settings import config
from pydantic import BaseModel
from typing import Optional

# Return a nested dictionary suitable for FastAPI request body
def get_default_index_params():

    splitter = config.get("splitter", {})
    loader = config.get("loader", {})

    return {
        "splitter": {
            "chunk_size": splitter.get("chunk_size", 1000),
            "chunk_overlap": splitter.get("chunk_overlap", 200),
            "add_start_index": splitter.get("add_start_index", True),
        },
        "loader": {
            "type": loader.get("type", "pdf"),
            "path": loader.get("path", "./data/archive/Pdf/"),
            "glob": loader.get("glob", "*.pdf"),
        },
    }

# Return a nested dictionary suitable for FastAPI request body
def get_default_query_params():

    rag = config.get("rag", {})

    return {
        "rag": {
            "retriever_search_type": rag.get("retriever_search_type", "similarity"),
            "retriever_k": rag.get("retriever_k", 2),
            "llm_provider": rag.get("llm_provider", "huggingface"),
            "llm_model": rag.get("llm_model", "openai/gpt-oss-120b"),
            "provider_params": rag.get("provider_params", {"provider": "cerebras"}),
            "max_tokens": rag.get("max_tokens", 2048),
        }
    }

class QueryRequest(BaseModel):
    query: str = "What is the capital of France?"
    params: Optional[dict] = get_default_query_params()

class IndexRequest(BaseModel):
    params: Optional[dict] = get_default_index_params()