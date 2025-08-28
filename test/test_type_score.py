#!/usr/bin/env python3
"""
Test property type scoring functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_type_score():
    """Test property type scoring"""
    print("🧪 Testing property type scoring...")
    
    # Test cases
    test_cases = [
        ("House", ["House"], 1.0),  # Exact match
        ("house", ["House"], 1.0),  # Case insensitive
        ("House", ["House", "Villa"], 1.0),  # Multiple types, exact match
        ("House", ["Condo", "Apartment"], 0.0),  # No match
        ("House", [], 0.0),  # Empty list
        ("house", ["House"], 0.0),  # Case sensitive mismatch
    ]
    
    print("\n📝 Test cases:")
    for i, (property_type, available_types, expected) in enumerate(test_cases, 1):
        print(f"  {i}. Property: '{property_type}', Available: {available_types}, Expected: {expected}")
    
    # Test actual data
    print("\n🔍 Testing with actual data...")
    
    # Simulate frontend data
    user_preference = "House"
    
    # Simulate property types from database
    available_property_types = ["House", "Condo", "Apartment", "Villa", "Cabin"]
    
    # Calculate score
    if user_preference in available_property_types:
        score = 1.0
    else:
        score = 0.0
    
    print(f"User preference: {user_preference}")
    print(f"Available types: {available_property_types}")
    print(f"Score: {score}")
    
    print("\n✅ Property type scoring test completed!")

if __name__ == "__main__":
    test_type_score()
