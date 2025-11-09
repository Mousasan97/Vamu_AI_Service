"""Google Places API client implementation."""
import httpx
import logging
from typing import List, Optional, Dict, Any
from app.config import settings
from app.shared.exceptions import (
    GooglePlacesAPIError,
    RateLimitError,
    AuthenticationError,
)
from app.features.inspiration.domain.entities.venue import Venue, OpeningHours
from app.features.inspiration.domain.entities.location import Location
from app.features.inspiration.domain.entities.search_params import SearchParams


logger = logging.getLogger(__name__)


class GooglePlacesProvider:
    """
    Client for Google Places API Text Search.
    Handles HTTP requests, error handling, and response parsing.
    """
    
    # Field mask for optimal cost/data balance
    FIELD_MASK = ",".join([
        # Essentials (cheapest)
        "places.id",
        "places.name",
        
        # Pro SKU
        "places.displayName",
        "places.formattedAddress",
        "places.location",
        "places.types",
        "places.viewport",
        "places.googleMapsUri",
        
        # Enterprise SKU
        "places.rating",
        "places.userRatingCount",
        "places.priceLevel",
        "places.websiteUri",
        "places.nationalPhoneNumber",
        "places.currentOpeningHours",
        "places.businessStatus",
        
        # Pagination
        "nextPageToken",
    ])
    
    def __init__(self, api_key: str = None, base_url: str = None):
        """Initialize Google Places provider."""
        self.api_key = api_key or settings.GOOGLE_PLACES_API_KEY
        self.base_url = base_url or settings.GOOGLE_PLACES_BASE_URL
        self.endpoint = f"{self.base_url}/places:searchText"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_by_text(
        self,
        params: SearchParams,
    ) -> List[Venue]:
        """
        Execute Text Search API request.
        
        Args:
            params: Search parameters
            
        Returns:
            List of Venue entities
            
        Raises:
            GooglePlacesAPIError: On API errors
            RateLimitError: When rate limit exceeded
            AuthenticationError: On auth failures
        """
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": self.FIELD_MASK,
        }
        
        body = params.to_google_api_request()

        logger.info(f"Searching Google Places: {body.get('textQuery')}")
        logger.debug(f"Full Google Places request body: {body}")
        
        try:
            response = await self.client.post(
                self.endpoint,
                headers=headers,
                json=body,
            )
            
            # Handle different error status codes
            if response.status_code == 429:
                raise RateLimitError("Google Places API rate limit exceeded", 429)
            elif response.status_code in [401, 403]:
                raise AuthenticationError(
                    "Google Places API authentication failed",
                    response.status_code
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.text else {}
                error_message = error_data.get("error", {}).get("message", "Unknown error")
                raise GooglePlacesAPIError(
                    f"Google Places API error: {error_message}",
                    response.status_code
                )
            
            response.raise_for_status()
            data = response.json()
            
            # Parse places from response
            places_data = data.get("places", [])
            venues = [self._parse_place(place) for place in places_data]
            
            logger.info(f"Found {len(venues)} venues")
            return venues
            
        except httpx.TimeoutException as e:
            logger.error(f"Google Places API timeout: {e}")
            raise GooglePlacesAPIError("Request timeout") from e
        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling Google Places API: {e}")
            raise GooglePlacesAPIError(f"HTTP error: {str(e)}") from e
    
    def _parse_place(self, place_data: Dict[str, Any]) -> Venue:
        """
        Parse Google Places API response to Venue entity.
        
        Args:
            place_data: Raw place data from API
            
        Returns:
            Venue entity
        """
        # Location
        location_data = place_data.get("location", {})
        location = Location(
            latitude=location_data.get("latitude", 0.0),
            longitude=location_data.get("longitude", 0.0),
        )
        
        # Display name
        display_name_data = place_data.get("displayName", {})
        display_name = display_name_data.get("text", "Unknown")
        
        # Opening hours
        opening_hours_data = place_data.get("currentOpeningHours", {})
        opening_hours = None
        if opening_hours_data:
            opening_hours = OpeningHours(
                open_now=opening_hours_data.get("openNow"),
                weekday_descriptions=opening_hours_data.get("weekdayDescriptions", []),
            )
        
        return Venue(
            place_id=place_data.get("id", ""),
            name=place_data.get("name", ""),
            display_name=display_name,
            address=place_data.get("formattedAddress", ""),
            location=location,
            rating=place_data.get("rating"),
            total_ratings=place_data.get("userRatingCount"),
            price_level=place_data.get("priceLevel"),
            types=place_data.get("types", []),
            business_status=place_data.get("businessStatus"),
            phone=place_data.get("nationalPhoneNumber"),
            website=place_data.get("websiteUri"),
            is_open_now=opening_hours_data.get("openNow") if opening_hours_data else None,
            opening_hours=opening_hours,
            google_maps_uri=place_data.get("googleMapsUri"),
        )
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
