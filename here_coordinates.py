#!/usr/bin/env python3
"""
Simplified script to get precise coordinates using HERE API
HERE API provides 250,000 free requests per month
"""

import sqlite3
import requests
import time
import logging
import os
from typing import Optional, Tuple
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

# HERE API Key - Load from environment variable
HERE_API_KEY = os.getenv('HERE_API_KEY')

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_NAME)

def get_precise_coordinates(address: str) -> Optional[Tuple[float, float]]:
    """
    Get precise coordinates using HERE API
    
    Args:
        address: Complete address
        
    Returns:
        (latitude, longitude) tuple, returns None if failed
    """
    if not HERE_API_KEY:
        logger.error("HERE_API_KEY not found in environment variables. Please set it in your .env file.")
        return None
    
    try:
        base_url = "https://geocode.search.hereapi.com/v1/geocode"
        params = {
            'q': address,
            'apiKey': HERE_API_KEY,
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
        
        logger.info(f"🎯 Starting precise coordinate acquisition, total count: {total_properties}")
        logger.info("=" * 60)
        
        updated_count = 0
        failed_count = 0
        
        for i, (property_id, location) in enumerate(properties, 1):
            logger.info(f"[{i}/{total_properties}] Property {property_id}: {location}")
            
            coordinates = get_precise_coordinates(location)
            
            if coordinates:
                lat, lng = coordinates
                
                cursor.execute("""
                    UPDATE properties 
                    SET latitude = ?, longitude = ? 
                    WHERE property_id = ?
                """, (lat, lng, property_id))
                
                updated_count += 1
                logger.info(f"✅ Property {property_id} coordinates updated successfully")
                
            else:
                failed_count += 1
                logger.error(f"❌ Property {property_id} coordinate acquisition failed")
            
            # Commit to database every 10 updates
            if i % 10 == 0:
                conn.commit()
                logger.info(f"📝 Committed {i} updates to database")
            
            logger.info("-" * 40)
            
            # API rate limit delay (HERE API is relatively lenient)
            time.sleep(0.2)
        
        # Final commit
        conn.commit()
        conn.close()
        
        logger.info("=" * 60)
        logger.info(f"🎉 Precise coordinate update completed!")
        logger.info(f"✅ Successfully updated: {updated_count}")
        logger.info(f"❌ Update failed: {failed_count}")
        logger.info(f"📊 Success rate: {updated_count/total_properties*100:.1f}%")
        
    except Exception as e:
        logger.error(f"❌ Failed to update precise coordinates: {e}")
        raise

def show_sample_results():
    """Display precise coordinate examples"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT property_id, location, latitude, longitude 
            FROM properties 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL 
            ORDER BY property_id
            LIMIT 10
        """)
        examples = cursor.fetchall()
        
        conn.close()
        
        if examples:
            logger.info("🎯 Precise coordinate examples:")
            logger.info("-" * 80)
            for prop_id, location, lat, lng in examples:
                logger.info(f"Property {prop_id:3d}: {location}")
                logger.info(f"             -> ({lat:.6f}, {lng:.6f})")
                logger.info("")
        
    except Exception as e:
        logger.error(f"❌ Failed to display examples: {e}")

def main():
    """Main function"""
    print("🗺️  HERE API Precise Coordinate Acquisition Script")
    print("=" * 60)
    
    if not HERE_API_KEY:
        print("❌ Error: HERE_API_KEY not found in environment variables")
        print("")
        print("📝 Setup steps:")
        print("1. Create or edit .env file in project root")
        print("2. Add: HERE_API_KEY=your_actual_api_key_here")
        print("3. Visit https://developer.here.com/ to get API key")
        print("4. Run script again")
        return
    
    try:
        logger.info("🎯 Starting precise coordinate acquisition...")
        update_precise_coordinates()
        show_sample_results()
        logger.info("🎉 All tasks completed!")
        
    except Exception as e:
        logger.error(f"❌ Script execution failed: {e}")
        raise

if __name__ == "__main__":
    main()
