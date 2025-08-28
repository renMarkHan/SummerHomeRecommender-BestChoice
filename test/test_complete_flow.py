#!/usr/bin/env python3
"""
Test complete travel planning flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_planning import TravelPlanningSession
from travel_recommendation_engine import TravelRecommendationEngine

def test_complete_flow():
    """Test the complete travel planning flow"""
    print("🧪 Testing complete travel planning flow...")
    
    # 1. Create session
    session = TravelPlanningSession("test_complete_session")
    print(f"✅ Created session: {session.session_id}")
    
    # 2. Manually set all information
    session.update_collected_info("destination", "Toronto")
    session.update_collected_info("travel_dates", "Next weekend")
    session.update_collected_info("group_size", 2)
    session.update_collected_info("budget_range", (150, 300))
    session.update_collected_info("preferred_environment", "city")
    session.update_collected_info("must_have_features", ["WiFi", "kitchen"])
    
    print(f"📋 Session info: {session.collected_info}")
    print(f"🎯 Completion: {session.get_completion_percentage():.1f}%")
    
    # 3. Check if we have sufficient information
    has_sufficient = session.has_sufficient_info()
    print(f"✅ Has sufficient info: {has_sufficient}")
    
    if has_sufficient:
        # 4. Generate recommendations
        print("\n🚀 Generating recommendations...")
        engine = TravelRecommendationEngine()
        recommendations = engine.generate_travel_recommendations(session)
        
        print("📝 Recommendations generated:")
        print("=" * 60)
        
        # Display recommendations (truncated for readability)
        lines = recommendations.split('\n')
        for i, line in enumerate(lines[:20]):  # Show first 20 lines
            print(f"{i+1:2d}: {line}")
        
        if len(lines) > 20:
            print("... (truncated for display)")
        
        print("=" * 60)
        
        # 5. Test property access
        print("\n🏠 Testing property access from recommendations...")
        filtered_properties = engine.filter_properties_for_travel_planning(session)
        
        if filtered_properties:
            print(f"📊 Found {len(filtered_properties)} matching properties")
            
            # Show sample properties
            for i, prop in enumerate(filtered_properties[:3], 1):  # Show first 3 properties
                print(f"\nProperty {i}:")
                print(f"  Title: {prop.title}")
                print(f"  Location: {prop.location}")
                print(f"  Price: ${prop.nightly_price}/night")
                print(f"  Type: {prop.property_type}")
                print(f"  Max Guests: {prop.max_guests}")
                print(f"  Features: {prop.features[:100]}...")  # Truncate long features
        
        # 6. Simulate chatbox display
        print("\n💬 Simulating chatbox display...")
        chat_response = f"Based on your preferences, I found {len(filtered_properties)} properties in Toronto. "
        chat_response += "Here are my top recommendations:\n\n"
        
        if filtered_properties:
            for i, prop in enumerate(filtered_properties[:3], 1):
                chat_response += f"{i}. **{prop.title}** - ${prop.nightly_price}/night\n"
                chat_response += f"   📍 {prop.location} | 👥 Up to {prop.max_guests} guests\n"
                chat_response += f"   🏠 {prop.property_type}\n\n"
        
        chat_response += "Would you like me to help you with anything else?"
        
        print("Chat response:")
        print("-" * 40)
        print(chat_response)
        print("-" * 40)
        
    else:
        print("❌ Not enough information to generate recommendations")
        missing_fields = []
        for field, value in session.collected_info.items():
            if value is None and field in ["destination", "travel_dates", "group_size", "budget_range"]:
                missing_fields.append(field)
        print(f"Missing fields: {missing_fields}")
    
    print("\n✅ Complete flow test finished!")

if __name__ == "__main__":
    test_complete_flow()
