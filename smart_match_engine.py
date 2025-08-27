#!/usr/bin/env python3
"""
Smart Match Engine
Implements weight-based attribute scoring and intelligent matching functionality
"""

import numpy as np
import pandas as pd
import math
import requests
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class SmartMatchEngine:
    def __init__(self):
        self.nominatim_headers = {
            'User-Agent': 'VacationRentalsApp/1.0 (https://example.com; contact@example.com)'
        }
    
    def get_location_coordinates(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Get address coordinates using Nominatim API
        
        Args:
            location: Address string (e.g., "Toronto" or "219 Dundas Street E")
            
        Returns:
            (latitude, longitude) tuple, returns None if failed
        """
        try:
            base_url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': f"{location}, Canada",
                'format': 'json',
                'limit': 1,
                'addressdetails': 0
            }
            
            response = requests.get(base_url, params=params, headers=self.nominatim_headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                logger.info(f"Got center coordinates: {location} -> ({lat}, {lon})")
                return lat, lon
            else:
                logger.warning(f"Address coordinates not found: {location}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get address coordinates for {location}: {e}")
            return None
    
    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinate points using Haversine formula (kilometers)
        
        Args:
            lat1, lon1: Coordinates of the first point
            lat2, lon2: Coordinates of the second point
            
        Returns:
            Distance (kilometers)
        """
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth radius (kilometers)
        r = 6371
        
        return c * r
    
    def calculate_type_score(self, property_type: str, selected_types: List[str]) -> float:
        """
        Calculate type matching score
        
        Args:
            property_type: Property type
            selected_types: List of user-selected types
            
        Returns:
            Type score (0 or 1)
        """
        # Debug logging
        logger.info(f"calculate_type_score: property_type='{property_type}', selected_types={selected_types}")
        
        if not selected_types:
            logger.info("No selected types, returning 0.0")
            return 0.0
            
        if not property_type:
            logger.info("No property type, returning 0.0")
            return 0.0
        
        # Convert to lowercase for case-insensitive comparison
        property_type_lower = property_type.lower()
        selected_types_lower = [t.lower() for t in selected_types]
        
        logger.info(f"Case-insensitive comparison: property_type='{property_type_lower}', selected_types={selected_types_lower}")
        
        # Check if property_type is in selected_types (case-insensitive)
        is_match = property_type_lower in selected_types_lower
        logger.info(f"Type match result: {is_match} ('{property_type_lower}' in {selected_types_lower})")
        
        return 1.0 if is_match else 0.0
    
    def calculate_feature_score(self, property_features: List[str], selected_features: List[str]) -> float:
        """
        Calculate feature matching score
        
        Args:
            property_features: Property features list
            selected_features: User-selected features list
            
        Returns:
            Feature score (between 0 and 1)
        """
        if not selected_features:
            return 1.0  # If user hasn't selected features, give full score
        
        if not property_features:
            return 0.0  # If property has no features, give 0 score
        
        # Convert to lowercase for case-insensitive comparison
        property_features_lower = [f.lower() for f in property_features]
        selected_features_lower = [f.lower() for f in selected_features]
        
        # Calculate number of matched features (case-insensitive)
        matched_count = len(set(property_features_lower) & set(selected_features_lower))
        return matched_count / len(selected_features)
    
    def calculate_location_score(self, property_lat: float, property_lon: float, 
                                center_lat: float, center_lon: float, radius: float) -> float:
        """
        Calculate location matching score
        
        Args:
            property_lat, property_lon: Property coordinates
            center_lat, center_lon: Center coordinates
            radius: User-set radius (kilometers)
            
        Returns:
            Location score (between 0 and 1)
        """
        # Calculate distance
        distance = self.haversine_distance(property_lat, property_lon, center_lat, center_lon)
        
        # Within radius
        if distance <= radius:
            return 1.0
        
        # Outside radius, calculate score
        score = 1.0 - (distance - radius) / radius
        return max(0.0, score)  # Ensure score is not less than 0
    
    def calculate_price_score(self, property_price: float, min_budget: float, 
                             max_budget: float) -> float:
        """
        Calculate price matching score
        
        Args:
            property_price: Property price
            min_budget: User minimum budget
            max_budget: User maximum budget
            
        Returns:
            Price score (between 0 and 1)
        """
        # Less than minimum budget
        if property_price < min_budget:
            return 0.0
        
        # Within budget range
        if property_price <= max_budget:
            return 1.0
        
        # Exceeds maximum budget, calculate discount rate
        discount_rate = self.property_budget_discount_rate(max_budget, property_price)
        return 1.0 - discount_rate
    
    def property_budget_discount_rate(self, user_max_budget: float, property_price: float) -> float:
        """
        Calculate budget discount rate (copied from user-provided function)
        
        Args:
            user_max_budget: User maximum budget
            property_price: Property price
            
        Returns:
            Discount rate (between 0 and 1)
        """
        # Calculate amount exceeding budget
        difference = property_price - user_max_budget
        
        # Within budget, no discount
        if difference <= 0:
            return 0
        
        # Exceeds 20% of budget, full discount
        elif difference > 0.2 * user_max_budget:
            return 1
        
        # Within 0-20% over budget range, apply quadratic discount rate
        else:
            return (difference / (0.2 * user_max_budget)) ** 1.7
    
    def calculate_total_scores(self, properties_df: pd.DataFrame, 
                              selected_types: List[str],
                              selected_features: List[str],
                              center_location: str,
                              radius: float,
                              min_budget: float,
                              max_budget: float,
                              location_weight: int,
                              type_weight: int,
                              features_weight: int,
                              price_weight: int) -> pd.DataFrame:
        """
        Calculate total scores for all properties
        
        Args:
            properties_df: DataFrame containing property information
            selected_types: List of user-selected types
            selected_features: List of user-selected features
            center_location: Center location (address)
            radius: Radius (kilometers)
            min_budget: Minimum budget
            max_budget: Maximum budget
            location_weight: Location weight
            type_weight: Type weight
            features_weight: Features weight
            price_weight: Price weight
            
        Returns:
            DataFrame with total scores, sorted by score
        """
        try:
            # Get center coordinates
            center_coords = self.get_location_coordinates(center_location)
            if not center_coords:
                logger.error(f"Could not get center location coordinates: {center_location}")
                return pd.DataFrame()
            
            center_lat, center_lon = center_coords
            
            # Calculate total weight
            total_weight = location_weight + type_weight + features_weight + price_weight
            
            # Create scores list
            scores = []
            
            for _, property_row in properties_df.iterrows():
                # Debug: Log the data being processed
                logger.info(f"Processing property {property_row['property_id']}: type={property_row['ptype']}, selected_types={selected_types}")
                
                # Calculate individual scores
                type_score = self.calculate_type_score(property_row['ptype'], selected_types)
                features_score = self.calculate_feature_score(
                    property_row['features'] if property_row['features'] else [], 
                    selected_features
                )
                location_score = self.calculate_location_score(
                    property_row['latitude'], property_row['longitude'],
                    center_lat, center_lon, radius
                )
                price_score = self.calculate_price_score(
                    property_row['nightly_price'], min_budget, max_budget
                )
                
                # Debug: Log individual scores
                logger.info(f"Property {property_row['property_id']} scores: type={type_score}, features={features_score}, location={location_score}, price={price_score}")
                
                # Calculate weighted total score
                total_score = (
                    type_score * type_weight +
                    features_score * features_weight +
                    location_score * location_weight +
                    price_score * price_weight
                ) / total_weight
                
                scores.append({
                    'property_id': property_row['property_id'],
                    'type_score': type_score,
                    'features_score': features_score,
                    'location_score': location_score,
                    'price_score': price_score,
                    'total_score': total_score
                })
            
            # Create scores DataFrame
            scores_df = pd.DataFrame(scores)
            
            # Merge original data with scores
            result_df = properties_df.merge(scores_df, on='property_id')
            
            # Sort by total score, descending
            result_df = result_df.sort_values('total_score', ascending=False)
            
            # Keep only top 20
            result_df = result_df.head(20)
            
            logger.info(f"Smart Match completed, found {len(result_df)} matching properties")
            return result_df
            
        except Exception as e:
            logger.error(f"Failed to calculate Smart Match scores: {e}")
            return pd.DataFrame()

# Create global instance
smart_match_engine = SmartMatchEngine()
