"""
Vectorized Filtering Module
Uses numpy and pandas for efficient property filtering operations
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorizedPropertyFilter:
    """
    Efficient property filtering using vectorized operations
    """
    
    def __init__(self, properties_data: List[Dict[str, Any]]):
        """
        Initialize with properties data
        
        Args:
            properties_data: List of property dictionaries from database
        """
        self.properties_data = properties_data
        self.df = None
        self._prepare_dataframe()
    
    def _prepare_dataframe(self):
        """Convert properties data to pandas DataFrame for vectorized operations"""
        try:
            # Convert to DataFrame
            self.df = pd.DataFrame(self.properties_data)
            
            # Ensure numeric columns are properly typed
            if 'nightly_price' in self.df.columns:
                self.df['nightly_price'] = pd.to_numeric(self.df['nightly_price'], errors='coerce')
            
            # Process features and tags columns
            if 'features' in self.df.columns:
                self.df['features'] = self.df['features'].apply(
                    lambda x: x if isinstance(x, list) else (x.split(',') if x else [])
                )
            
            if 'tags' in self.df.columns:
                self.df['tags'] = self.df['tags'].apply(
                    lambda x: x if isinstance(x, list) else (x.split(',') if x else [])
                )
            
            logger.info(f"DataFrame prepared with {len(self.df)} properties")
            
        except Exception as e:
            logger.error(f"Error preparing DataFrame: {e}")
            self.df = pd.DataFrame()
    
    def filter_by_budget(self, min_budget: float, max_budget: float) -> pd.DataFrame:
        """
        Filter properties by budget range using vectorized operations
        
        Args:
            min_budget: Minimum nightly price
            max_budget: Maximum nightly price
            
        Returns:
            Filtered DataFrame
        """
        if self.df.empty or 'nightly_price' not in self.df.columns:
            return pd.DataFrame()
        
        # Vectorized budget filtering
        budget_mask = (self.df['nightly_price'] >= min_budget) & (self.df['nightly_price'] <= max_budget)
        filtered_df = self.df[budget_mask].copy()
        
        logger.info(f"Budget filter: {len(filtered_df)} properties match ${min_budget}-${max_budget}")
        return filtered_df
    
    def filter_by_features(self, selected_features: List[str], case_sensitive: bool = False) -> pd.DataFrame:
        """
        Filter properties by features using vectorized operations
        
        Args:
            selected_features: List of features to match
            case_sensitive: Whether to perform case-sensitive matching
            
        Returns:
            Filtered DataFrame
        """
        if self.df.empty or 'features' not in self.df.columns or not selected_features:
            return self.df.copy()
        
        # Normalize features for case-insensitive matching
        if not case_sensitive:
            selected_features = [f.lower().strip() for f in selected_features]
        
        # Vectorized feature matching
        def has_features(features_list):
            if not isinstance(features_list, list):
                return False
            
            if case_sensitive:
                return any(feature in features_list for feature in selected_features)
            else:
                normalized_features = [f.lower().strip() for f in features_list]
                return any(feature in normalized_features for feature in selected_features)
        
        # Apply vectorized filtering
        feature_mask = self.df['features'].apply(has_features)
        filtered_df = self.df[feature_mask].copy()
        
        logger.info(f"Feature filter: {len(filtered_df)} properties match features {selected_features}")
        return filtered_df
    
    def filter_by_property_type(self, selected_types: List[str], case_sensitive: bool = False) -> pd.DataFrame:
        """
        Filter properties by property type using vectorized operations
        
        Args:
            selected_types: List of property types to match
            case_sensitive: Whether to perform case-sensitive matching
            
        Returns:
            Filtered DataFrame
        """
        if self.df.empty or 'ptype' not in self.df.columns or not selected_types:
            return self.df.copy()
        
        # Normalize types for case-insensitive matching
        if not case_sensitive:
            selected_types = [t.lower().strip() for t in selected_types]
            type_mask = self.df['ptype'].str.lower().str.strip().isin(selected_types)
        else:
            type_mask = self.df['ptype'].isin(selected_types)
        
        filtered_df = self.df[type_mask].copy()
        
        logger.info(f"Type filter: {len(filtered_df)} properties match types {selected_types}")
        return filtered_df
    
    def filter_by_location(self, selected_locations: List[str], case_sensitive: bool = False) -> pd.DataFrame:
        """
        Filter properties by location using vectorized operations
        
        Args:
            selected_locations: List of locations to match
            case_sensitive: Whether to perform case-sensitive matching
            
        Returns:
            Filtered DataFrame
        """
        if self.df.empty or 'location' not in self.df.columns or not selected_locations:
            return self.df.copy()
        
        # Normalize locations for case-insensitive matching
        if not case_sensitive:
            selected_locations = [l.lower().strip() for l in selected_locations]
            location_mask = self.df['location'].str.lower().str.strip().isin(selected_locations)
        else:
            location_mask = self.df['location'].isin(selected_locations)
        
        filtered_df = self.df[location_mask].copy()
        
        logger.info(f"Location filter: {len(filtered_df)} properties match locations {selected_locations}")
        return filtered_df
    
    def apply_combined_filters(self, 
                              budget_range: Optional[Tuple[float, float]] = None,
                              features: Optional[List[str]] = None,
                              property_types: Optional[List[str]] = None,
                              locations: Optional[List[str]] = None,
                              case_sensitive: bool = False) -> pd.DataFrame:
        """
        Apply multiple filters simultaneously using vectorized operations
        
        Args:
            budget_range: Tuple of (min_budget, max_budget)
            features: List of features to match
            property_types: List of property types to match
            locations: List of locations to match
            case_sensitive: Whether to perform case-sensitive matching
            
        Returns:
            Filtered DataFrame with all filters applied
        """
        if self.df.empty:
            return pd.DataFrame()
        
        # Start with all properties
        filtered_df = self.df.copy()
        
        # Apply budget filter
        if budget_range and len(budget_range) == 2:
            min_budget, max_budget = budget_range
            if min_budget is not None and max_budget is not None:
                filtered_df = self.filter_by_budget(min_budget, max_budget)
        
        # Apply features filter
        if features:
            filtered_df = self.filter_by_features(features, case_sensitive)
        
        # Apply property type filter
        if property_types:
            filtered_df = self.filter_by_property_type(property_types, case_sensitive)
        
        # Apply location filter
        if locations:
            filtered_df = self.filter_by_location(locations, case_sensitive)
        
        logger.info(f"Combined filters applied: {len(filtered_df)} properties remain")
        return filtered_df
    
    def get_filter_statistics(self, filtered_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get statistics about filtered properties
        
        Args:
            filtered_df: Filtered DataFrame
            
        Returns:
            Dictionary with statistics
        """
        if filtered_df.empty:
            return {
                'total_properties': 0,
                'avg_price': 0,
                'price_range': (0, 0),
                'feature_counts': {},
                'type_counts': {},
                'location_counts': {}
            }
        
        stats = {
            'total_properties': len(filtered_df),
            'avg_price': filtered_df['nightly_price'].mean() if 'nightly_price' in filtered_df.columns else 0,
            'price_range': (
                filtered_df['nightly_price'].min() if 'nightly_price' in filtered_df.columns else 0,
                filtered_df['nightly_price'].max() if 'nightly_price' in filtered_df.columns else 0
            )
        }
        
        # Feature distribution
        if 'features' in filtered_df.columns:
            all_features = []
            for features_list in filtered_df['features']:
                if isinstance(features_list, list):
                    all_features.extend(features_list)
            
            if all_features:
                feature_counts = pd.Series(all_features).value_counts()
                stats['feature_counts'] = feature_counts.head(10).to_dict()
        
        # Property type distribution
        if 'ptype' in filtered_df.columns:
            type_counts = filtered_df['ptype'].value_counts()
            stats['type_counts'] = type_counts.to_dict()
        
        # Location distribution
        if 'location' in filtered_df.columns:
            location_counts = filtered_df['location'].value_counts()
            stats['location_counts'] = location_counts.to_dict()
        
        return stats
    
    def get_unique_features(self, case_sensitive: bool = False) -> List[str]:
        """Get unique features from all properties"""
        if self.df.empty or 'features' not in self.df.columns:
            return []
        
        all_features = []
        for features_list in self.df['features']:
            if isinstance(features_list, list):
                all_features.extend(features_list)
        
        if not case_sensitive:
            all_features = [f.lower().strip() for f in all_features]
        
        unique_features = list(set(all_features))
        unique_features.sort()
        
        return unique_features
    
    def get_unique_property_types(self, case_sensitive: bool = False) -> List[str]:
        """Get unique property types from all properties"""
        if self.df.empty or 'ptype' not in self.df.columns:
            return []
        
        if case_sensitive:
            unique_types = self.df['ptype'].unique().tolist()
        else:
            unique_types = self.df['ptype'].str.lower().str.strip().unique().tolist()
        
        unique_types.sort()
        return unique_types
    
    def get_unique_locations(self, case_sensitive: bool = False) -> List[str]:
        """Get unique locations from all properties"""
        if self.df.empty or 'location' not in self.df.columns:
            return []
        
        if case_sensitive:
            unique_locations = self.df['location'].unique().tolist()
        else:
            unique_locations = self.df['location'].str.lower().str.strip().unique().tolist()
        
        unique_locations.sort()
        return unique_locations


