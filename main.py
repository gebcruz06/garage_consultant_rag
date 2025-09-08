import subprocess
import sys

def run_script(script_name):
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting RAG pipeline...\n")

    print(" Step 1: Preprocessing PDFs...")
    run_script("preprocess_pdf.py")

    print("\n Step 2: Chunking & Embedding with Gemma 3-4B...")
    run_script("chunk_embed_gemma3_4b.py")

    print("\n Step 3: Launching Interactive QA with Gemma 3-4B...")
    run_script("prompt_gemma3_4b.py")
