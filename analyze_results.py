import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "sentiment_results.db")



# ==============================
# Connect to Database
# ==============================

conn = sqlite3.connect(db_path)
# ==============================
# 1️⃣ Sentiment Distribution Graph
# ==============================

def show_sentiment_distribution():
    query = """
    SELECT sentiment, COUNT(*) as total
    FROM results
    GROUP BY sentiment
    """

    df = pd.read_sql_query(query, conn)

    print("\nSentiment Summary:")
    print(df)

    # Plot graph
    plt.figure()
    plt.bar(df["sentiment"], df["total"])
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.title("Sentiment Distribution")
    plt.show()


# ==============================
# 2️⃣ Search Sentence Function
# ==============================

def search_sentence():
    keyword = input("\nEnter keyword to search: ")

    query = f"""
    SELECT text, score, sentiment
    FROM results
    WHERE text LIKE '%{keyword}%'
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("No results found.")
    else:
        print("\nTop Matching Results:")
        print(df)


# ==============================
# Menu System
# ==============================

def main():
    while True:
        print("\n==== Sentiment Analysis Dashboard ====")
        print("1. Show Sentiment Distribution")
        print("2. Search Sentence")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            show_sentiment_distribution()

        elif choice == "2":
            search_sentence()

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
    conn.close()
