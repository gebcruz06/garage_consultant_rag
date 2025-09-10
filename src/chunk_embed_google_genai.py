import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Directory containing processed markdown files
input_dir = "data/processed"

# Base directory to store ChromaDBs
base_persist_dir = "data/chroma_db_google_genai"

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY.")

# Initialize embedding model once
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=api_key
)

# Iterate over all markdown files
for filename in os.listdir(input_dir):
    if filename.endswith(".md"):
        file_path = os.path.join(input_dir, filename)

        print(f"\nProcessing: {filename}")

        with open(file_path, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        # Split into chunks
        chunks = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=64,
            separators=["\n\n", "\n", " ", ""]
        ).split_text(markdown_text)

        print(f"Total Chunks Created: {len(chunks)}")

        # Each file gets its own persist directory
        persist_directory = os.path.join(
            base_persist_dir,
            os.path.splitext(filename)[0]  # folder name without .md
        )
        os.makedirs(persist_directory, exist_ok=True)

        # Create and persist vector store
        vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )

        print(f"ChromaDB stored at: {persist_directory}")
