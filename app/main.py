from fastapi import FastAPI, HTTPException, Body
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from qdrant_client.models import Filter
import uvicorn
import os

from app.config.settings import config, llm_client
from app.vectorstore.store_factory import create_vector_store
from app.indexing.indexing import index_documents
from app.retriever.retrieval import get_retriever
from app.rag.chain import make_rag_chain
from app.schemas.schemas import IndexRequest, QueryRequest

@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:

    if not hasattr(app.state, "vector_store"):
        app.state.client, app.state.vector_store = create_vector_store(config)

    yield

app = FastAPI(lifespan=lifespan)

# To index the documents in the vector store
@app.post("/index")
def index(request: IndexRequest = Body(...)):
    """
    Index documents using parameters from request body.
    If a parameter is not modified, the default from config is used.
    """
    index_documents(app.state.vector_store, request.params)
    return {"message": "Indexing completed successfully"}


# To clear all documents from the collection
@app.post("/clear")
def clear():
    collection_name = config["vectorstore"]["collection_name"]

    app.state.client.delete(
        collection_name=collection_name,
        points_selector=Filter() 
    )
    return {"message": "Collection cleared successfully"}

# RAG query endpoint
@app.post("/query")
def query(request: QueryRequest = Body(...)):
    retriever = get_retriever(app.state.vector_store, request.params)
    rag_chain = make_rag_chain(retriever, llm_client, request.params)

    return rag_chain(request.query)

# Health check endpoint to verify vector store connectivity
@app.get("/health")
def health():
    try:
        client = app.state.vector_store.client
        client.get_collections()  # simple ping
        return {"status": "healthy", "vector_db": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Vector DB unreachable: {str(e)}",
        )

if __name__ == "__main__":
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
    
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)


