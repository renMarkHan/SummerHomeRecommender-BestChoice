#!/usr/bin/env python3
"""
Test information extraction functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_planning import extract_information_from_message

def test_extraction():
    """Test information extraction"""
    print("🧪 Testing information extraction...")
    
    # Test destination extraction
    print("\n📝 Testing destination extraction...")
    result1 = extract_information_from_message("Toronto", "destination")
    print(f"  'Toronto' -> {result1}")
    
    # Test date extraction
    print("\n📝 Testing date extraction...")
    result2 = extract_information_from_message("next weekend", "dates")
    print(f"  'next weekend' -> {result2}")
    
    # Test group size extraction
    print("\n📝 Testing group size extraction...")
    result3 = extract_information_from_message("2 people", "group_size")
    print(f"  '2 people' -> {result3}")
    
    # Test budget extraction
    print("\n📝 Testing budget extraction...")
    result4 = extract_information_from_message("$200 per night", "budget")
    print(f"  '$200 per night' -> {result4}")
    
    print("\n✅ Information extraction test completed!")

if __name__ == "__main__":
    test_extraction()

