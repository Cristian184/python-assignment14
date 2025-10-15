# query_db.py
import sqlite3

DB_FILE = "baseball.db"

def query():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("Baseball Database Query Tool")
    print("Enter SQL queries below (e.g., SELECT * FROM events LIMIT 5;)")
    print("Type 'exit' to quit.\n")

    while True:
        q = input("SQL> ")
        if q.lower() in ["exit", "quit"]:
            break
        try:
            cursor.execute(q)
            rows = cursor.fetchall()
            for r in rows:
                print(r)
        except Exception as e:
            print(f"Error: {e}")

    conn.close()
    print("Goodbye.")

if __name__ == "__main__":
    query()
