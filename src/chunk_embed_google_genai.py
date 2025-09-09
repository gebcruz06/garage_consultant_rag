import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

file_path = "data/processed/Suzuki_Celerio_Gen2_Service_Manual.md"
persist_directory = "chroma_db_google_genai"

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY.")

print("Building ChromaDB...")

with open(file_path, "r", encoding="utf-8") as f:
    markdown_text = f.read()

chunks = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    separators=["\n\n", "\n", " ", ""]
).split_text(markdown_text)

print(f"Total Chunks Created: {len(chunks)}")

vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    ),
    persist_directory=persist_directory
)

print(f"ChromaDB stored at: {persist_directory}")