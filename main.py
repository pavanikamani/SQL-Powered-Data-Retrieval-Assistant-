User Input
     ↓
Prompt Template
     ↓
Schema Injection
     ↓
EURI LLM
     ↓
Generated SQL
     ↓
Database Execution
     ↓
Tabular Output


"""
main.py

Purpose:
--------
This file represents the Streamlit UI layer of the application.

Workflow:
---------
1️⃣ Accept natural language input from user
2️⃣ Fetch database schema dynamically
3️⃣ Read external prompt template
4️⃣ Inject schema + user question into prompt
5️⃣ Send final prompt to EURI LLM
6️⃣ Receive generated SQL query
7️⃣ Execute SQL on PostgreSQL database
8️⃣ Display results in tabular format

This file acts as the orchestration layer
connecting UI → LLM → Database → Output.
"""

# ======================================================
# Import Required Libraries
# ======================================================

import streamlit as st
from sqlalchemy import create_engine
from config import DATABASE_URI
from utills import get_db_schema, call_euri_llm, execute_sql


# ======================================================
# Streamlit UI Configuration
# ======================================================

st.set_page_config(page_title="SQL Assistant", layout="wide")
st.title("🧠 SQL-Powered Data Retrieval Assistant")


# ======================================================
# Step 1: Accept User Natural Language Query
# ======================================================

nl_query = st.text_input("Ask your question (in natural language):")


# ======================================================
# Step 2: Process Query When User Submits
# ======================================================

if nl_query:

    # Create database connection using SQLAlchemy
    engine = create_engine(DATABASE_URI)

    # Dynamically extract database schema
    schema = get_db_schema(engine)

    # --------------------------------------------------
    # Step 3: Load Prompt Template
    # --------------------------------------------------

    # Read structured prompt from external file
    with open("prompt_template.txt") as f:
        template = f.read()

    # Combine:
    #   - Database schema
    #   - User natural language question
    # into one final prompt
    prompt = template.format(schema=schema, question=nl_query)

    # --------------------------------------------------
    # Step 4: Send Prompt to EURI LLM
    # --------------------------------------------------

    with st.spinner("Generating SQL using EURI LLM..."):
        sql_query = call_euri_llm(prompt)

    # Display generated SQL query for transparency
    st.code(sql_query, language="sql")

    # --------------------------------------------------
    # Step 5: Execute SQL and Display Results
    # --------------------------------------------------

    try:
        results, columns = execute_sql(engine, sql_query)

        if results:
            # Display results in structured tabular format
            st.dataframe(results, use_container_width=True)
        else:
            st.info("Query executed successfully. No data returned.")

    except Exception as e:
        st.error(f"Error running query: {e}")
