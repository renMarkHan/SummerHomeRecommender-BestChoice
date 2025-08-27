#!/usr/bin/env python3
"""
Test logging functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_logging():
    """Test logging functionality"""
    print("🧪 Testing logging...")
    
    logger.info("✅ This is an info log")
    logger.warning("⚠️ This is a warning log")
    logger.error("❌ This is an error log")
    
    print("✅ Logging test completed")

if __name__ == "__main__":
    test_logging()

