"""Use case for suggesting venue locations based on event details."""
import logging
from typing import List
from app.features.inspiration.domain.entities.venue import Venue
from app.features.inspiration.domain.entities.search_params import SearchParams
from app.features.inspiration.infrastructure.providers.google_places_provider import (
    GooglePlacesProvider,
)


logger = logging.getLogger(__name__)


class SuggestWhereUseCase:
    """
    Use case for suggesting where to hold an event.
    Orchestrates calls to Google Places API.
    """
    
    def __init__(self, places_provider: GooglePlacesProvider):
        """Initialize use case with dependencies."""
        self.places_provider = places_provider
    
    async def execute(self, search_params: SearchParams) -> List[Venue]:
        """
        Execute the use case to find venue suggestions.
        
        Args:
            search_params: Search parameters for finding venues
            
        Returns:
            List of venue suggestions
            
        Raises:
            GooglePlacesAPIError: On API errors
        """
        logger.info(f"Executing SuggestWhereUseCase with query: {search_params.text_query}")
        
        # Call Google Places API
        venues = await self.places_provider.search_by_text(search_params)
        
        # TODO: Future enhancements
        # - Filter based on user preferences from DB
        # - Apply business rules
        # - Personalization based on past events
        # - Combine with other data sources
        
        return venues
