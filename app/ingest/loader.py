import logging
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from typing import List
from langchain_core.documents import Document
from pypdf import PdfReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load documents from the specified path and return a list of Document objects
def load_docs(config) -> List[Document]:
    loader_cfg = config["loader"]
    path = Path(loader_cfg["path"])
    glob_pattern = loader_cfg.get("glob", "*.*")
    docs: List[Document] = []

    for file in path.glob(glob_pattern):
        try:
            if file.suffix.lower() == ".pdf":
                try:
                    loader = PyPDFLoader(str(file))
                    file_docs = loader.load()
                    docs.extend(file_docs)
                except Exception as e:
                    logger.warning(f"PyPDFLoader failed for {file}, trying pypdf directly: {e}")
                    try:
                        reader = PdfReader(str(file))
                        text = "\n".join(page.extract_text() or "" for page in reader.pages)
                        if text.strip():
                            docs.append(Document(page_content=text, metadata={"source": str(file)}))
                        else:
                            logger.warning(f"No text extracted from {file}")
                    except Exception as e2:
                        logger.error(f"Failed to load PDF {file}: {e2}")

            elif file.suffix.lower() == ".txt":
                loader = TextLoader(str(file))
                docs.extend(loader.load())

            elif file.suffix.lower() == ".csv":
                loader = CSVLoader(str(file))
                docs.extend(loader.load())

            else:
                logger.info(f"Unsupported file type, skipping: {file}")

        except Exception as e:
            logger.error(f"Failed to load {file}: {e}")

    logger.info(f"Loaded {len(docs)} documents from {path}")
    return docs