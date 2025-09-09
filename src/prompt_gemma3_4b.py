import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

chroma_db = "chroma_db_google_genai"

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY")

print("Loading existing ChromaDB...")

qa_chain = RetrievalQA.from_chain_type(
    llm=GoogleGenerativeAI(
        model="gemma-3-4b-it",
        google_api_key=api_key,
        temperature=0.2
    ),
    retriever=Chroma(
        persist_directory=chroma_db,
        embedding_function=GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
    ).as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

print("\n🔎 Interactive Q&A ready! Type your questions below.")
print("Type 'exit' to quit.\n")

while True:
    query = input("❓ Your question: ")
    if query.lower() in ["exit", "quit", "q"]:
        print("👋 Exiting Q&A session.")
        break

    result = qa_chain.invoke({"query": query})
    
    print(f"\n💡 Answer:\n{result['result']}")
    
    print("-" * 60)