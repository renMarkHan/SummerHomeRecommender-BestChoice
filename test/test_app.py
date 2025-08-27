#!/usr/bin/env python3
"""
Test application functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_app():
    """Test application functionality"""
    print("🧪 Testing application functionality...")
    
    # Test imports
    print("\n📦 Testing imports...")
    
    try:
        from travel_planning import TravelPlanningSession
        print("✅ TravelPlanningSession imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import TravelPlanningSession: {e}")
    
    try:
        from travel_recommendation_engine import TravelRecommendationEngine
        print("✅ TravelRecommendationEngine imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import TravelRecommendationEngine: {e}")
    
    try:
        from database import get_all_properties
        print("✅ Database functions imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import database functions: {e}")
    
    print("\n✅ Application test completed!")

if __name__ == "__main__":
    test_app()
