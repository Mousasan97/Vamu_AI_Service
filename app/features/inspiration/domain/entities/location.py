"""Location entity representing geographic coordinates."""
from dataclasses import dataclass


@dataclass
class Location:
    """Geographic location with latitude and longitude."""
    latitude: float
    longitude: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API requests."""
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
