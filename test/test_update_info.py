#!/usr/bin/env python3
"""
Test session information update functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_planning import TravelPlanningSession

def test_update_info():
    """Test session information updates"""
    print("🧪 Testing session information updates...")
    
    # Create test session
    session = TravelPlanningSession("test_session")
    print(f"✅ Created session: {session.session_id}")
    print(f"📋 Initial info: {session.collected_info}")
    
    # Test updating destination
    print("\n📝 Testing destination update...")
    success1 = session.update_collected_info("destination", "Toronto")
    print(f"  Update success: {success1}")
    print(f"  Destination: {session.collected_info['destination']}")
    
    # Test updating travel dates
    print("\n📝 Testing travel dates update...")
    success2 = session.update_collected_info("travel_dates", "Next weekend")
    print(f"  Update success: {success2}")
    print(f"  Travel dates: {session.collected_info['travel_dates']}")
    
    # Test updating group size
    print("\n📝 Testing group size update...")
    success3 = session.update_collected_info("group_size", 2)
    print(f"  Update success: {success3}")
    print(f"  Group size: {session.collected_info['group_size']}")
    
    # Test updating budget range
    print("\n📝 Testing budget range update...")
    success4 = session.update_collected_info("budget_range", (150, 300))
    print(f"  Update success: {success4}")
    print(f"  Budget range: {session.collected_info['budget_range']}")
    
    print(f"\n📊 Final session info: {session.collected_info}")
    print(f"🎯 Completion percentage: {session.get_completion_percentage():.1f}%")
    print(f"✅ Has sufficient info: {session.has_sufficient_info()}")
    
    print("\n✅ Session update test completed!")

if __name__ == "__main__":
    test_update_info()

