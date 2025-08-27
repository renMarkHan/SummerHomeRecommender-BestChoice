#!/usr/bin/env python3
"""
Test travel recommendation engine functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from travel_recommendation_engine import TravelRecommendationEngine
from travel_planning import TravelPlanningSession

def test_recommendation_engine():
    """Test the recommendation engine"""
    print("🧪 Testing travel recommendation engine...")
    
    # Create test data
    session = TravelPlanningSession("test_session")
    session.update_collected_info("destination", "Toronto")
    session.update_collected_info("travel_dates", "Next weekend")
    session.update_collected_info("group_size", 2)
    session.update_collected_info("budget_range", (150, 300))
    session.update_collected_info("preferred_environment", "city")
    session.update_collected_info("must_have_features", ["WiFi", "kitchen"])
    
    # Mark steps as completed
    session.step_completion["initial"] = True
    session.step_completion["destination"] = True
    session.step_completion["dates"] = True
    session.step_completion["group_size"] = True
    session.step_completion["budget"] = True
    session.step_completion["environment"] = True
    session.step_completion["features"] = True
    
    print(f"✅ Test session created with completion: {session.get_completion_percentage():.1f}%")
    print(f"📋 Session info: {session.collected_info}")
    
    # Create recommendation engine
    engine = TravelRecommendationEngine()
    
    # Test filtering functionality
    print("\n🔍 Testing filtering functionality...")
    filtered_properties = engine.filter_properties_for_travel_planning(session)
    print(f"✅ Found {len(filtered_properties)} properties after filtering")
    
    if filtered_properties:
        print("📊 Sample filtered properties:")
        for i, prop in enumerate(filtered_properties[:3], 1):
            print(f"  {i}. {prop.title} - ${prop.nightly_price}/night in {prop.location}")
    
    # Test scoring functionality
    print("\n🎯 Testing scoring functionality...")
    if filtered_properties:
        scored_properties = engine.score_properties_by_preferences(filtered_properties, session)
        print(f"✅ Scored {len(scored_properties)} properties")
        
        print("🏆 Top scored properties:")
        for i, (prop, score) in enumerate(scored_properties[:3], 1):
            print(f"  {i}. {prop.title} - Score: {score:.1f}")
    
    # Test recommendation generation
    print("\n🚀 Testing recommendation generation...")
    recommendations = engine.generate_travel_recommendations(session)
    
    print("📝 Generated recommendations:")
    print("=" * 50)
    
    # Display only first 10 lines to avoid overwhelming output
    lines = recommendations.split('\n')[:10]  # Only show first 10 lines
    for line in lines:
        print(line)
    
    if len(recommendations.split('\n')) > 10:
        print("... (truncated for display)")
    
    print("=" * 50)
    
    # Test individual property access
    if filtered_properties:
        print("\n🏠 Testing individual property access:")
        for i, prop in enumerate(filtered_properties[:3], 1):  # Show first 3 properties
            print(f"\nProperty {i}:")
            print(f"  Title: {prop.title}")
            print(f"  Location: {prop.location}")
            print(f"  Price: ${prop.nightly_price}/night")
            print(f"  Type: {prop.property_type}")
            print(f"  Max Guests: {prop.max_guests}")
            print(f"  Features: {prop.features[:100]}...")  # Truncate long features
    
    print("\n✅ Recommendation engine test completed!")

if __name__ == "__main__":
    test_recommendation_engine()
