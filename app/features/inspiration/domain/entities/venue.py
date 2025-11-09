"""Venue entity representing a place suggestion."""
from dataclasses import dataclass
from typing import Optional, List
from .location import Location


@dataclass
class OpeningHours:
    """Opening hours information."""
    open_now: Optional[bool] = None
    weekday_descriptions: Optional[List[str]] = None


@dataclass
class Venue:
    """
    Venue entity representing a place suggestion from Google Places.
    Maps Google Places API response to our domain model.
    """
    # Core fields
    place_id: str
    name: str
    display_name: str
    address: str
    location: Location
    
    # Rating & Reviews
    rating: Optional[float] = None
    total_ratings: Optional[int] = None
    
    # Business Info
    price_level: Optional[str] = None
    types: Optional[List[str]] = None
    business_status: Optional[str] = None
    
    # Contact Info
    phone: Optional[str] = None
    website: Optional[str] = None
    
    # Opening Hours
    is_open_now: Optional[bool] = None
    opening_hours: Optional[OpeningHours] = None
    
    # Google Maps
    google_maps_uri: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API response."""
        return {
            "place_id": self.place_id,
            "name": self.name,
            "display_name": self.display_name,
            "address": self.address,
            "location": {
                "latitude": self.location.latitude,
                "longitude": self.location.longitude,
            },
            "rating": self.rating,
            "total_ratings": self.total_ratings,
            "price_level": self.price_level,
            "types": self.types,
            "business_status": self.business_status,
            "phone": self.phone,
            "website": self.website,
            "is_open_now": self.is_open_now,
            "opening_hours": {
                "open_now": self.opening_hours.open_now if self.opening_hours else None,
                "weekday_descriptions": self.opening_hours.weekday_descriptions if self.opening_hours else None,
            } if self.opening_hours else None,
            "google_maps_uri": self.google_maps_uri,
        }
