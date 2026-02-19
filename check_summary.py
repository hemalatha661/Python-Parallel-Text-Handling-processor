import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("sentiment_results.db")

# Query summary
df = pd.read_sql_query("""
SELECT sentiment, COUNT(*) as total
FROM results
GROUP BY sentiment;
""", conn)

print(df)

conn.close()
