def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Create a RAG chain function that generates a response based on a query and retrieved documents
def make_rag_chain(retriever, llm_client, config):
    llm_model = config["rag"]["llm_model"]
    max_tokens = config["rag"]["max_tokens"]

    def rag_query(question: str) -> str:

        docs = retriever.invoke(question)
        context = format_docs(docs)

        system_message = (
            "You are a helpful AI assistant. "
            "Answer the question based only on the provided context. "
            "Keep the answer short and precise."
        )

        user_message = f"Context:\n{context or 'No relevant context found.'}\n\nQuestion: {question}"

        # Query the LLM
        response = llm_client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            max_tokens=max_tokens,
        )

        answer = response.choices[0].message.content.strip()
        return answer

    return rag_query