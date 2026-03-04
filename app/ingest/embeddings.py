from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

# Get the embeddings model based on config
def get_embeddings(config):
    emb_cfg = config["embeddings"]
    provider = emb_cfg["provider"]

    if provider == "huggingface":
        return HuggingFaceEmbeddings(model_name=emb_cfg["model_name"])
    elif provider == "openai":
        return OpenAIEmbeddings(model=emb_cfg["model_name"])
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")



