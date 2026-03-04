from app.ingest.loader import load_docs
from app.ingest.splitter import split_docs

def index_documents(vector_store, params):
    docs = load_docs(params)
    splits = split_docs(docs, params)

    vector_store.add_documents(splits)
    