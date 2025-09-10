import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY environment variable.")

# List available vector databases
base_dir = "data/chroma_db_google_genai"  # change if your DBs are inside a specific folder
vector_dbs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

if not vector_dbs:
    raise ValueError("No vector databases found.")

print("\n Available Models:")
for i, db in enumerate(vector_dbs, start=1):
    print(f"{i}. {db}")

# Let user choose car model
choice = None
while choice is None:
    try:
        selection = int(input("\n Select a car model (press 0 to exit): "))
        if selection == 0:
            print(" Exiting program.")
            exit(0)
        elif 1 <= selection <= len(vector_dbs):
            choice = vector_dbs[selection - 1]
        else:
            print(" Invalid choice. Please select from available options.")
    except ValueError:
        print("Please select from available options.")

print(f"\n Loading vector database for: {choice}\n")

db_path = os.path.join(base_dir, choice)

# Setup retriever and chain with chosen DB
retriever = Chroma(
    persist_directory=db_path,
    embedding_function=GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", google_api_key=api_key
    )
).as_retriever(search_kwargs={"k": 3})

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=GoogleGenerativeAI(model="gemma-3-4b-it", google_api_key=api_key, temperature=0.2),
    retriever=retriever,
    return_source_documents=True,
    output_key="answer"
)

# History and memory management
store = {}
def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

qa_with_history = RunnableWithMessageHistory(
    qa_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
    output_messages_key="answer"
)

# Interactive Q&A loop
print("🔎 Interactive Q&A ready! Type 'exit' to quit.\n")
session_id = "default-session"

while True:
    query = input("❓ Your question: ")
    if query.lower() in ["exit", "quit", "q"]:
        print("👋 Exiting.")
        break

    result = qa_with_history.invoke(
        {"question": query},
        config={"configurable": {"session_id": session_id}}
    )

    print(f"\n💡 {result['answer']}\n" + "-" * 60)
