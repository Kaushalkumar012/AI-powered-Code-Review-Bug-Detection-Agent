from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="app/.env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("TOKEN LOADED:", GITHUB_TOKEN)