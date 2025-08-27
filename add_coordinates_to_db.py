#!/usr/bin/env python3
"""
Add coordinate columns to properties database
"""

import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def add_coordinate_columns():
    """Add latitude and longitude columns to properties table"""
    try:
        conn = sqlite3.connect("properties.db")
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(properties)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if "latitude" not in columns:
            cursor.execute("ALTER TABLE properties ADD COLUMN latitude REAL")
            logger.info("Latitude column added successfully")
        else:
            logger.info("Latitude column already exists")
        
        if "longitude" not in columns:
            cursor.execute("ALTER TABLE properties ADD COLUMN longitude REAL")
            logger.info("Longitude column added successfully")
        else:
            logger.info("Longitude column already exists")
        
        # Set default coordinates for existing records (Toronto downtown)
        cursor.execute("UPDATE properties SET latitude = 43.6532, longitude = -79.3832 WHERE latitude IS NULL OR longitude IS NULL")
        
        conn.commit()
        logger.info("Coordinate columns added, existing records set to Toronto downtown coordinates")
        
    except Exception as e:
        logger.error(f"Failed to add coordinate columns: {e}")
        conn.rollback()
    finally:
        conn.close()

def verify_coordinates():
    """Verify coordinate columns were added correctly"""
    try:
        conn = sqlite3.connect("properties.db")
        cursor = conn.cursor()
        
        # Count total properties
        cursor.execute("SELECT COUNT(*) FROM properties")
        total_count = cursor.fetchone()[0]
        
        # Count properties with coordinates
        cursor.execute("SELECT COUNT(*) FROM properties WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
        coord_count = cursor.fetchone()[0]
        
        logger.info(f"Total properties: {total_count}")
        logger.info(f"Properties with coordinates: {coord_count}")
        
    except Exception as e:
        logger.error(f"Failed to verify coordinates: {e}")
    finally:
        conn.close()

def main():
    """Main execution function"""
    logger.info("Starting coordinate column addition...")
    
    try:
        add_coordinate_columns()
        verify_coordinates()
        logger.info("Coordinate columns added successfully!")
        
    except Exception as e:
        logger.error(f"Script execution failed: {e}")

if __name__ == "__main__":
    main()
