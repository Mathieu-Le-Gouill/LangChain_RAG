import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_community.vectorstores import Chroma    
from app.ingest.embeddings import get_embeddings

def create_vector_store(config):
    """Build provider client and vector store instance based on config settings.
    
    Returns:
        client: the underlying client (e.g. QdrantClient) if applicable, else
                None for vector stores that manage their own client (e.g. Chroma)
        vector_store: the instantiated vector store ready for use
    """
    store_cfg = config["vectorstore"]
    provider = store_cfg["provider"]

    collection_name = store_cfg["collection_name"]
    embedding_dim = config["embeddings"]["dimension"]

    embeddings = get_embeddings(config)

    if provider == "qdrant":

        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not qdrant_url:
            raise ValueError("Missing QDRANT_URL in .env")
        if not qdrant_api_key:
            raise ValueError("Missing QDRANT_API_KEY in .env")
        
        # Initialize Qdrant client and ensure collection exists
        client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

        try:
            client.get_collection(collection_name)
        except Exception:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=embedding_dim,
                    distance=Distance.COSINE,
                ),
            )

        # Initialize Qdrant vector store
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings,
        )

    elif provider == "chroma":
        client = None  # Chroma manages its own client internally
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings.embed_query,
        )
    else:
        raise ValueError(f"Unsupported vector store provider: {provider}")
    
    return client, vector_store
