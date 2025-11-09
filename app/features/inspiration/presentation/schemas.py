"""Pydantic schemas for FastAPI request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List


# Request Schemas

class LocationRequest(BaseModel):
    """Location coordinates in request."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")


class PreferencesRequest(BaseModel):
    """User preferences for venue search."""
    max_results: int = Field(8, ge=1, le=20, description="Maximum number of results")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")
    price_level: Optional[List[str]] = Field(None, description="Preferred price levels")
    open_now: bool = Field(False, description="Only show currently open venues")


class WhereInspirationRequest(BaseModel):
    """Request for where to hold an event."""
    what: str = Field(..., min_length=1, description="Event description (e.g., 'Pizza night in Milan')")
    when: Optional[str] = Field(None, description="Event date/time (ISO format)")
    location: Optional[LocationRequest] = Field(None, description="Location bias for search")
    location_radius: Optional[float] = Field(5000.0, description="Search radius in meters")
    preferences: Optional[PreferencesRequest] = Field(None, description="Search preferences")
    
    class Config:
        json_schema_extra = {
            "example": {
                "what": "Pizza night in Milan",
                "when": "2025-11-15T19:00:00",
                "location": {
                    "latitude": 45.4642,
                    "longitude": 9.1900
                },
                "location_radius": 5000,
                "preferences": {
                    "max_results": 8,
                    "min_rating": 4.0,
                    "price_level": ["PRICE_LEVEL_MODERATE"],
                    "open_now": True
                }
            }
        }


# Response Schemas

class LocationResponse(BaseModel):
    """Location in response."""
    latitude: float
    longitude: float


class OpeningHoursResponse(BaseModel):
    """Opening hours information."""
    open_now: Optional[bool] = None
    weekday_descriptions: Optional[List[str]] = None


class VenueResponse(BaseModel):
    """Venue suggestion response."""
    place_id: str
    name: str
    display_name: str
    address: str
    location: LocationResponse
    rating: Optional[float] = None
    total_ratings: Optional[int] = None
    price_level: Optional[str] = None
    types: Optional[List[str]] = None
    business_status: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    is_open_now: Optional[bool] = None
    opening_hours: Optional[OpeningHoursResponse] = None
    google_maps_uri: Optional[str] = None


class WhereInspirationResponse(BaseModel):
    """Response containing venue suggestions."""
    suggestions: List[VenueResponse]
    total_count: int
    query: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "suggestions": [
                    {
                        "place_id": "ChIJ...",
                        "name": "places/ChIJ...",
                        "display_name": "Pizzeria Spontini",
                        "address": "Via Gaspare Spontini, 4, 20131 Milano MI, Italy",
                        "location": {
                            "latitude": 45.4752,
                            "longitude": 9.2088
                        },
                        "rating": 4.5,
                        "total_ratings": 2341,
                        "price_level": "PRICE_LEVEL_MODERATE",
                        "types": ["restaurant", "pizza_restaurant", "food"],
                        "business_status": "OPERATIONAL",
                        "phone": "+39 02 ...",
                        "website": "https://...",
                        "is_open_now": True,
                        "google_maps_uri": "https://maps.google.com/?cid=..."
                    }
                ],
                "total_count": 5,
                "query": "pizza restaurant Milan"
            }
        }


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    status_code: int
