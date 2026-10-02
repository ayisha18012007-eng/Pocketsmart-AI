import os

from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-secret-key-change-me"
)

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "pocketsmart.db"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

FRONTEND_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000"
    ).split(",")
    if origin.strip()
]