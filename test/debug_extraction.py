#!/usr/bin/env python3
"""
Debug information extraction functionality
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_planning import extract_information_with_ai, TravelPlanningSession

async def debug_extraction():
    """Debug the information extraction process"""
    print("🔍 Debugging information extraction...")
    
    # Test case 1: destination step, input "Toronto"
    print("\n📝 Test case 1: destination step, input 'Toronto'")
    session1 = TravelPlanningSession("test_session_1")
    result1 = await extract_information_with_ai("Toronto", "destination", session1)
    print(f"Result: {result1}")
    
    # Test case 2: initial step, input "Toronto"
    print("\n📝 Test case 2: initial step, input 'Toronto'")
    session2 = TravelPlanningSession("test_session_2")
    result2 = await extract_information_with_ai("Toronto", "initial", session2)
    print(f"Result: {result2}")
    
    # Test case 3: dates step, input "next weekend"
    print("\n📝 Test case 3: dates step, input 'next weekend'")
    session3 = TravelPlanningSession("test_session_3")
    result3 = await extract_information_with_ai("next weekend", "dates", session3)
    print(f"Result: {result3}")
    
    # Test case 4: group_size step, input "2 people"
    print("\n📝 Test case 4: group_size step, input '2 people'")
    session4 = TravelPlanningSession("test_session_4")
    result4 = await extract_information_with_ai("2 people", "group_size", session4)
    print(f"Result: {result4}")
    
    # Test case 5: budget step, input "$200 per night"
    print("\n📝 Test case 5: budget step, input '$200 per night'")
    session5 = TravelPlanningSession("test_session_5")
    result5 = await extract_information_with_ai("$200 per night", "budget", session5)
    print(f"Result: {result5}")
    
    print("\n✅ Debug extraction completed!")

if __name__ == "__main__":
    asyncio.run(debug_extraction())

