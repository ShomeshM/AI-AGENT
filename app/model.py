import requests
import re

def extract_sql(text):
    """Extract SQL from LLM response (even if inside ```sql blocks)."""
    match = re.search(r"```sql\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def generate_sql_query(question: str) -> str:
    schema_hint = """
You are a PostgreSQL SQL assistant.
Only return the final SQL query without any explanation.
Assume the following tables:

1. sales(date DATE, item_id INT, ad_sales FLOAT, impression INT, ad_spend FLOAT, clicks INT, units_sold INT)
2. product(eligibility_datetime_utc TIMESTAMP, item_id INT, eligibility BOOLEAN, message TEXT)
3. total(date DATE, item_id INT, total_sales FLOAT, total_units_ordered INT)

Notes:
- Join on item_id for all three tables
- ad_sales is revenue from ads
- total_sales is overall sales
- eligibility is a boolean value in product
- units_sold and total_units_ordered are counts of quantity
"""

    full_prompt = schema_hint + "\nUser question:\n" + question

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": full_prompt,
            "stream": False
        }
    )

    data = response.json()
    return extract_sql(data["response"])
