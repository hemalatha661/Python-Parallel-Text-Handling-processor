**Python-Parallel-Text-Handling-Processor**

**Project Overview**
This project demonstrates text processing using Python.  
It reads multiple text files, performs rule-based sentiment analysis, and compares the performance of sequential and multiprocessing execution.  
The results are stored in an SQLite database.

**Features**
- Processes multiple text files
- Rule-based sentiment analysis (Positive / Negative / Neutral)
- Sequential execution
- Parallel execution using multiprocessing
- Execution time comparison
- SQLite database integration

**Project Structure**
python-parallel-text-handling/
│
├── main.py
├── database.py
├── reviews/
│ └── review1.txt
├── reviews.db
└── README.md

 **Technologies Used**
- Python
- Multiprocessing Module
- SQLite (sqlite3)
- OS Module
- Time Module

  
**Database Setup**
This project uses **SQLite** as the database.

- Database file name: `reviews.db`
- The database is automatically created when running the program.
- Table name: `reviews`

Table Structure

| Column Name | Type    | Description |
|-------------|---------|-------------|
| id          | INTEGER | Primary Key (Auto Increment) |
| file_name   | TEXT    | Name of review file |
| score       | INTEGER | Sentiment score |
| sentiment   | TEXT    | Final result (Positive/Negative/Neutral) |
| process_id  | INTEGER | Process ID (for multiprocessing) |

The `database.py` file:
- Creates the database and table
- Inserts processed results
- Clears previous records if needed
