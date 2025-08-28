#!/usr/bin/env python3
"""
Travel recommendation engine
Filters and scores properties based on user preferences
"""

import logging
from typing import List, Dict, Any, Tuple
from property import Property

logger = logging.getLogger(__name__)

class TravelRecommendationEngine:
    """Travel recommendation engine for filtering and scoring properties"""
    
    def __init__(self):
        """Initialize the recommendation engine"""
        self.properties = []
        self.load_properties()
    
    def load_properties(self):
        """Load properties from database"""
        try:
            from database import get_all_properties
            self.properties = get_all_properties()
            logger.info(f"Loaded {len(self.properties)} properties")
        except Exception as e:
            logger.error(f"Failed to load property data: {e}")
            self.properties = []
    
    def filter_properties_for_travel_planning(self, session) -> List[Property]:
        """Filter properties based on travel planning session data"""
        if not self.properties:
            logger.warning("No property data available")
            return []
        
        filtered_properties = self.properties.copy()
        
        # Filter by destination (location)
        if session.collected_info.get("destination"):
            destination = session.collected_info["destination"].lower()
            filtered_properties = [p for p in filtered_properties 
                                 if destination in p.location.lower()]
            logger.info(f"Destination filtered, remaining {len(filtered_properties)} properties")
        
        # Filter by budget
        if session.collected_info.get("budget_range"):
            budget_range = session.collected_info["budget_range"]
            if isinstance(budget_range, tuple):
                min_budget, max_budget = budget_range
            else:
                min_budget = max_budget = budget_range
            
            filtered_properties = [p for p in filtered_properties 
                                 if min_budget <= p.nightly_price <= max_budget]
            logger.info(f"Budget filtered, remaining {len(filtered_properties)} properties")
        
        # Filter by group size
        if session.collected_info.get("group_size"):
            group_size = session.collected_info["group_size"]
            if isinstance(group_size, str) and group_size.isdigit():
                group_size = int(group_size)
            filtered_properties = self.filter_by_group_size(filtered_properties, group_size)
            logger.info(f"Group size filtered, remaining {len(filtered_properties)} properties")
        
        # Filter by environment preference
        if session.collected_info.get("preferred_environment"):
            environment = session.collected_info["preferred_environment"]
            filtered_properties = self.filter_by_environment(filtered_properties, environment)
            logger.info(f"Environment filtered, remaining {len(filtered_properties)} properties")
        
        # Filter by required features
        if session.collected_info.get("must_have_features"):
            features = session.collected_info["must_have_features"]
            filtered_properties = self.filter_by_features(filtered_properties, features)
            logger.info(f"Features filtered, remaining {len(filtered_properties)} properties")
        
        return filtered_properties
    
    def filter_by_group_size(self, properties: List[Property], group_size: int) -> List[Property]:
        """Filter properties by group size"""
        if group_size <= 2:
            return [p for p in properties if p.max_guests >= group_size]
        elif group_size <= 4:
            return [p for p in properties if p.max_guests >= group_size and p.max_guests <= 6]
        else:
            return [p for p in properties if p.max_guests >= group_size]
    
    def filter_by_environment(self, properties: List[Property], environment: str) -> List[Property]:
        """Filter properties by environment preference"""
        environment = environment.lower()
        if environment in ["beach", "ocean", "waterfront"]:
            return [p for p in properties if "waterfront" in p.tags.lower() or "beach" in p.tags.lower()]
        elif environment in ["mountain", "forest", "nature"]:
            return [p for p in properties if "mountain" in p.tags.lower() or "forest" in p.tags.lower()]
        elif environment in ["city", "urban", "downtown"]:
            return [p for p in properties if "downtown" in p.tags.lower() or "city" in p.tags.lower()]
        else:
            return properties
    
    def filter_by_features(self, properties: List[Property], features: List[str]) -> List[Property]:
        """Filter properties by required features"""
        if not features:
            return properties
        
        filtered = []
        for prop in properties:
            prop_features = prop.features.lower()
            if all(feature.lower() in prop_features for feature in features):
                filtered.append(prop)
        return filtered
    
    def score_properties_by_preferences(self, properties: List[Property], session) -> List[Tuple[Property, float]]:
        """Score properties based on user preferences"""
        scored_properties = []
        
        for prop in properties:
            try:
                score = 0.0
                
                # Budget scoring (closer to preferred budget = higher score)
                if session.collected_info.get("budget_range"):
                    budget_range = session.collected_info["budget_range"]
                    if isinstance(budget_range, tuple):
                        preferred_budget = (budget_range[0] + budget_range[1]) / 2
                    else:
                        preferred_budget = budget_range
                    
                    budget_diff = abs(prop.nightly_price - preferred_budget)
                    if budget_diff <= 50:
                        score += 30
                    elif budget_diff <= 100:
                        score += 20
                    elif budget_diff <= 200:
                        score += 10
                
                # Environment scoring
                if session.collected_info.get("preferred_environment"):
                    environment = session.collected_info["preferred_environment"].lower()
                    if environment in prop.tags.lower():
                        score += 20
                
                # Features scoring
                if session.collected_info.get("must_have_features"):
                    features = session.collected_info["must_have_features"]
                    feature_matches = sum(1 for feature in features if feature.lower() in prop.features.lower())
                    score += feature_matches * 10
                
                # Location scoring (if destination matches)
                if session.collected_info.get("destination"):
                    destination = session.collected_info["destination"].lower()
                    if destination in prop.location.lower():
                        score += 25
                
                # Base score for all properties
                score += 50
                
                scored_properties.append((prop, score))
                
            except Exception as e:
                logger.error(f"Error scoring property {prop.property_id}: {e}")
                scored_properties.append((prop, 0.0))
        
        # Sort by score (highest first)
        scored_properties.sort(key=lambda x: x[1], reverse=True)
        return scored_properties
    
    def generate_recommendation_reason(self, property: Property, session) -> str:
        """Generate personalized reason for recommendation"""
        reasons = []
        
        if session.collected_info.get("destination"):
            destination = session.collected_info["destination"]
            reasons.append(f"Located in {destination}")
        
        if session.collected_info.get("budget_range"):
            budget_range = session.collected_info["budget_range"]
            if isinstance(budget_range, tuple):
                reasons.append(f"Within your budget range (${budget_range[0]}-${budget_range[1]})")
            else:
                reasons.append(f"Fits your budget of ${budget_range}")
        
        if session.collected_info.get("group_size"):
            group_size = session.collected_info["group_size"]
            reasons.append(f"Accommodates {group_size} people")
        
        if session.collected_info.get("preferred_environment"):
            environment = session.collected_info["preferred_environment"]
            reasons.append(f"Matches your preferred {environment} environment")
        
        if reasons:
            return " | ".join(reasons)
        else:
            return "Based on your preferences"
    
    def generate_travel_recommendations(self, session) -> str:
        """Generate travel recommendations based on session data"""
        try:
            # Filter properties
            filtered_properties = self.filter_properties_for_travel_planning(session)
            
            if not filtered_properties:
                return "Sorry, I couldn't find any properties matching your criteria. Please try adjusting your preferences."
            
            # Score properties
            scored_properties = self.score_properties_by_preferences(filtered_properties, session)
            
            # Take top 5 recommendations
            top_recommendations = scored_properties[:5]
            
            # Format recommendations
            recommendations_text = self.format_recommendations_text(top_recommendations, session)
            
            return recommendations_text
            
        except Exception as e:
            logger.error(f"Failed to generate travel recommendations: {e}")
            return "Sorry, I encountered an error while generating recommendations. Please try again."
    
    def format_recommendations_text(self, scored_properties: List[Tuple[Property, float]], session) -> str:
        """Format recommendations as text"""
        if not scored_properties:
            return "No recommendations available."
        
        result = f"Based on your preferences, here are my top recommendations:\n\n"
        
        for i, (prop, score) in enumerate(scored_properties, 1):
            reason = self.generate_recommendation_reason(prop, session)
            
            result += f"{i}. **{prop.title}**\n"
            result += f"   📍 {prop.location}\n"
            result += f"   💰 ${prop.nightly_price}/night\n"
            result += f"   👥 Up to {prop.max_guests} guests\n"
            result += f"   🏠 {prop.property_type}\n"
            result += f"   ✨ {reason}\n\n"
        
        result += f"Found {len(scored_properties)} properties matching your criteria. "
        result += "Would you like me to help you with anything else?"
        
        return result
