import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("sentiment_results.db")

# Read first 10 records
df = pd.read_sql_query("SELECT * FROM results LIMIT 10;", conn)

print(df)

conn.close()
