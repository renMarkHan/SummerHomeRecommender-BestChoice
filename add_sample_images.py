#!/usr/bin/env python3
"""
Add sample images to properties
"""

import sqlite3
import os
import random

def add_sample_images():
    """Add sample images to properties database"""
    try:
        conn = sqlite3.connect("properties.db")
        cursor = conn.cursor()
        
        # Check if image column exists
        cursor.execute("PRAGMA table_info(properties)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if "image_url" not in columns:
            cursor.execute("ALTER TABLE properties ADD COLUMN image_url TEXT")
            print("Added image_url column")
        
        # Sample image URLs
        sample_images = [
            "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400",
            "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400",
            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=400",
            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=400",
            "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=400",
            "https://images.unsplash.com/photo-1600607687644-c7171b42498b?w=400",
            "https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=400",
            "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=400",
            "https://images.unsplash.com/photo-1600566752546-3a7d5b1f3c1d?w=400",
            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=400"
        ]
        
        # Update properties with random sample images
        cursor.execute("SELECT property_id FROM properties")
        properties = cursor.fetchall()
        
        updated_count = 0
        for (property_id,) in properties:
            # Randomly select an image
            image_url = random.choice(sample_images)
            
            cursor.execute(
                "UPDATE properties SET image_url = ? WHERE property_id = ?",
                (image_url, property_id)
            )
            updated_count += 1
        
        conn.commit()
        print(f"Updated {updated_count} properties with sample images")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_sample_images()
