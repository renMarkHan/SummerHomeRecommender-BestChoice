#!/usr/bin/env python3
"""
Script to get precise coordinates using HERE Geocoding API
Requires HERE API Key
"""

import sqlite3
import requests
import time
import logging
from typing import Optional, Tuple
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration
DB_NAME = "vacation_rentals.db"

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_NAME)

def get_precise_coordinates_here(address: str) -> Optional[Tuple[float, float]]:
    """
    Get precise coordinates using HERE Geocoding API (Free tier: 250,000 requests/month)
    
    Args:
        address: Complete address
        
    Returns:
        (latitude, longitude) tuple, returns None if failed
    """
    here_api_key = os.getenv('HERE_API_KEY')  # Need to set in .env file
    
    if not here_api_key:
        logger.error("HERE API Key not set")
        return None
    
    try:
        base_url = "https://geocode.search.hereapi.com/v1/geocode"
        params = {
            'q': address,
            'apiKey': here_api_key,
            'in': 'countryCode:CAN',  # Restrict to Canada
            'limit': 1
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['items']:
            position = data['items'][0]['position']
            lat = float(position['lat'])
            lng = float(position['lng'])
            
            # Get formatted address
            title = data['items'][0]['title']
            address_parts = data['items'][0]['address']
            
            logger.info(f"Precise coordinates: {address}")
            logger.info(f"  -> Identified as: {title}")
            logger.info(f"  -> Coordinates: ({lat:.6f}, {lng:.6f})")
            
            return lat, lng
        else:
            logger.warning(f"HERE API did not find coordinates: {address}")
            return None
            
    except Exception as e:
        logger.error(f"HERE API request failed {address}: {e}")
        return None

def update_precise_coordinates():
    """Update precise coordinates for all properties"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all properties
        cursor.execute("SELECT property_id, location FROM properties ORDER BY property_id")
        properties = cursor.fetchall()
        total_properties = len(properties)
        
        logger.info(f"Starting to get precise coordinates, total count: {total_properties}")
        
        updated_count = 0
        failed_count = 0
        
        for i, (property_id, location) in enumerate(properties, 1):
            logger.info(f"Processing progress: {i}/{total_properties} - Property {property_id}: {location}")
            
            # Use HERE API to get coordinates
            coordinates = get_precise_coordinates_here(location)
            
            if coordinates:
                lat, lng = coordinates
                
                cursor.execute("""
                    UPDATE properties 
                    SET latitude = ?, longitude = ? 
                    WHERE property_id = ?
                """, (lat, lng, property_id))
                
                updated_count += 1
                logger.info(f"Property {property_id} precise coordinates updated successfully")
                
            else:
                failed_count += 1
                logger.warning(f"Property {property_id} precise coordinates acquisition failed")
            
            # Commit every 10 updates
            if i % 10 == 0:
                conn.commit()
                logger.info(f"Committed {i} updates")
            
            # API rate limit delay
            time.sleep(0.1)  # HERE API is relatively lenient
        
        # Final commit
        conn.commit()
        conn.close()
        
        logger.info(f"Precise coordinate update completed!")
        logger.info(f"Successfully updated: {updated_count}")
        logger.info(f"Update failed: {failed_count}")
        
    except Exception as e:
        logger.error(f"Failed to update precise coordinates: {e}")
        raise

def verify_precise_coordinates():
    """Verify precise coordinate results"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM properties WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
        with_coordinates = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM properties")
        total = cursor.fetchone()[0]
        
        # Show some precise coordinate examples
        cursor.execute("""
            SELECT property_id, location, latitude, longitude 
            FROM properties 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL 
            ORDER BY property_id
            LIMIT 10
        """)
        examples = cursor.fetchall()
        
        conn.close()
        
        logger.info(f"Precise coordinate verification results:")
        logger.info(f"Total properties count: {total}")
        logger.info(f"Properties with coordinates count: {with_coordinates}")
        logger.info(f"Coordinate coverage rate: {with_coordinates/total*100:.1f}%")
        
        if examples:
            logger.info("Precise coordinate examples:")
            for prop_id, location, lat, lng in examples:
                logger.info(f"  Property {prop_id}: {location} -> ({lat:.6f}, {lng:.6f})")
        
    except Exception as e:
        logger.error(f"Failed to verify precise coordinates: {e}")

def main():
    """Main function"""
    logger.info("Starting to get precise coordinate information...")
    
    # Check API configuration
    if not os.getenv('HERE_API_KEY'):
        logger.error("Please configure HERE API Key:")
        logger.error("- HERE_API_KEY (HERE Maps)")
        logger.error("Set this environment variable in your .env file")
        return
    
    try:
        update_precise_coordinates()
        verify_precise_coordinates()
        logger.info("Precise coordinate acquisition completed!")
        
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        raise

if __name__ == "__main__":
    main()
