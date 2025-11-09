"""Search parameters for Google Places API."""
from dataclasses import dataclass, field
from typing import Optional, List
from .location import Location


@dataclass
class SearchParams:
    """
    Parameters for Google Places Text Search API.
    Maps our domain requirements to Google Places API format.
    """
    # Required
    text_query: str
    
    # Location
    location_bias: Optional[Location] = None
    location_radius: float = 5000.0  # meters
    
    # Filters
    included_type: Optional[str] = None
    min_rating: Optional[float] = None
    price_levels: Optional[List[str]] = None
    is_open_now: bool = False
    
    # Result Configuration
    max_result_count: int = 8
    language: str = "en-US"
    region_code: Optional[str] = None
    
    # Advanced
    use_strict_type_filtering: bool = True
    rank_preference: str = "RELEVANCE"  # or "DISTANCE"
    
    def to_google_api_request(self) -> dict:
        """Convert to Google Places API request format."""
        request = {
            "textQuery": self.text_query,
            "maxResultCount": min(self.max_result_count, 20),  # API limit
            "languageCode": self.language,
        }
        
        # Location bias (circle)
        if self.location_bias:
            request["locationBias"] = {
                "circle": {
                    "center": self.location_bias.to_dict(),
                    "radius": self.location_radius,
                }
            }
        
        # Filters
        if self.included_type:
            request["includedType"] = self.included_type
            request["useStrictTypeFiltering"] = self.use_strict_type_filtering
        
        if self.min_rating is not None:
            request["minRating"] = self.min_rating
        
        if self.price_levels:
            request["priceLevels"] = self.price_levels
        
        if self.is_open_now:
            request["openNow"] = True
        
        if self.region_code:
            request["regionCode"] = self.region_code
        
        request["rankPreference"] = self.rank_preference
        
        return request
