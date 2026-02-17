"""
config.py

Purpose:
--------
This file is used to manage environment configuration variables
such as API keys and database connection strings.

Why This File Exists:
---------------------
Instead of hardcoding sensitive information inside main.py,
we store them in a separate configuration module.

This improves:
✔ Security (no secrets in source code)
✔ Modularity
✔ Maintainability
✔ Clean project structure

Environment variables are loaded from a `.env` file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ======================================================
# EURI API Configuration
# ======================================================

# API Key (stored securely in .env file)
EURI_API_KEY = os.getenv("EURI_API_KEY")

# Public API endpoint (safe to keep in source code)
EURI_API_URL = "https://api.euron.one/api/v1/euri/chat/completions"

# LLM Model Name
MODEL_NAME = "gpt-4.1-nano"

# ======================================================
# Database Configuration
# ======================================================

# PostgreSQL connection string (stored securely in .env file)
DATABASE_URI = os.getenv("DATABASE_URI")
