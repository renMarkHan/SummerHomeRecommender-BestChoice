#!/usr/bin/env python3
"""
Property Database Export Script

This script exports all properties from the vacation_rentals.db database
and saves them to a JSON file.
"""

import sqlite3
import json
import os
from datetime import datetime


def get_database_connection():
    """Create and return a database connection."""
    try:
        conn = sqlite3.connect('vacation_rentals.db')
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def export_properties_to_json(output_file='exported_properties.json'):
    """Export all properties from the database to a JSON file."""
    
    # Connect to database
    conn = get_database_connection()
    if not conn:
        return False
    
    try:
        # Create cursor
        cursor = conn.cursor()
        
        # Get all properties
        cursor.execute("""
            SELECT * FROM properties
        """)
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        if not rows:
            print("No properties found in the database.")
            return False
        
        # Convert rows to list of dictionaries
        properties = []
        for row in rows:
            # Convert sqlite3.Row to dict
            property_dict = dict(row)
            
            # Handle special data types
            for key, value in property_dict.items():
                if value is None:
                    property_dict[key] = None
                elif isinstance(value, (int, float)):
                    # Keep numbers as is
                    pass
                else:
                    # Convert to string for other types
                    property_dict[key] = str(value)
            
            properties.append(property_dict)
        
        # Create export data with metadata
        export_data = {
            "export_info": {
                "export_date": datetime.now().isoformat(),
                "total_properties": len(properties),
                "database_file": "vacation_rentals.db",
                "table_name": "properties"
            },
            "properties": properties
        }
        
        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully exported {len(properties)} properties to '{output_file}'")
        print(f"Export completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        # Close connection
        conn.close()


def export_properties_simple(output_file='properties_simple.json'):
    """Export properties in a simple format without metadata."""
    
    conn = get_database_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM properties")
        rows = cursor.fetchall()
        
        if not rows:
            print("No properties found in the database.")
            return False
        
        # Convert to simple list format
        properties = []
        for row in rows:
            property_dict = dict(row)
            
            # Handle data types
            for key, value in property_dict.items():
                if value is None:
                    property_dict[key] = None
                elif isinstance(value, (int, float)):
                    pass
                else:
                    property_dict[key] = str(value)
            
            properties.append(property_dict)
        
        # Write simple format
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(properties, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully exported {len(properties)} properties to '{output_file}' (simple format)")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()


def show_database_info():
    """Show information about the database and properties table."""
    
    conn = get_database_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("PRAGMA table_info(properties)")
        columns = cursor.fetchall()
        
        print("Database Information:")
        print("=" * 50)
        print(f"Database file: vacation_rentals.db")
        print(f"Table: properties")
        print(f"Columns ({len(columns)}):")
        
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Get row count
        cursor.execute("SELECT COUNT(*) FROM properties")
        count = cursor.fetchone()[0]
        print(f"Total properties: {count}")
        
        # Show sample data
        if count > 0:
            cursor.execute("SELECT * FROM properties LIMIT 1")
            sample = cursor.fetchone()
            print(f"\nSample property keys: {list(sample.keys())}")
        
        print("=" * 50)
        
    except sqlite3.Error as e:
        print(f"Error getting database info: {e}")
    finally:
        conn.close()


def main():
    """Main function to run the export."""
    
    print("Property Database Export Tool")
    print("=" * 40)
    
    # Show database info first
    show_database_info()
    print()
    
    # Export with metadata
    print("Exporting properties with metadata...")
    if export_properties_to_json('exported_properties.json'):
        print("✓ Full export completed")
    else:
        print("✗ Full export failed")
    
    print()
    
    # Export simple format
    print("Exporting properties in simple format...")
    if export_properties_simple('properties_simple.json'):
        print("✓ Simple export completed")
    else:
        print("✗ Simple export failed")
    
    print()
    print("Export process completed!")
    
    # List created files
    files = ['exported_properties.json', 'properties_simple.json']
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"File: {file} ({size} bytes)")


if __name__ == "__main__":
    main()
