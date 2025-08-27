#!/usr/bin/env python3
"""
Travel planning session management module
Manages user travel planning conversation state and information collection
"""

import os
import json
import uuid
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

class TravelPlanningSession:
    """Travel planning session management"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.current_step = "initial"
        self.conversation_count = 0
        
        # Collected user information
        self.collected_info = {
            "destination": None,           # Destination
            "travel_dates": None,          # Travel dates
            "group_size": None,            # Group size
            "budget_range": None,          # Budget range (min, max)
            "preferred_environment": None, # Environment preference
            "must_have_features": [],      # Required features
            "property_type": None,         # Property type preference
            "travel_purpose": None,        # Travel purpose
            "preferred_activities": []     # Preferred activities
        }
        
        # Conversation history
        self.conversation_history = []
        
        # Current recommendation results
        self.current_recommendations = []
        
        # Step completion status
        self.step_completion = {
            "initial": False,
            "destination": False,
            "dates": False,
            "group_size": False,
            "budget": False,
            "environment": False,
            "features": False
        }
        
        logger.info(f"Created new travel planning session: {self.session_id}")
    
    def update_collected_info(self, step: str, value: any) -> bool:
        """Update collected information and mark step as complete"""
        try:
            # Find the corresponding step name to mark completion
            step_name = self._find_step_name_by_field(step)
            if step_name:
                self.step_completion[step_name] = True
            
            if step in self.collected_info:
                self.collected_info[step] = value
                logger.info(f"Session {self.session_id} updated info: {step} = {value}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to update session info: {e}")
            return False
    
    def _find_step_name_by_field(self, field: str) -> str:
        """Find step name by field name"""
        field_to_step = {
            "destination": "destination",
            "travel_dates": "dates", 
            "group_size": "group_size",
            "budget_range": "budget",
            "preferred_environment": "environment",
            "must_have_features": "features"
        }
        return field_to_step.get(field)
    
    def reset_session(self):
        """Reset session to initial state"""
        self.current_step = "initial"
        self.conversation_count = 0
        self.collected_info = {k: None if k != "must_have_features" else [] for k in self.collected_info}
        self.conversation_history = []
        self.current_recommendations = []
        self.step_completion = {k: False for k in self.step_completion}
        logger.info(f"Session {self.session_id} has been reset")
    
    def has_sufficient_info(self) -> bool:
        """Check if we have enough information to generate recommendations"""
        required_fields = ["destination", "travel_dates", "group_size", "budget_range"]
        return all(self.collected_info[field] is not None for field in required_fields)
    
    def get_completion_percentage(self) -> float:
        """Calculate completion percentage based on collected information"""
        total_steps = len(self.step_completion)
        completed_steps = sum(self.step_completion.values())
        return (completed_steps / total_steps) * 100

# Travel planning steps definition
TRAVEL_PLANNING_STEPS = {
    "initial": {
        "question": "Where would you like to go?",
        "requirements": "City, region, or country name",
        "examples": "Toronto, Vancouver, Banff, Japan, Europe",
        "field": None  # initial step doesn't correspond to any field
    },
    "destination": {
        "question": "When do you plan to travel?",
        "requirements": "Travel dates or timeframe",
        "examples": "Next weekend, August 15-20, Christmas period",
        "field": "destination"  # destination step corresponds to destination field
    },
    "dates": {
        "question": "How many people will be traveling?",
        "requirements": "Number of travelers",
        "examples": "2 people, 4 people, family trip",
        "field": "travel_dates"  # dates step corresponds to travel_dates field
    },
    "group_size": {
        "question": "What's your budget range?",
        "requirements": "Budget per night or total",
        "examples": "$100-200 per night, $300-500, flexible budget",
        "field": "group_size"  # group_size step corresponds to group_size field
    },
    "budget": {
        "question": "What environment do you prefer?",
        "requirements": "Environment preference",
        "examples": "Beach, mountain, city, forest, suburban",
        "field": "budget_range"  # budget step corresponds to budget_range field
    },
    "environment": {
        "question": "What features are must-haves?",
        "requirements": "Essential amenities or features",
        "examples": "WiFi, kitchen, parking, pet-friendly",
        "field": "preferred_environment"  # environment step corresponds to preferred_environment field
    },
    "features": {
        "question": "Any other preferences?",
        "requirements": "Additional preferences or requirements",
        "examples": "Property type, travel purpose, activities",
        "field": "must_have_features"  # features step corresponds to must_have_features field
    }
}

def generate_next_question(session: TravelPlanningSession) -> str:
    """Generate the next question based on current step and collected information"""
    
    # Base questions
    if session.current_step == "initial":
        return "Hi! I'm happy to help you plan your trip. First, where would you like to go? It can be a city, region, or country - like Toronto, Vancouver, Banff, or anywhere else?"
    
    # Personalize questions based on collected information
    if session.current_step == "destination" and session.collected_info.get("destination"):
        return f"Great! You want to go to {session.collected_info['destination']}. When do you plan to travel?"
    
    if session.current_step == "dates" and session.collected_info.get("travel_dates"):
        return f"Perfect! You're planning to travel {session.collected_info['travel_dates']}. How many people will be traveling?"
    
    if session.current_step == "group_size" and session.collected_info.get("group_size"):
        return f"Got it! {session.collected_info['group_size']} people traveling. What's your budget range?"
    
    if session.current_step == "budget" and session.collected_info.get("budget_range"):
        return f"Budget noted: {session.collected_info['budget_range']}. What environment do you prefer?"
    
    # Add example prompts
    examples = TRAVEL_PLANNING_STEPS.get(session.current_step, {}).get("examples", "")
    if examples:
        return f"{TRAVEL_PLANNING_STEPS[session.current_step]['question']}\n\nExamples: {examples}"
    
    return TRAVEL_PLANNING_STEPS.get(session.current_step, {}).get("question", "Please provide more information.")

def extract_information_from_message(user_message: str, current_step: str) -> any:
    """Extract information from user message (rule-based version)"""
    
    # Debug output
    print(f"🔍 DEBUG: extract_information_from_message called")
    print(f"🔍 DEBUG: user_message = '{user_message}'")
    print(f"🔍 DEBUG: current_step = '{current_step}'")
    
    logger.info(f"🔍 Starting rule-based information extraction: message='{user_message}', step='{current_step}'")
    
    user_message = user_message.lower().strip()
    logger.info(f"🔍 Processed message: '{user_message}'")
    
    try:
        if current_step == "destination" or current_step == "initial":
            logger.info(f"🔍 Processing destination/initial step")
            # Extract city names
            canadian_cities = [
                "toronto", "vancouver", "montreal", "calgary", "edmonton",
                "ottawa", "winnipeg", "quebec", "banff", "whistler",
                "victoria", "halifax", "st. john's", "saskatoon", "regina"
            ]
            
            for city in canadian_cities:
                if city in user_message:
                    result = city.title()
                    logger.info(f"🔍 Found city: {city} -> {result}")
                    return result
            
            # If no predefined city found, return user input
            result = user_message.title()
            logger.info(f"🔍 No predefined city found, returning user input: {result}")
            return result
        
        elif current_step == "dates":
            logger.info(f"🔍 Processing dates step")
            # Simple date extraction (can be enhanced later)
            if any(word in user_message for word in ["next month"]):
                result = "Next month"
                logger.info(f"🔍 Found date keyword, returning: {result}")
                return result
            elif any(word in user_message for word in ["christmas"]):
                result = "Christmas period"
                logger.info(f"🔍 Found date keyword, returning: {result}")
                return result
            else:
                result = user_message
                logger.info(f"🔍 No date keyword found, returning user input: {result}")
                return result
        
        elif current_step == "group_size":
            logger.info(f"🔍 Processing group_size step")
            # Extract number of people
            import re
            numbers = re.findall(r'\d+', user_message)
            if numbers:
                result = int(numbers[0])
                logger.info(f"🔍 Found number, returning: {result}")
                return result
            elif "family" in user_message:
                result = 4
                logger.info(f"🔍 Found family keyword, returning: {result}")
                return result
            elif "couple" in user_message:
                result = 2
                logger.info(f"🔍 Found couple keyword, returning: {result}")
                return result
            else:
                result = user_message
                logger.info(f"🔍 No group size info found, returning user input: {result}")
                return result
        
        elif current_step == "budget":
            logger.info(f"🔍 Processing budget step")
            # Extract budget range
            import re
            numbers = re.findall(r'\d+', user_message)
            if len(numbers) >= 2:
                min_budget = int(numbers[0])
                max_budget = int(numbers[1])
                result = (min_budget, max_budget)
                logger.info(f"🔍 Found two numbers, returning range: {result}")
                return result
            elif len(numbers) == 1:
                budget = int(numbers[0])
                result = (budget, budget + 100)  # Default range
                logger.info(f"🔍 Found one number, returning range: {result}")
                return result
            else:
                result = user_message
                logger.info(f"🔍 No numbers found, returning user input: {result}")
                return result
        
        elif current_step == "environment":
            logger.info(f"🔍 Processing environment step")
            # Environment preferences
            environments = ["beach", "mountain", "city", "forest", "suburban"]
            for env in environments:
                if env in user_message:
                    logger.info(f"🔍 Found environment keyword: {env}")
                    return env
            result = user_message
            logger.info(f"🔍 No environment keyword found, returning user input: {result}")
            return result
        
        elif current_step == "features":
            logger.info(f"🔍 Processing features step")
            # Feature extraction
            features = ["wifi", "kitchen", "pool", "gym", "pet-friendly", "parking", "balcony"]
            extracted_features = []
            for feature in features:
                if feature in user_message:
                    extracted_features.append(feature)
            result = extracted_features if extracted_features else user_message
            logger.info(f"🔍 Extracted features: {result}")
            return result
        
        else:
            logger.info(f"🔍 Unknown step, returning user input: {user_message}")
            return user_message
            
    except Exception as e:
        logger.error(f"❌ Information extraction failed: {e}")
        logger.error(f"❌ Error details: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(f"❌ Stack trace: {traceback.format_exc()}")
        return user_message

def classify_user_intent(user_message: str) -> str:
    """Classify user intent from message"""
    user_message = user_message.lower().strip()
    
    # Check for travel planning intent
    travel_keywords = ["plan", "trip", "travel", "vacation", "holiday", "journey", "visit"]
    if any(keyword in user_message for keyword in travel_keywords):
        return "travel_planning"
    
    # Check for information provision
    info_keywords = ["toronto", "vancouver", "montreal", "calgary", "edmonton", "ottawa", "winnipeg", "quebec", "banff", "whistler", "victoria", "halifax", "st. john's", "saskatoon", "regina", "next", "weekend", "month", "christmas", "people", "family", "couple", "budget", "price", "cost", "beach", "mountain", "city", "forest", "suburban", "wifi", "kitchen", "parking", "pet", "pool", "gym"]
    if any(keyword in user_message for keyword in info_keywords):
        return "provide_information"
    
    # Check for recommendation request
    rec_keywords = ["recommend", "suggestion", "find", "search", "show", "list", "what", "where", "how"]
    if any(keyword in user_message for keyword in rec_keywords):
        return "request_recommendation"
    
    # Default to general chat
    return "general_chat"

async def generate_next_question_with_ai(session: TravelPlanningSession) -> str:
    """Generate next question using AI"""
    
    if not OPENROUTER_API_KEY:
        logger.warning("OpenRouter API key not configured, falling back to template-based question generation")
        return generate_next_question(session)
    
    try:
        # Build conversation history
        history_str = ""
        if session.conversation_history:
            history_str = " | ".join([f"User: {msg['user']}, Assistant: {msg['assistant']}" for msg in session.conversation_history[-3:]])
        
        system_prompt = f"""You are a helpful travel planning assistant. Generate a natural, friendly question for the next step.
        
        Current step: {session.current_step}
        Collected information: {session.collected_info}
        Previous conversation: {history_str}
        
        Generate a question that:
        1. Is natural and conversational
        2. References previously collected information when relevant
        3. Provides helpful examples
        4. Moves the conversation forward
        
        Return only the question, no explanations."""
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate the next question"}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_question = result['choices'][0]['message']['content'].strip()
        
        logger.info(f"AI generated question: {ai_question}")
        return ai_question
        
    except Exception as e:
        logger.error(f"AI question generation failed: {e}")
        return generate_next_question(session)

async def extract_information_with_ai(user_message: str, current_step: str, session: TravelPlanningSession) -> any:
    """Extract information using AI from natural language"""
    
    logger.info(f"🤖 Starting AI information extraction: message='{user_message}', step='{current_step}'")
    
    if not OPENROUTER_API_KEY:
        logger.warning("⚠️ OpenRouter API key not configured, falling back to rule-based extraction")
        logger.info(f"🔄 Calling rule-based extraction function...")
        result = extract_information_from_message(user_message, current_step)
        logger.info(f"✅ Rule-based extraction result: {result}")
        return result
    
    step_info = TRAVEL_PLANNING_STEPS.get(current_step, {})
    field_name = step_info.get('field', current_step)
    
    system_prompt = f"""You are a professional information extraction assistant. You need to extract specific information from user's natural language responses.

