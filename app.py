"""
app.py

Main Streamlit Application

Purpose:
--------
This application converts user speech (multi-language) or typed natural language 
into SQL queries using an LLM (EURI GPT model), executes them on a PostgreSQL database, 
and automatically visualizes the results.

Primary Focus:
--------------
🎙️ Speech-to-Text Translation using SpeechRecognition + PyAudio
🧠 Natural Language → SQL Conversion
📊 Automatic Data Visualization
"""

# ==============================
# Import Required Libraries
# ==============================

import streamlit as st
from sqlalchemy import create_engine
from config import DATABASE_URI
from utills import get_db_schema, call_euri_llm, execute_sql

import speech_recognition as sr  # Used for Speech-to-Text conversion
import pandas as pd              # Used to structure query results
import plotly.express as px      # Used for automatic visualization


# ==============================
# Streamlit Page Configuration
# ==============================

st.set_page_config(page_title="SQL Assistant", layout="wide")
st.title("🧠 SQL-Powered Data Retrieval Assistant")

# ==========================================================
# STEP 1: Select Language for Speech-to-Text Translation
# ==========================================================

st.subheader("🌐 Choose Language for Speech Recognition")

# Supported languages for Google Speech Recognition
language_map = {
    "English (US)": "en-US",
    "Hindi (India)": "hi-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Chinese (Mandarin)": "zh-CN",
    "Arabic": "ar-SA",
    "Bengali": "bn-IN",
    "Japanese": "ja-JP",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Marathi": "mr-IN"
}

# Dropdown selection
selected_language = st.selectbox("Choose a language", list(language_map.keys()))
language_code = language_map[selected_language]


# ==========================================================
# STEP 2: Speech-to-Text Input Section (Core Feature)
# ==========================================================

st.subheader("🎙️ Speak Your SQL Query")

nl_query = ""  # Natural language query placeholder

# If microphone button is clicked
if st.button("🎤 Start Listening"):

    # Initialize speech recognizer
    recognizer = sr.Recognizer()

    # Capture audio from microphone
    with sr.Microphone() as source:
        st.info(f"Listening in {selected_language}... Speak now.")
        audio = recognizer.listen(source, timeout=6)

    try:
        # Convert captured speech to text using Google Speech API
        nl_query = recognizer.recognize_google(audio, language=language_code)
        st.success(f"You said: {nl_query}")

    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand the audio.")

    except sr.RequestError as e:
        st.error(f"Speech Recognition API error: {e}")

# If speech not used, allow manual text input
else:
    nl_query = st.text_input("Or type your question here:")


# ==========================================================
# STEP 3: Convert Natural Language → SQL → Execute
# ==========================================================

if nl_query:

    # Create database connection using SQLAlchemy
    engine = create_engine(DATABASE_URI)

    # Dynamically fetch database schema
    schema = get_db_schema(engine)

    # Load prompt template for LLM
    with open("prompt_template.txt") as f:
        template = f.read()

    # Format prompt with schema and user question
    prompt = template.format(schema=schema, question=nl_query)

    # Call LLM to generate SQL query
    with st.spinner("🧠 Generating SQL using EURI LLM..."):
        sql_query = call_euri_llm(prompt)

    # Display generated SQL query
    st.code(sql_query, language="sql")

    # Execute SQL and fetch results
    try:
        results, columns = execute_sql(engine, sql_query)

        if results:
            # Convert results into DataFrame
            df = pd.DataFrame(results, columns=columns)

            st.subheader("📊 Query Results:")
            st.dataframe(df, use_container_width=True)

            # ==========================================================
            # STEP 4: Automatic Data Visualization
            # ==========================================================

            st.subheader("📈 Visualization")

            # If first column looks like date/time → Line Chart
            if "date" in df.columns[0].lower() or "time" in df.columns[0].lower():
                fig = px.line(df, x=df.columns[0], y=df.columns[1], title="Line Chart")
                st.plotly_chart(fig, use_container_width=True)

            # If exactly 2 columns → Bar Chart
            elif df.shape[1] == 2:
                fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Bar Chart")
                st.plotly_chart(fig, use_container_width=True)

            # If 3 columns → Scatter Plot
            elif df.shape[1] == 3:
                fig = px.scatter(df, x=df.columns[0], y=df.columns[1],
                                 color=df.columns[2], title="Scatter Plot")
                st.plotly_chart(fig, use_container_width=True)

            # If single column → Histogram
            elif df.shape[1] == 1:
                fig = px.histogram(df, x=df.columns[0], title="Histogram")
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("Visualization not auto-detected — refine your query for 2–3 columns.")

        else:
            st.info("✅ Query executed successfully. No data returned.")

    except Exception as e:
        st.error(f"❌ Error running query: {e}")
