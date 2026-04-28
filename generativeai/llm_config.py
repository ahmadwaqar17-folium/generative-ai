from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

# Load the shared .env from the repo root
# Works whether you run from generativeai/ or from the project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

llm = init_chat_model("groq:qwen/qwen3-32b")
