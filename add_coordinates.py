#!/usr/bin/env python3
"""
Add coordinates to properties database
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

def add_coordinate_columns():
    """Add latitude and longitude columns to properties table"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(properties)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if "latitude" not in columns:
            logger.info("Adding latitude column...")
            cursor.execute("ALTER TABLE properties ADD COLUMN latitude REAL")
            logger.info("Latitude column added successfully")
        else:
            logger.info("Latitude column already exists")
        
        if "longitude" not in columns:
            logger.info("Adding longitude column...")
            cursor.execute("ALTER TABLE properties ADD COLUMN longitude REAL")
            logger.info("Longitude column added successfully")
        else:
            logger.info("Longitude column already exists")
        
        conn.commit()
        logger.info("Coordinate columns added successfully")
        
    except Exception as e:
        logger.error(f"Failed to add coordinate columns: {e}")
        conn.rollback()
    finally:
        conn.close()

def extract_city_from_address(address: str) -> str:
    """Extract city name from address string"""
    if not address:
        return ""
    
    # Split address, city is usually in the second to last position
    parts = address.split(',')
    if len(parts) >= 2:
        # Take the second to last part, usually the city name
        city = parts[-2].strip()
        
        # If city name contains state/province abbreviation, remove it
        if len(city) <= 3 and city.isupper():
            city = parts[-3].strip() if len(parts) >= 3 else city
        
        return city
    
    return address.strip()

def get_coordinates_from_nominatim(location: str) -> tuple:
    """Get coordinates from Nominatim API"""
    try:
        # Extract city name
        city = extract_city_from_address(location)
        logger.info(f"Extracted city '{city}' from address '{location}'")
        
        if not city:
            return None, None
        
        # Build query URL, add country name for better accuracy
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': f"{city}, Canada",  # Add country name for better accuracy
            'format': 'json',
            'limit': 1
        }
        
        # Send request (add User-Agent header, Nominatim requires it)
        headers = {
            'User-Agent': 'CozyDoDo/1.0 (https://cozydodo.com; contact@cozydodo.com)'
        }
        
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            logger.info(f"Got coordinates: {city}, Canada -> ({lat}, {lon})")
            return lat, lon
        else:
            logger.warning(f"No coordinates found: {city}, Canada")
            return None, None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed {location}: {e}")
        return None, None
    except (KeyError, ValueError, IndexError) as e:
        logger.error(f"Failed to parse coordinates {location}: {e}")
        return None, None
    except Exception as e:
        logger.error(f"Unknown error getting coordinates {location}: {e}")
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
        logger.info(f"Need to update coordinates for {total_properties} properties")
        
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
                
                # Commit each update
                conn.commit()
                
                # Add delay to avoid API limits (Nominatim limits 1 request per second)
                time.sleep(1.1)
                
            except Exception as e:
                logger.warning(f"Property {property_id} coordinate update failed")
                failed_count += 1
                continue
        
        logger.info(f"Coordinate update completed!")
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
        
        logger.info(f"Coordinate verification results:")
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
    logger.info("Starting coordinate information addition script...")
    
    try:
        # Step 1: Add coordinate columns
        logger.info("Step 1: Adding coordinate columns")
        add_coordinate_columns()
        
        # Step 2: Update coordinate information
        logger.info("Step 2: Updating coordinate information")
        update_property_coordinates()
        
        # Step 3: Verify coordinate update results
        logger.info("Step 3: Verifying coordinate update results")
        verify_coordinates()
        
        logger.info("Coordinate information addition script execution completed!")
        
    except Exception as e:
        logger.error(f"Script execution failed: {e}")

if __name__ == "__main__":
    main()
