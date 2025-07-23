from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def load_csv_to_postgres(csv_path, table_name):
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)