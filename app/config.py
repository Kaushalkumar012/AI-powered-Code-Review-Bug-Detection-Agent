from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="app/.env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")