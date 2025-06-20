from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os

# Ruta a los archivos fuente
DATA_PATH = "data"
CHROMA_PATH = "db"

print("⏳ Ingestando documentos…")

# Cargar documentos
loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
documents = loader.load()

# Dividir en chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

# Embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Crear y guardar base vectorial
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_PATH,
)

print(f"✅ Ingestados {len(chunks)} chunks en '{os.path.abspath(CHROMA_PATH)}'.")
