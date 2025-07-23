from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import ollama
import re

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Check for DB config error
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in your .env file.")

# Connect to PostgreSQL
engine = create_engine(DATABASE_URL)

def extract_sql(text):
    """Extract SQL from LLM response (even if inside ```sql blocks)."""
    match = re.search(r"```sql\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # fallback: try to find first SELECT ... ; statement
    match = re.search(r"(SELECT[\s\S]+?;)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()

def generate_sql_query(user_input):
    prompt = f"""
You are a SQL assistant. Based on the user's request, generate a SQL query using the following PostgreSQL schema:
- sales(item_id, ad_sales, impression, ad_spend, clicks, units_sold, date)
- product(item_id, eligibility_datetime_utc, eligibility, message)
- total(item_id, total_sales, total_units_ordered, date)

User request: {user_input}

SQL:
"""

    try:
        response = ollama.chat(model="llama3", messages=[
            {"role": "user", "content": prompt}
        ])
        sql_query = response['message']['content'].strip()
        sql_query = extract_sql(sql_query)  # <-- Only the SQL

        # Remove this print to avoid duplicate logs
        # print("Generated SQL:", sql_query)

        return sql_query
    except Exception as e:
        print("Error generating SQL from Ollama:", e)
        raise RuntimeError("Failed to generate SQL from language model.") from e

def execute_sql_query(query):
    try:
        print("Generated SQL:", query)  # Print only here
        print("🧠 Executing SQL...")
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.mappings().all()
            print("Query Result:", [dict(row) for row in rows])
            return [dict(row) for row in rows]
    except Exception as e:
        print("❌ SQL Execution Error:")
        print(f"Query: {query}")
        print(f"Error: {e}")
        raise RuntimeError("SQL execution failed.") from e


