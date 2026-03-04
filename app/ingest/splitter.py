from langchain_text_splitters import RecursiveCharacterTextSplitter

# Split documents into smaller chunks based on config params
def split_docs(docs, config):
    splitter_cfg = config["splitter"]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=splitter_cfg["chunk_size"],
        chunk_overlap=splitter_cfg["chunk_overlap"],
        add_start_index=splitter_cfg["add_start_index"],
    )
    return splitter.split_documents(docs)
