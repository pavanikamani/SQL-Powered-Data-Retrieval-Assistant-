**SQL Voice Assistant – LLM Powered Data Retrieval**
An AI-powered Streamlit application that converts natural language (text or speech) into executable SQL queries using an LLM (EURI GPT model), executes them on a SQL database, and dynamically visualizes the results.
This system enables users to interact with any SQL-based database using plain English instead of writing queries manually.

**🚀 Features**
🎙️ Speech-to-Text support (multi-language)
🧠 Natural Language → SQL conversion (EURI API)
🗄️ Works with SQL systems (PostgreSQL, MySQL, etc.)
🔗 Supports complex queries & multi-table joins
📊 Automatic data visualization
🔐 Secure configuration using .env
⚡ Modular and clean architecture
**🏗️ Architecture Flow**
User (Speech/Text)
        ↓
Streamlit UI
        ↓
Speech-to-Text (if used)
        ↓
Database Schema Extraction
        ↓
Prompt Template + Schema + Question
        ↓
EURI LLM API
        ↓
Generated SQL Query
        ↓
SQL Database Execution
        ↓
Tabular Results + Visualization

**🛠️ Tech Stack**
Python 3.10
Streamlit
SQLAlchemy
PostgreSQL (Neon DB)
EURI GPT-4.1 Nano
SpeechRecognition + PyAudio
Plotly

**⚙️ Installation**
conda create -n sqlvoice python=3.10
conda activate sqlvoice
pip install -r requirements.txt
streamlit run app.py

**🔐 Environment Variables**
Create a .env file:
DATABASE_URI=your_database_uri
EURI_API_KEY=your_api_key

**📁 Project Structure**
app.py              → UI + Speech-to-SQL pipeline
utills.py           → Schema, LLM call, SQL execution
config.py           → Environment configuration
prompt_template.txt → Prompt engineering

**🎯 Capabilities**
✔ Interact with any SQL database
✔ Run complex analytical queries
✔ Perform joins across multiple tables
✔ Convert speech to SQL
✔ Automatically visualize results






