
import json
import sqlite3
import pandas as pd
import re

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def setup_database(db_name='degradation_data.db', json_file_path='./degraders_list_with_images.json'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    data = load_json_data(json_file_path)
    df = pd.DataFrame(data)

    # Clean column names for SQLite compatibility (e.g., remove special characters)
    df.columns = [re.sub(r'[^a-zA-Z0-9_]', '', col) for col in df.columns]
    print(f"Columns after cleaning in setup_database.py: {df.columns.tolist()}")

    # Create table schema dynamically from DataFrame columns
    # Assuming most columns can be TEXT, adjust if specific types are needed
    columns_with_types = []
    for col in df.columns:
        if col == 'Year':
            columns_with_types.append(f'{col} INTEGER')
        elif col in ['Tax_ID', 'Enzyme_ID']:
            columns_with_types.append(f'{col} TEXT') # Storing as TEXT as they might not be purely numeric IDs
        else:
            columns_with_types.append(f'{col} TEXT')
    
    create_table_query = f"CREATE TABLE IF NOT EXISTS degraders ({', '.join(columns_with_types)})"
    cursor.execute(create_table_query)
    conn.commit()

    # Insert data into the table
    # Using 'replace' to handle potential duplicate entries if script is run multiple times
    df.to_sql('degraders', conn, if_exists='replace', index=False)

    conn.close()
    print(f"Database '{db_name}' created and data imported successfully.")

def load_data_from_db(db_name='degradation_data.db'):
    """Loads all data from the 'degraders' table in the SQLite database."""
    try:
        conn = sqlite3.connect(db_name)
        query = "SELECT * FROM degraders"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error loading data from database: {e}")
        return None

if __name__ == "__main__":
    setup_database()
    # Example of how to load data after setup
    # df_loaded = load_data_from_db()
    # if df_loaded is not None:
    #     print("Data loaded successfully:")
    #     print(df_loaded.head())