def create_vectorized_filter(properties_data: List[Dict[str, Any]]) -> VectorizedPropertyFilter:
    """
    Factory function to create a VectorizedPropertyFilter instance
    
    Args:
        properties_data: List of property dictionaries
        
    Returns:
        VectorizedPropertyFilter instance
    """
    return VectorizedPropertyFilter(properties_data)


# Example usage and testing
if __name__ == "__main__":
    # Test data
    test_properties = [
        {
            'property_id': 1,
            'location': 'Banff',
            'ptype': 'Cabin',
            'nightly_price': 200.0,
            'features': ['WiFi', 'Hot Tub', 'Mountain View'],
            'tags': ['mountain', 'nature']
        },
        {
            'property_id': 2,
            'location': 'Vancouver',
            'ptype': 'Apartment',
            'nightly_price': 150.0,
            'features': ['WiFi', 'Balcony', 'City View'],
            'tags': ['city', 'urban']
        }
    ]
    
    # Create filter
    filter_instance = create_vectorized_filter(test_properties)
    
    # Test filtering
    print("Unique features:", filter_instance.get_unique_features())
    print("Unique types:", filter_instance.get_unique_property_types())
    print("Unique locations:", filter_instance.get_unique_locations())
    
    # Test combined filtering
    filtered = filter_instance.apply_combined_filters(
        budget_range=(100, 250),
        features=['WiFi'],
        property_types=['Cabin']
    )
    
    print(f"Filtered properties: {len(filtered)}")
    print(filtered)
