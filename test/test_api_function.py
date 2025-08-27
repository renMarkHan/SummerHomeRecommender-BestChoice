#!/usr/bin/env python3
"""
Test API functions
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_planning import extract_information_with_ai, TravelPlanningSession, classify_user_intent

async def test_api_functions():
    """Test API functions"""
    print("🧪 Testing API functions...")
    
    # Test intent classification
    print("\n📝 Testing intent classification...")
    intent1 = classify_user_intent("Toronto")
    print(f"  'Toronto' -> {intent1}")
    
    intent2 = classify_user_intent("next weekend")
    print(f"  'next weekend' -> {intent2}")
    
    intent3 = classify_user_intent("2 people")
    print(f"  '2 people' -> {intent3}")
    
    # Test information extraction
    print("\n📝 Testing information extraction...")
    session = TravelPlanningSession("test_session")
    
    print("  Testing destination step...")
    result1 = await extract_information_with_ai("Toronto", "destination", session)
    print(f"    'Toronto' -> {result1}")
    
    print("  Testing dates step...")
    result2 = await extract_information_with_ai("next weekend", "dates", session)
    print(f"    'next weekend' -> {result2}")
    
    print("  Testing group_size step...")
    result3 = await extract_information_with_ai("2 people", "group_size", session)
    print(f"    '2 people' -> {result3}")
    
    print("  Testing budget step...")
    result4 = await extract_information_with_ai("$200 per night", "budget", session)
    print(f"    '$200 per night' -> {result4}")

if __name__ == "__main__":
    asyncio.run(test_api_functions())

