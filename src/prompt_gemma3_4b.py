import os
import re
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

images_dir = "data/processed/images"

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY")

print("📂 Loading existing ChromaDB...")

def extract_and_display_images(text, images_dir):
    """Extract image references from text and display available images"""
    image_pattern = r'!\[.*?\]\((.*?)\)'
    image_matches = re.findall(image_pattern, text)
    
    if image_matches:
        print("\n🖼️  Referenced Images:")
        for img_ref in image_matches:
            # Clean the image reference path
            img_ref = img_ref.strip()
            
            # Extract just the filename from the path
            img_filename = os.path.basename(img_ref)
            
            # Create full path to image
            img_path = os.path.join(images_dir, img_filename)
            
            print(f"🔍 Looking for: {img_filename}")
            print(f"📁 Full path: {img_path}")
            
            if os.path.exists(img_path):
                print(f"📷 {img_filename} - Found!")
            else:
                print(f"❌ {img_filename} - Not found")
                # Debug: show what files are actually in the directory
                if os.path.exists(images_dir):
                    files = os.listdir(images_dir)
                    print(f"📂 Available files: {files[:5]}...")  # Show first 5 files

qa_chain = RetrievalQA.from_chain_type(
    llm=GoogleGenerativeAI(
        model="gemma-3-4b-it",
        google_api_key=api_key,
        temperature=0.2
    ),
    retriever=Chroma(
        persist_directory="chroma_db_gemma3_4b",
        embedding_function=GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
    ).as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

print("\n🔎 Interactive QA ready! Type your questions below.")
print("Type 'exit' to quit.\n")

while True:
    query = input("❓ Your question: ")
    if query.lower() in ["exit", "quit", "q"]:
        print("👋 Exiting QA session.")
        break

    result = qa_chain.invoke({"query": query})
    
    print(f"\n💡 Answer:\n{result['result']}")
    
    if "source_documents" in result:
        print("\n📖 Sources:")
        for doc in result["source_documents"]:
            print(f"- {doc.metadata}")
            # Extract and display images from source documents
            extract_and_display_images(doc.page_content, images_dir)
    print("-" * 60)