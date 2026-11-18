"""
db_config.py — Database configuration loader from .env file.
"""
import os
from dotenv import load_dotenv

# Load .env from project root (two levels up from backend/database/)
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_path)


def get_db_config():
    """Return a dictionary with database connection parameters from .env."""
    return {
        "host": os.getenv("YOUR_HOST", "127.0.0.1"),
        "port": int(os.getenv("YOUR_PORT", "3306")),
        "user": os.getenv("YOUR_USER", "root"),
        "password": os.getenv("YOUR_PASSWORD", ""),
        "database": os.getenv("YOUR_DB_NAME", "football_dw"),
    }


def get_db_host():
    """Return a dictionary with only host/port/user/password (no database)."""
    config = get_db_config()
    return {
        "host": config["host"],
        "port": config["port"],
        "user": config["user"],
        "password": config["password"],
    }
