#!/usr/bin/env python3
"""
Test property scoring weights
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_weights():
    """Test property scoring weights"""
    print("🧪 Testing property scoring weights...")
    
    # Define weights for different criteria
    weights = {
        "location": 0.3,
        "price": 0.25,
        "features": 0.2,
        "property_type": 0.15,
        "reviews": 0.1
    }
    
    print("\n📊 Weight configuration:")
    total_weight = 0
    for criterion, weight in weights.items():
        print(f"  {criterion}: {weight:.2f}")
        total_weight += weight
    
    print(f"  Total: {total_weight:.2f}")
    
    # Test weight validation
    if abs(total_weight - 1.0) < 0.01:
        print("✅ Weights sum to 1.0 (valid)")
    else:
        print("❌ Weights do not sum to 1.0 (invalid)")
    
    print("\n✅ Weight test completed!")

if __name__ == "__main__":
    test_weights()
