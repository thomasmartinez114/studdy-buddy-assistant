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