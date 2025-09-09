import subprocess
import sys
import os

def run_script(script_name: str) -> int:

    try:
        script_path = os.path.join(os.path.dirname(__file__), "src", script_name)
        print(f"\n Running {script_path}...")
        result = subprocess.run([sys.executable, script_path], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e}")
        return e.returncode
    except FileNotFoundError:
        print(f"Script not found: {script_name}")
        return 1

if __name__ == "__main__":
    print("Starting RAG pipeline...")

    # Define the pipeline steps and their checkpoints
    pipeline_steps = [
        ("Step 1: Pre-processing PDFs...", os.path.join("data", "processed", "Suzuki_Celerio_Gen2_Service_Manual.md"), "pre_process_pymupdf4llm.py"),
        ("Step 2: Chunking and Embedding...", "chroma_db_google_genai", "chunk_embed_google_genai.py"),
    ]

    # Run steps with checkpoints
    for step_description, checkpoint_path, script_name in pipeline_steps:
        if not os.path.exists(checkpoint_path):
            print(f"\n {step_description}")
            run_script(script_name)
        else:
            print(f"\n {step_description.split(':')[0]}: already done, skipping...")

    # Step 3: Prompting and Querying (always runs)
    print("\n Step 3: Prompting and Querying...")
    run_script("prompt_gemma3_4b.py")