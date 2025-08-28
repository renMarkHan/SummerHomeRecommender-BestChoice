#!/usr/bin/env python3
"""
Test async information extraction functionality
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_planning import extract_information_with_ai, TravelPlanningSession

async def test_async_extraction():
    """Test async information extraction"""
    print("🧪 Testing async information extraction...")
    
    # Create test session
    session = TravelPlanningSession("test_session")
    print(f"✅ Created session: {session.session_id}")
    
    # Test async extraction
    print("\n📝 Testing async extraction...")
    
    test_cases = [
        ("Toronto", "destination"),
        ("next weekend", "dates"),
        ("2 people", "group_size"),
        ("$200 per night", "budget")
    ]
    
    for user_input, step in test_cases:
        print(f"  Testing: '{user_input}' -> {step}")
        result = await extract_information_with_ai(user_input, step, session)
        print(f"    Result: {result}")
    
    print("\n✅ Async extraction test completed!")

if __name__ == "__main__":
    asyncio.run(test_async_extraction())

