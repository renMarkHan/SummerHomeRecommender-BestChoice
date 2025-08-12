import sqlite3

DB_NAME = "vacation_rentals.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        group_size INTEGER NOT NULL,
        preferred_env TEXT NOT NULL,
        budget_min REAL NOT NULL,
        budget_max REAL NOT NULL,
        travel_start_date TEXT,
        travel_end_date TEXT
    )
    ''')

    # Create properties table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        property_id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        type TEXT NOT NULL,
        nightly_price REAL NOT NULL,
        features TEXT,
        tags TEXT
    )
    ''')

    conn.commit()
    conn.close()
