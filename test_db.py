"""
test_db.py

Purpose:
--------
This script is used to verify that the PostgreSQL (Neon DB)
connection is working correctly.

It reads the DATABASE_URI from the .env file,
creates a SQLAlchemy engine,
and attempts to establish a database connection.

If successful, it confirms the database is reachable.

This file is useful for:
✔ Initial setup validation
✔ Debugging connection issues
✔ Deployment verification
"""

# ======================================================
# Required Imports
# ======================================================

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


# ======================================================
# Load Environment Variables
# ======================================================

# Load variables from .env file
load_dotenv()

# Fetch database URI from environment
uri = os.getenv("DATABASE_URI")

# Print URI (for debugging purposes)
# ⚠️ Remove this print in production to avoid exposing credentials
print(uri)


# ======================================================
# Create Database Engine
# ======================================================

engine = create_engine(uri)

# Attempt to connect
engine.connect()

print("✅ NEON DB CONNECTED")
