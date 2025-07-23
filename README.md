# AI-AGENT
This project is a FastAPI-based backend that uses an LLM (via Ollama) to convert natural language queries into SQL for a PostgreSQL database containing sales, product, and total data. It can return query results as JSON or generate bar chart visualizations as images. The project supports CSV-to-Postgres loading and is ready for local development.

---

## Features

- **/ask**: Submit a natural language question, get SQL and results as JSON.
- **/docs**: Interactive API documentation (Swagger UI).
- Loads CSV data into PostgreSQL.
- Modular code for easy extension.

---

## Project Structure

```
Anarix/
│
├── app/
│   ├── api.py         # FastAPI endpoints
│   ├── model.py       # (Optional) LLM prompt and SQL extraction│
│   ├── sql_agent.py   # LLM chat + SQL execution
│   ├── utils.py       # CSV to Postgres loader
│   └── data/
│       ├── product.csv
│       ├── sales.csv
│       └── total.csv
├── main.py            # App entrypoint
├── Req.txt            # Python dependencies
├── .env               # Environment variables (DATABASE_URL, etc.)
├── .gitignore
└── README.md
```

---

## Setup Instructions

1. **Clone the repo and install dependencies:**
    ```sh
    pip install -r Req.txt
    ```

2. **Set up your `.env` file:**
    ```
    DATABASE_URL=postgresql://username:password@localhost:5432/yourdb
    ```

3. **(Optional) Load CSV data into Postgres:**
    ```python
    # In a Python shell
    from app.utils import load_csv_to_postgres
    load_csv_to_postgres("app/data/sales.csv", "sales")
    load_csv_to_postgres("app/data/product.csv", "product")
    load_csv_to_postgres("app/data/total.csv", "total")
    ```

4. **Start Ollama with Llama3 model:**
    ```
    ollama run llama3
    ```

5. **Run the FastAPI server:**
    ```sh
    python main.py
    ```

6. **Open the API docs:**
    - Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Example Usage

- **/ask**:  
  POST JSON:  
  ```json
  { "query": "Show top 5 products by sales" }
  ```
  Response:  
  ```json
  { "sql": "...", "result": [...] }
  ```
---

## Requirements

- Python 3.8+
- PostgreSQL
- Ollama (with Llama3 model)

---