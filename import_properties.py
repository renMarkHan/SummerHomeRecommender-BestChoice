#!/usr/bin/env python3
"""
Property Database Import Script

This script imports properties from a JSON file back into the vacation_rentals.db database.
Automatically creates database and table if they don't exist.
"""

import sqlite3
import json
import os
import sys
import argparse
from datetime import datetime


def get_database_connection():
    """Create and return a database connection."""
    try:
        conn = sqlite3.connect('vacation_rentals.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def check_table_exists(conn, table_name='properties'):
    """Check if the properties table exists."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Error checking table existence: {e}")
        return False


def create_properties_table(conn):
    """Create the properties table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                property_id INTEGER PRIMARY KEY,
                location TEXT NOT NULL,
                type TEXT,
                nightly_price REAL,
                features TEXT,
                tags TEXT,
                image_url TEXT,
                image_alt TEXT,
                latitude REAL,
                longitude REAL
            )
        """)
        conn.commit()
        print("✓ Properties table created successfully")
        return True
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        return False


def ensure_database_setup():
    """Ensure database and table exist, create if necessary."""
    conn = get_database_connection()
    if not conn:
        return False
    
    try:
        # Check if table exists
        if not check_table_exists(conn):
            print("📋 Properties table not found, creating...")
            if not create_properties_table(conn):
                return False
        else:
            print("✓ Properties table already exists")
        
        return True
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False
    finally:
        conn.close()


def clear_properties_table(conn):
    """Clear all existing properties from the table."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM properties")
        conn.commit()
        print("✓ Cleared existing properties table")
        return True
    except sqlite3.Error as e:
        print(f"Error clearing table: {e}")
        return False


