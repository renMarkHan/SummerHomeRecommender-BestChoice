#!/usr/bin/env python3
"""
Test property generation functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_property_generation():
    """Test property generation functionality"""
    print("🧪 Testing property generation...")
    
    # Test property data structure
    print("\n📊 Testing property data structure...")
    
    sample_property = {
        "location": "Toronto, ON",
        "type": "Condo",
        "nightly_price": 150,
        "features": ["WiFi", "Kitchen", "Parking"],
        "tags": ["Downtown", "Modern", "Convenient"]
    }
    
    print("Sample property structure:")
    for key, value in sample_property.items():
        print(f"  {key}: {value}")
    
    # Test JSON generation
    print("\n📝 Testing JSON generation...")
    import json
    
    try:
        json_string = json.dumps(sample_property, indent=2)
        print("Generated JSON:")
        print(json_string)
        print("✅ JSON generation successful")
    except Exception as e:
        print(f"❌ JSON generation failed: {e}")
    
    # Test multiple properties
    print("\n🏠 Testing multiple properties...")
    
    properties = [
        {
            "location": "Vancouver, BC",
            "type": "House",
            "nightly_price": 250,
            "features": ["WiFi", "Kitchen", "Garden"],
            "tags": ["Suburban", "Family-friendly", "Quiet"]
        },
        {
            "location": "Montreal, QC",
            "type": "Apartment",
            "nightly_price": 120,
            "features": ["WiFi", "Balcony", "Gym"],
            "tags": ["Urban", "Historic", "Vibrant"]
        }
    ]
    
    try:
        json_array = json.dumps(properties, indent=2)
        print("Generated properties array:")
        print(json_array)
        print("✅ Multiple properties generation successful")
    except Exception as e:
        print(f"❌ Multiple properties generation failed: {e}")
    
    print("\n✅ Property generation test completed!")

if __name__ == "__main__":
    test_property_generation()
