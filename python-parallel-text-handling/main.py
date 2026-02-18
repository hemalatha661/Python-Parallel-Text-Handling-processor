import os
import time
from multiprocessing import Pool, cpu_count
from database import setup_database, save_results, clear_table

# -----------------------------
# Configuration
# -----------------------------

REVIEWS_FOLDER = "reviews"

POSITIVE_WORDS = {"good", "great", "excellent", "amazing", "happy", "love", "wonderful", "best", "nice"}
NEGATIVE_WORDS = {"bad", "worst", "poor", "terrible", "hate", "awful", "sad", "disappointed"}

# -----------------------------
# Sentiment Analysis Function
# -----------------------------

def analyze_review(file_path):
    process_id = os.getpid()

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().lower()

    words = text.split()
    score = 0

    for word in words:
        if word in POSITIVE_WORDS:
            score += 1
        elif word in NEGATIVE_WORDS:
            score -= 1

    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return (os.path.basename(file_path), score, sentiment, process_id)


# -----------------------------
# Sequential Processing
# -----------------------------

def run_sequential(file_list):
    print("\nRunning Sequential Processing...\n")
    start_time = time.time()

    results = [analyze_review(file) for file in file_list]

    execution_time = time.time() - start_time
    print(f"Sequential Execution Time: {execution_time:.4f} seconds")
    return results, execution_time


# -----------------------------
# Multiprocessing
# -----------------------------

def run_multiprocessing(file_list):
    print("\nRunning Multiprocessing...\n")
    start_time = time.time()

    with Pool(cpu_count()) as pool:
        results = pool.map(analyze_review, file_list)

    execution_time = time.time() - start_time
    print(f"Multiprocessing Execution Time: {execution_time:.4f} seconds")
    return results, execution_time


# -----------------------------
# Main Function
# -----------------------------

def main():
    setup_database()
    clear_table()

    file_list = [
        os.path.join(REVIEWS_FOLDER, file)
        for file in os.listdir(REVIEWS_FOLDER)
        if file.endswith(".txt")
    ]

    if not file_list:
        print("No review files found!")
        return

    # Sequential
    seq_results, seq_time = run_sequential(file_list)

    # Multiprocessing
    mp_results, mp_time = run_multiprocessing(file_list)

    # Save final results
    save_results(mp_results)

    print("\n--- Sample Results ---")
    for result in mp_results:
        print(f"File: {result[0]}, Score: {result[1]}, Sentiment: {result[2]}, Process ID: {result[3]}")

    print("\nPerformance Comparison:")
    print(f"Sequential Time      : {seq_time:.4f} sec")
    print(f"Multiprocessing Time : {mp_time:.4f} sec")
    print(f"CPU Cores Used       : {cpu_count()}")

    print("\nResults stored in reviews.db")


if __name__ == "__main__":
    main()
