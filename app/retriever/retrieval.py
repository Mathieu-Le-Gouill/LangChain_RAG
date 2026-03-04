# Get a retriever from the vector store based on config params
def get_retriever(vector_store, params):
    retriever = vector_store.as_retriever(
        search_type=params["rag"]["retriever_search_type"],
        search_kwargs={"k": params["rag"]["retriever_k"]},
    )

    return retriever