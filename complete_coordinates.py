#!/usr/bin/env python3
"""
Complete coordinate information for properties
"""

import sqlite3
import requests
import time
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_PATH = "properties.db"

def get_coordinates_from_nominatim(location: str) -> tuple:
    """Get coordinates from Nominatim API"""
    try:
        if not location:
            return None, None
        
        # Build query URL
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': f"{location}, Canada",
            'format': 'json',
            'limit': 1
        }
        
        # Send request with User-Agent header
        headers = {
            'User-Agent': 'CozyDoDo/1.0 (https://cozydodo.com; contact@cozydodo.com)'
        }
        
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            return None, None
            
    except Exception as e:
        logger.error(f"Failed to get coordinates {location}: {e}")
        return None, None

def update_property_coordinates():
    """Update coordinates for all properties"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Get all properties that need coordinate updates
        cursor.execute("SELECT property_id, location FROM properties WHERE latitude IS NULL OR longitude IS NULL")
        properties = cursor.fetchall()
        
        if not properties:
            logger.info("All properties already have coordinate information")
            return
        
        total_properties = len(properties)
        logger.info(f"Need to complete coordinates for {total_properties} properties")
        
        updated_count = 0
        failed_count = 0
        
        for i, (property_id, location) in enumerate(properties, 1):
            try:
                logger.info(f"Processing progress: {i}/{total_properties} - Property {property_id}: {location}")
                
                if not location:
                    continue
                
                # Get coordinates
                lat, lon = get_coordinates_from_nominatim(location)
                
                if lat is not None and lon is not None:
                    # Update database
                    cursor.execute(
                        "UPDATE properties SET latitude = ?, longitude = ? WHERE property_id = ?",
                        (lat, lon, property_id)
                    )
                    logger.info(f"Property {property_id} coordinates updated successfully")
                    updated_count += 1
                else:
                    failed_count += 1
                
                # Commit every 10 updates to reduce delays
                if i % 10 == 0:
                    conn.commit()
                    logger.info(f"Committed {i} updates")
                
                # Reduce delay to 0.5 seconds
                time.sleep(0.5)
                
            except Exception as e:
                logger.warning(f"Property {property_id} coordinate update failed")
                failed_count += 1
                continue
        
        # Final commit
        conn.commit()
        
        logger.info(f"Coordinate information addition completed!")
        logger.info(f"Successfully updated: {updated_count}")
        logger.info(f"Update failed: {failed_count}")
        
    except Exception as e:
        logger.error(f"Failed to update coordinates: {e}")
        conn.rollback()
    finally:
        conn.close()

def verify_coordinates():
    """Verify coordinate update results"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Count total properties
        cursor.execute("SELECT COUNT(*) FROM properties")
        total = cursor.fetchone()[0]
        
        # Count properties with coordinates
        cursor.execute("SELECT COUNT(*) FROM properties WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
        with_coordinates = cursor.fetchone()[0]
        
        # Calculate coverage percentage
        coverage = (with_coordinates / total) * 100 if total > 0 else 0
        
        logger.info(f"Final verification results:")
        logger.info(f"Total properties: {total}")
        logger.info(f"Properties with coordinates: {with_coordinates}")
        logger.info(f"Coordinate coverage: {coverage:.1f}%")
        
        # Show some examples
        logger.info(f"Sample coordinates:")
        cursor.execute("SELECT property_id, location, latitude, longitude FROM properties WHERE latitude IS NOT NULL AND longitude IS NOT NULL LIMIT 5")
        examples = cursor.fetchall()
        
        for prop_id, location, lat, lon in examples:
            print(f"  Property {prop_id}: {location} -> ({lat}, {lon})")
        
    except Exception as e:
        logger.error(f"Failed to verify coordinates: {e}")
    finally:
        conn.close()

def main():
    """Main execution function"""
    logger.info("Starting quick completion of remaining coordinate information...")
    
    try:
        update_property_coordinates()
        verify_coordinates()
        logger.info("Coordinate information addition completed!")
        
    except Exception as e:
        logger.error(f"Script execution failed: {e}")

if __name__ == "__main__":
    main()
