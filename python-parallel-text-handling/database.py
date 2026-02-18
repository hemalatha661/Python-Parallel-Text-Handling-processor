import sqlite3

DATABASE_NAME = "reviews.db"

def setup_database():
    """
    Creates the reviews table if it does not exist.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            score INTEGER,
            sentiment TEXT,
            process_id INTEGER
        )
    """)

    conn.commit()
    conn.close()


def save_results(results):
    """
    Inserts sentiment analysis results into database.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO reviews (file_name, score, sentiment, process_id)
        VALUES (?, ?, ?, ?)
    """, results)

    conn.commit()
    conn.close()


def clear_table():
    """
    Optional: Clears previous records before inserting new ones.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reviews")

    conn.commit()
    conn.close()
