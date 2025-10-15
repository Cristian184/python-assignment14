# import_to_db.py
import sqlite3
import pandas as pd
import os

DB_FILE = "baseball.db"
DATA_FOLDER = "data"

def import_csvs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".csv"):
            table_name = file.replace(".csv", "")
            df = pd.read_csv(os.path.join(DATA_FOLDER, file))
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Imported {file} into table '{table_name}'")

    conn.commit()
    conn.close()
    print("Database import complete.")

if __name__ == "__main__":
    import_csvs()
