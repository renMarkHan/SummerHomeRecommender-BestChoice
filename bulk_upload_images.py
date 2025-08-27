#!/usr/bin/env python3
"""
Bulk Image Upload Script for Vacation Rentals
This script helps you upload multiple images and assign them to properties
"""

import os
import sqlite3
import shutil
from pathlib import Path
import random

def setup_database_connection():
    """Setup database connection"""
    return sqlite3.connect('vacation_rentals.db')

def get_properties_without_images():
    """Get properties that don't have local images"""
    conn = setup_database_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT property_id, location, type 
        FROM properties 
        WHERE image_url IS NULL OR image_url LIKE '%unsplash.com%'
        ORDER BY property_id
    """)
    
    properties = cursor.fetchall()
    conn.close()
    return properties

def get_properties_with_local_images():
    """Get properties that have local images"""
    conn = setup_database_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT property_id, location, type, image_url
        FROM properties 
        WHERE image_url IS NOT NULL AND image_url LIKE '/static/images/properties%'
        ORDER BY property_id
    """)
    
    properties = cursor.fetchall()
    conn.close()
    return properties

def upload_image_to_property(image_path, property_id, property_info):
    """Upload a single image to a property"""
    try:
        # Validate image file
        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return False
        
        # Check file size (5MB limit)
        file_size = os.path.getsize(image_path)
        if file_size > 5 * 1024 * 1024:
            print(f"❌ Image too large ({file_size / 1024 / 1024:.2f}MB): {image_path}")
            return False
        
        # Create images directory
        images_dir = Path("static/images/properties")
        images_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        file_extension = Path(image_path).suffix
        filename = f"property_{property_id}_{int(os.urandom(4).hex(), 16)}{file_extension}"
        destination_path = images_dir / filename
        
        # Copy image file
        shutil.copy2(image_path, destination_path)
        
        # Update database
        conn = setup_database_connection()
        cursor = conn.cursor()
        
        image_url = f"/static/images/properties/{filename}"
        image_alt = f"{property_info[1]} - {property_info[2]}"
        
        cursor.execute("""
            UPDATE properties 
            SET image_url = ?, image_alt = ?
            WHERE property_id = ?
        """, (image_url, image_alt, property_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Uploaded: {os.path.basename(image_path)} → Property #{property_id} ({property_info[1]})")
        return True
        
    except Exception as e:
        print(f"❌ Failed to upload {image_path} to property {property_id}: {e}")
        return False

def bulk_upload_from_directory(image_directory):
    """Bulk upload images from a directory"""
    print(f"\n🖼️  Starting bulk upload from: {image_directory}")
    
    # Get properties without images
    properties_needing_images = get_properties_without_images()
    
    if not properties_needing_images:
        print("🎉 All properties already have local images!")
        return
    
    print(f"📊 Found {len(properties_needing_images)} properties needing images")
    
    # Get image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    image_files = []
    
    for file_path in Path(image_directory).rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    if not image_files:
        print("❌ No image files found in the directory")
        return
    
    print(f"🖼️  Found {len(image_files)} image files")
    
    # Match images to properties
    if len(image_files) >= len(properties_needing_images):
        # We have enough images for all properties
        print("🎯 Assigning images to properties...")
        
        # Randomly shuffle properties for variety
        random.shuffle(properties_needing_images)
        
        success_count = 0
        for i, (property_id, location, prop_type) in enumerate(properties_needing_images):
            if i < len(image_files):
                if upload_image_to_property(str(image_files[i]), property_id, (property_id, location, prop_type)):
                    success_count += 1
        
        print(f"\n🎉 Successfully uploaded {success_count} images!")
        
    else:
        # Not enough images for all properties
        print(f"⚠️  Warning: Only {len(image_files)} images for {len(properties_needing_images)} properties")
        print("Some properties will remain without images")
        
        success_count = 0
        for i, image_path in enumerate(image_files):
            if i < len(properties_needing_images):
                property_id, location, prop_type = properties_needing_images[i]
                if upload_image_to_property(str(image_path), property_id, (property_id, location, prop_type)):
                    success_count += 1
        
        print(f"\n🎉 Successfully uploaded {success_count} images!")

def show_image_status():
    """Show current image status"""
    print("\n📊 Current Image Status:")
    print("=" * 50)
    
    # Properties without images
    properties_without = get_properties_without_images()
    print(f"Properties without images: {len(properties_without)}")
    
    # Properties with local images
    properties_with_local = get_properties_with_local_images()
    print(f"Properties with local images: {len(properties_with_local)}")
    
    # Total properties
    conn = setup_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM properties")
    total_properties = cursor.fetchone()[0]
    conn.close()
    
    print(f"Total properties: {total_properties}")
    print(f"Coverage: {len(properties_with_local)}/{total_properties} ({len(properties_with_local)/total_properties*100:.1f}%)")
    
    if properties_without:
        print(f"\nProperties needing images:")
        for prop_id, location, prop_type in properties_without[:10]:  # Show first 10
            print(f"  #{prop_id}: {location} ({prop_type})")
        if len(properties_without) > 10:
            print(f"  ... and {len(properties_without) - 10} more")

def main():
    """Main function"""
    print("🏝 Vacation Rentals - Bulk Image Upload Tool")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Show current image status")
        print("2. Upload images from directory")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            show_image_status()
            
        elif choice == "2":
            image_dir = input("Enter the path to your images directory: ").strip()
            
            if not os.path.exists(image_dir):
                print("❌ Directory not found!")
                continue
            
            if not os.path.isdir(image_dir):
                print("❌ Path is not a directory!")
                continue
            
            bulk_upload_from_directory(image_dir)
            
        elif choice == "3":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
