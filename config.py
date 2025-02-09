import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")

    # ✅ Use SQLite instead of PostgreSQL
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:////tmp/secrets.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