Current step: {current_step}
Field to extract: {field_name}
User response: "{user_message}"

Based on field type, please extract and return appropriate format:

- destination: Extract city or region name, return string
- travel_dates: Extract date information, return descriptive string
- group_size: Extract number of people, return descriptive string (e.g., "2 people", "4 people")
- budget_range: Extract budget number, return number (take median or minimum)
- preferred_environment: Extract environment preference, return string
- must_have_features: Extract feature list, return string list

Please return only the extracted value, no explanations. If unable to extract, return null.

Examples:
- User says "I want to go to Toronto" → Extract destination: "Toronto"
- User says "this weekend" → Extract travel_dates: "This Weekend"  
- User says "we are two people" → Extract group_size: "2 people"
- User says "$200-300 per night" → Extract budget_range: 250
- User says "I like beach" → Extract preferred_environment: "beach"
- User says "need WiFi and kitchen" → Extract must_have_features: ["WiFi", "kitchen"]"""

    user_prompt = f"Please extract {field_name} information from this response: \"{user_message}\""
    
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 100,
            "temperature": 0.1
        }
        
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_extracted = result['choices'][0]['message']['content'].strip()
        
        # Try to parse AI returned results
        try:
            if ai_extracted.lower() in ['null', 'none', '']:
                return None
            
            # Try to parse as JSON (for list types)
            if ai_extracted.startswith('[') and ai_extracted.endswith(']'):
                return json.loads(ai_extracted)
            
            # Try to parse as number (for budget)
            if field_name == 'budget_range':
                import re
                numbers = re.findall(r'\d+', ai_extracted)
                if numbers:
                    return int(numbers[0])
            
            # Return string
            return ai_extracted.strip('"\'')
            
        except:
            logger.warning(f"AI extraction result parsing failed: {ai_extracted}")
            return ai_extracted
        
        logger.info(f"AI information extraction successful: {field_name} = {ai_extracted}")
        return ai_extracted
        
    except Exception as e:
        logger.error(f"AI information extraction failed: {e}")
        return extract_information_from_message(user_message, current_step)
