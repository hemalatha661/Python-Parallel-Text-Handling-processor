**Python-Parallel-Text-Handling-processor**
 Python-Parallel-Text-Handling-Processor is a rule-based sentiment analysis system that processes multiple text review files and compares sequential execution with multiprocessing (parallel execution) using CPU cores.

The project demonstrates how parallel computing improves performance in text processing tasks while storing results in a structured SQLite database.
    
**How It Works**

Reads multiple .txt files from the reviews/ folder.

Applies rule-based sentiment scoring:

Positive words → +1

Negative words → -1

Calculates final sentiment:

Score > 0 → Positive

Score < 0 → Negative

Score = 0 → Neutral

**Runs analysis in:**

Sequential mode

Multiprocessing mode

Compares execution times.

Stores results in SQLite database (reviews.db).
