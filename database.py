import sqlite3
from property import Property
import numpy as pd
import pandas as pd


DB_NAME = "vacation.db"

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
                tags=row[5].split(",") if row[5] else []
            )
            properties.append(prop)
        
    return properties

def get_all_properties_df():
    properties = get_all_properties()
    data = [{
        "property_id": p.property_id,
        "location": p.location,
        "type": p.ptype,
        "nightly_price": p.nightly_price,
        "features": p.features,
        "tags": p.tags
    } for p in properties]
    return pd.DataFrame(data)