#!/usr/bin/env python3
"""
Test message extraction functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_planning import extract_information_from_message

def test_message_extraction():
    """Test message extraction"""
    print("🧪 Testing message extraction...")
    
    # Test cases
    test_cases = [
        ("Toronto", "destination"),
        ("next weekend", "dates"),
        ("2 people", "group_size"),
        ("$200 per night", "budget")
    ]
    
    print("\n📝 Test cases:")
    for i, (user_input, step) in enumerate(test_cases, 1):
        print(f"  {i}. Input: '{user_input}', Step: {step}")
    
    # Test extraction
    print("\n🔍 Testing extraction...")
    for user_input, step in test_cases:
        result = extract_information_from_message(user_input, step)
        print(f"  '{user_input}' -> {step}: {result}")
    
    print("\n✅ Message extraction test completed!")

if __name__ == "__main__":
    test_message_extraction()