def import_properties_from_json(json_file='properties_simple.json', clear_existing=True):
    """Import properties from JSON file into the database."""
    
    # Check if JSON file exists
    if not os.path.exists(json_file):
        print(f"❌ JSON file '{json_file}' not found")
        return False
    
    # Ensure database and table exist
    if not ensure_database_setup():
        print("❌ Failed to set up database")
        return False
    
    # Connect to database
    conn = get_database_connection()
    if not conn:
        return False
    
    try:
        # Read JSON file
        print(f"📖 Reading JSON file: {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            properties = json.load(f)
        
        if not isinstance(properties, list):
            print("❌ JSON file should contain an array of properties")
            return False
        
        print(f"📊 Found {len(properties)} properties in JSON file")
        
        # Clear existing data if requested
        if clear_existing:
            if not clear_properties_table(conn):
                return False
        
        # Prepare insert statement
        insert_sql = """
            INSERT INTO properties (
                property_id, location, type, nightly_price, features, 
                tags, image_url, image_alt, latitude, longitude
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor = conn.cursor()
        imported_count = 0
        skipped_count = 0
        
        # Import each property
        for property_data in properties:
            try:
                # Extract values with safe defaults
                property_id = property_data.get('property_id')
                location = property_data.get('location', '')
                property_type = property_data.get('type', '')
                nightly_price = property_data.get('nightly_price', 0.0)
                features = property_data.get('features', '')
                tags = property_data.get('tags', '')
                image_url = property_data.get('image_url', '')
                image_alt = property_data.get('image_alt', '')
                latitude = property_data.get('latitude', 0.0)
                longitude = property_data.get('longitude', 0.0)
                
                # Insert into database
                cursor.execute(insert_sql, (
                    property_id, location, property_type, nightly_price, features,
                    tags, image_url, image_alt, latitude, longitude
                ))
                
                imported_count += 1
                
                # Progress indicator
                if imported_count % 50 == 0:
                    print(f"   Imported {imported_count} properties...")
                
            except sqlite3.Error as e:
                print(f"⚠️  Error importing property {property_data.get('property_id', 'unknown')}: {e}")
                skipped_count += 1
                continue
        
        # Commit all changes
        conn.commit()
        
        print(f"✅ Successfully imported {imported_count} properties")
        if skipped_count > 0:
            print(f"⚠️  Skipped {skipped_count} properties due to errors")
        
        # Verify import
        cursor.execute("SELECT COUNT(*) FROM properties")
        total_in_db = cursor.fetchone()[0]
        print(f"📊 Total properties in database: {total_in_db}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        conn.close()


def import_with_upsert(json_file='properties_simple.json'):
    """Import properties using UPSERT (INSERT OR REPLACE) to handle duplicates."""
    
    if not os.path.exists(json_file):
        print(f"❌ JSON file '{json_file}' not found")
        return False
    
    # Ensure database and table exist
    if not ensure_database_setup():
        print("❌ Failed to set up database")
        return False
    
    conn = get_database_connection()
    if not conn:
        return False
    
    try:
        # Read JSON file
        print(f"📖 Reading JSON file: {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            properties = json.load(f)
        
        print(f"📊 Found {len(properties)} properties in JSON file")
        
        # Use UPSERT to handle duplicates
        upsert_sql = """
            INSERT OR REPLACE INTO properties (
                property_id, location, type, nightly_price, features, 
                tags, image_url, image_alt, latitude, longitude
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor = conn.cursor()
        imported_count = 0
        
        for property_data in properties:
            try:
                # Extract values
                property_id = property_data.get('property_id')
                location = property_data.get('location', '')
                property_type = property_data.get('type', '')
                nightly_price = property_data.get('nightly_price', 0.0)
                features = property_data.get('features', '')
                tags = property_data.get('tags', '')
                image_url = property_data.get('image_url', '')
                image_alt = property_data.get('image_alt', '')
                latitude = property_data.get('latitude', 0.0)
                longitude = property_data.get('longitude', 0.0)
                
                # Upsert into database
                cursor.execute(upsert_sql, (
                    property_id, location, property_type, nightly_price, features,
                    tags, image_url, image_alt, latitude, longitude
                ))
                
                imported_count += 1
                
                if imported_count % 50 == 0:
                    print(f"   Processed {imported_count} properties...")
                
            except sqlite3.Error as e:
                print(f"⚠️  Error processing property {property_data.get('property_id', 'unknown')}: {e}")
                continue
        
        conn.commit()
        print(f"✅ Successfully processed {imported_count} properties (with UPSERT)")
        
        # Verify final count
        cursor.execute("SELECT COUNT(*) FROM properties")
        total_in_db = cursor.fetchone()[0]
        print(f"📊 Total properties in database: {total_in_db}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()


def show_import_options():
    """Show available import options."""
    print("\n📋 Import Options:")
    print("1. Clear existing data and import fresh")
    print("2. Import with UPSERT (handle duplicates)")
    print("3. View current database status")
    print("4. Exit")


def main():
    """Main function to run the import."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Property Database Import Tool')
    parser.add_argument('--auto-import', action='store_true', 
                       help='Automatically import data without interactive prompts')
    parser.add_argument('--json-file', default='properties_simple.json',
                       help='JSON file to import (default: properties_simple.json)')
    
    args = parser.parse_args()
    
    # Check database setup first
    print("🔍 Checking database setup...")
    if ensure_database_setup():
        print("✅ Database is ready")
    else:
        print("❌ Failed to set up database")
        return
    
    # Auto-import mode for run.sh
    if args.auto_import:
        print("🔄 Auto-import mode: Importing data from JSON...")
        if import_properties_from_json(args.json_file, clear_existing=True):
            print("✅ Auto-import completed successfully!")
            return
        else:
            print("❌ Auto-import failed!")
            sys.exit(1)
    
    # Interactive mode
    print("Property Database Import Tool")
    print("=" * 40)
    
    while True:
        show_import_options()
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            print("\n🔄 Clearing existing data and importing fresh...")
            if import_properties_from_json(args.json_file, clear_existing=True):
                print("✅ Import completed successfully!")
            else:
                print("❌ Import failed!")
                
        elif choice == '2':
            print("\n🔄 Importing with UPSERT...")
            if import_with_upsert(args.json_file):
                print("✅ Import completed successfully!")
            else:
                print("❌ Import failed!")
                
        elif choice == '3':
            print("\n📊 Current database status:")
            conn = get_database_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM properties")
                    count = cursor.fetchone()[0]
                    print(f"Total properties: {count}")
                    
                    if count > 0:
                        cursor.execute("SELECT property_id, location, type FROM properties LIMIT 5")
                        sample = cursor.fetchall()
                        print("Sample properties:")
                        for prop in sample:
                            print(f"  - ID {prop[0]}: {prop[1]} ({prop[2]})")
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    conn.close()
                    
        elif choice == '4':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid option. Please select 1-4.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
