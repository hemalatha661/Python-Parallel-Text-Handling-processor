import sqlite3
import pandas as pd
import numpy as np
import multiprocessing as mp
from datetime import datetime
import os
import time


# ==================================================
# 1️⃣ Rule-Based Keyword System
# ==================================================

positive_words = {
    "good", "great", "excellent", "amazing", "happy",
    "love", "awesome", "fantastic", "best", "wonderful"
}

negative_words = {
    "bad", "worst", "terrible", "sad", "hate",
    "angry", "poor", "awful", "disappointed", "horrible"
}


def calculate_score(text):
    score = 0
    words = str(text).lower().split()

    for word in words:
        word = word.strip(".,!?")
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    return score


def get_sentiment(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"


# ==================================================
# 2️⃣ Database Creation
# ==================================================

def create_database():
    try:
        with sqlite3.connect("sentiment_results.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT,
                    score INTEGER,
                    sentiment TEXT,
                    timestamp TEXT
                )
            """)
    except sqlite3.Error as e:
        print("Database Error:", e)


# ==================================================
# 3️⃣ Multiprocessing Worker
# ==================================================

def process_chunk(chunk):
    results = []

    for _, row in chunk.iterrows():
        text = row["sentence"]
        score = calculate_score(text)
        sentiment = get_sentiment(score)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        results.append((text, score, sentiment, timestamp))

    return results



# ==================================================
# 4️⃣ Main Dataset Processing
# ==================================================

def process_dataset(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError("Dataset file not found.")

        start_time = time.time()

        print("Reading dataset...")
        df = pd.read_csv(file_path)

        cpu_count = mp.cpu_count()
        print(f"Using {cpu_count} CPU cores for processing")

        # Split dataframe into equal chunks
        chunks = np.array_split(df, cpu_count)

        print("Starting multiprocessing...")

        with mp.Pool(cpu_count) as pool:
            processed_data = pool.map(process_chunk, chunks)

        # Flatten results
        all_records = [
            record for sublist in processed_data for record in sublist
        ]

        print("Inserting into database...")

        with sqlite3.connect("sentiment_results.db") as conn:
            cursor = conn.cursor()

            cursor.executemany("""
                INSERT INTO results (text, score, sentiment, timestamp)
                VALUES (?, ?, ?, ?)
            """, all_records)

            conn.commit()

        end_time = time.time()

        print("Multiprocessing completed successfully!")
        print(f"Total records inserted: {len(all_records)}")
        print(f"Execution time: {round(end_time - start_time, 2)} seconds")

    except FileNotFoundError as fe:
        print("File Error:", fe)

    except pd.errors.EmptyDataError:
        print("Error: Dataset file is empty.")

    except sqlite3.Error as db_error:
        print("Database Error:", db_error)

    except Exception as e:
        print("Unexpected Error:", e)


# ==================================================
# 5️⃣ Main Execution Block (Windows Safe)
# ==================================================

if __name__ == "__main__":
    create_database()
    process_dataset("train_data.csv")


