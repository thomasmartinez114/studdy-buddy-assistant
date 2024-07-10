import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

client = openai.OpenAI()

# === Create Vector Store === #
vector_store = client.beta.vector_stores.create(name="Knowledgebase")
print(f"Vector Store ID - {vector_store.id}")

# === Upload File === #
file_paths = ["./files/cryptocurrency.pdf"]
file_streams = [open(path, "rb") for path in file_paths]

# === Add files to Vector Store === #
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id,
    files=file_streams
)

# === Check the status of Files === #
print(f"File Status {file_batch.status}")

# === Update the Assistant with a Vector Store
assistant = client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)
print("Assistant Updated with vector store!")

# === Create a Thread === #
thread = client.beta.threads.create()
print(f"Your Thread ID is - {thread.id}\n\n")

# === Run a Loop where user can ask questions === #
while True:
    text = input("What's your question?\n")

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    message_content = messages[0].content[0].text
    print("Response: \n")
    print(f"{message_content.value}\n")