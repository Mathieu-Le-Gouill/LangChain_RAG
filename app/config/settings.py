import os
import yaml
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

# Load config
def load_config(path: str = "app/config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = load_config()

# Setup LLM client
llm_provider = config["rag"]["llm_provider"]
llm_model = config["rag"]["llm_model"]
provider_params = config["rag"]["provider_params"]

if llm_provider == "huggingface":
    api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_token:
        raise ValueError("Missing HUGGINGFACEHUB_API_TOKEN in .env")

    llm_client = InferenceClient(api_key=api_token, **provider_params)
else:
    raise ValueError(f"Unsupported LLM provider: {llm_provider}")
