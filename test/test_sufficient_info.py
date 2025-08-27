#!/usr/bin/env python3
"""
Test sufficient information checking functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_planning import TravelPlanningSession

def test_sufficient_info():
    """Test sufficient information checking"""
    print("🧪 Testing sufficient information checking...")
    
    # Create test session
    session = TravelPlanningSession("test_session")
    print(f"✅ Created session: {session.session_id}")
    
    # Check initial state
    print(f"\n📋 Initial state:")
    print(f"  Collected info: {session.collected_info}")
    print(f"  Has sufficient info: {session.has_sufficient_info()}")
    print(f"  Completion: {session.get_completion_percentage():.1f}%")
    
    # Simulate updating information
    print(f"\n📝 Simulating information updates...")
    
    # Update destination
    session.update_collected_info("destination", "Toronto")
    print(f"  ✅ Updated destination: {session.collected_info['destination']}")
    print(f"  Has sufficient info: {session.has_sufficient_info()}")
    
    # Update travel dates
    session.update_collected_info("travel_dates", "Next weekend")
    print(f"  ✅ Updated travel dates: {session.collected_info['travel_dates']}")
    print(f"  Has sufficient info: {session.has_sufficient_info()}")
    
    # Update group size
    session.update_collected_info("group_size", 2)
    print(f"  ✅ Updated group size: {session.collected_info['group_size']}")
    print(f"  Has sufficient info: {session.has_sufficient_info()}")
    
    # Update budget range
    session.update_collected_info("budget_range", (150, 300))
    print(f"  ✅ Updated budget range: {session.collected_info['budget_range']}")
    print(f"  Has sufficient info: {session.has_sufficient_info()}")
    
    # Final state
    print(f"\n📊 Final state:")
    print(f"  Collected info: {session.collected_info}")
    print(f"  Has sufficient info: {session.has_sufficient_info()}")
    print(f"  Completion: {session.get_completion_percentage():.1f}%")
    
    print("\n✅ Sufficient information test completed!")

if __name__ == "__main__":
    test_sufficient_info()

