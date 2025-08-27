#!/usr/bin/env python3
"""
Test database functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_all_properties

def test_database():
    """Test database functionality"""
    print("🧪 Testing database functionality...")
    
    try:
        # Test property retrieval
        print("\n📊 Testing property retrieval...")
        properties = get_all_properties()
        
        if properties:
            print(f"✅ Successfully retrieved {len(properties)} properties")
            
            # Show sample properties
            print("\n🏠 Sample properties:")
            for i, prop in enumerate(properties[:3], 1):
                print(f"  {i}. {prop.title}")
                print(f"     Location: {prop.location}")
                print(f"     Price: ${prop.nightly_price}/night")
                print(f"     Type: {prop.property_type}")
                print()
        else:
            print("❌ No properties retrieved")
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
    
    print("\n✅ Database test completed!")

if __name__ == "__main__":
    test_database()
