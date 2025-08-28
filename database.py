import sqlite3
from property import Property


DB_NAME = "vacation_rentals.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table with weighted attributes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        group_size INTEGER,
        preferred_env TEXT,
        budget_min REAL,
        budget_max REAL,
        travel_start_date TEXT,
        travel_end_date TEXT,
        weighed_location INTEGER DEFAULT 1,
        weighed_type INTEGER DEFAULT 1,
        weighed_features INTEGER DEFAULT 1,
        weighed_price INTEGER DEFAULT 1
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
        tags TEXT,
        image_url TEXT,
        image_alt TEXT
    )
    ''')

    # Add weighted attributes columns to existing users table if they don't exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN weighed_location INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN weighed_type INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN weighed_features INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN weighed_price INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add image columns to existing properties table if they don't exist
    try:
        cursor.execute("ALTER TABLE properties ADD COLUMN image_url TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE properties ADD COLUMN image_alt TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()
    conn.close()


def get_all_properties():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties")
    rows = cursor.fetchall()
    conn.close()
    properties = []

    for row in rows:
            prop = Property(
                property_id=row[0],
                location=row[1],
                ptype=row[2],
                nightly_price=row[3],
                features=row[4].split(",") if row[4] else [],
                tags=row[5].split(",") if row[5] else [],
                image_url=row[6] if len(row) > 6 else None,
                image_alt=row[7] if len(row) > 7 else None,
                latitude=row[8] if len(row) > 8 else None,
                longitude=row[9] if len(row) > 9 else None
            )
            properties.append(prop)
        
    return properties
