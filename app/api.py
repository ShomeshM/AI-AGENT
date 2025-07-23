from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
from app.sql_agent import generate_sql_query, execute_sql_query
from app.plot import plot_result

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/ask")
def ask(query: Query):
    try:
        sql = generate_sql_query(query.query)
        result = execute_sql_query(sql)
        return {"sql": sql, "result": result}
    except Exception as e:
        print("Error in /ask endpoint:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/visualize")
def visualize(query: Query):
    try:
        sql = generate_sql_query(query.query)
        result = execute_sql_query(sql)

        filename = f"output_{uuid.uuid4().hex}.png"
        image_path = plot_result(result, filename)

        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        print("Error in /visualize endpoint:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Running fine. Navigate to /docs for the API documentation."}