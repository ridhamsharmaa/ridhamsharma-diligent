import sqlite3
import pandas as pd
import glob
import os

# Make sure database folder exists
os.makedirs("database", exist_ok=True)

# Path to SQLite DB
db_path = "database/ecommerce.db"

# Connect to database
conn = sqlite3.connect(db_path)

print("Loading CSV files into SQLite database...\n")

# Loop through all CSV files
for file in sorted(glob.glob("data/*.csv")):
    table = os.path.basename(file).replace(".csv", "")
    
    print(f"Processing: {table}")
    df = pd.read_csv(file)

    # Load into SQLite table
    df.to_sql(table, conn, if_exists="replace", index=False)

    print(f" → Loaded {len(df)} rows into table '{table}'")

conn.close()

print("\nDone! Database created at: database/ecommerce.db")
