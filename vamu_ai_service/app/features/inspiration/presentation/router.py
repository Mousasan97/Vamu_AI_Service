"""FastAPI router for inspiration endpoints."""
import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.features.inspiration.presentation.schemas import (
    WhereInspirationRequest,
    WhereInspirationResponse,
    VenueResponse,
    LocationResponse,
    OpeningHoursResponse,
    ErrorResponse,
)
from app.features.inspiration.domain.entities.search_params import SearchParams
from app.features.inspiration.domain.entities.location import Location
from app.features.inspiration.application.use_cases.suggest_where_use_case import (
    SuggestWhereUseCase,
)
from app.features.inspiration.infrastructure.providers.google_places_provider import (
    GooglePlacesProvider,
)
from app.shared.exceptions import GooglePlacesAPIError, RateLimitError, AuthenticationError


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/inspiration", tags=["Inspiration"])


# Dependency injection
def get_places_provider() -> GooglePlacesProvider:
    """Get Google Places provider instance."""
    return GooglePlacesProvider()


def get_suggest_where_use_case(
    places_provider: GooglePlacesProvider = Depends(get_places_provider),
) -> SuggestWhereUseCase:
    """Get SuggestWhereUseCase instance with dependencies."""
    return SuggestWhereUseCase(places_provider=places_provider)


@router.post(
    "/where",
    response_model=WhereInspirationResponse,
    responses={
        200: {"description": "Successful response with venue suggestions"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
    summary="Get venue suggestions for an event",
    description="Suggests venues based on event description using Google Places API",
)
async def suggest_where(
    request: WhereInspirationRequest,
    use_case: SuggestWhereUseCase = Depends(get_suggest_where_use_case),
):
    """
    Suggest venues for an event based on the 'what' description.
    
    Example:
        Request: {"what": "Pizza night in Milan", "location": {...}}
        Response: List of pizza restaurants in Milan
    """
    try:
        logger.info(f"Received where inspiration request: {request.what}")
        
        # Build search parameters from request
        search_params = _build_search_params(request)
        
        # Execute use case
        venues = await use_case.execute(search_params)
        
        # Convert to response format
        venue_responses = [_venue_to_response(venue) for venue in venues]
        
        return WhereInspirationResponse(
            suggestions=venue_responses,
            total_count=len(venue_responses),
            query=search_params.text_query,
        )
        
    except RateLimitError as e:
        logger.error(f"Rate limit error: {e}")
        raise HTTPException(status_code=429, detail=str(e))
    
    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail="Service configuration error")
    
    except GooglePlacesAPIError as e:
        logger.error(f"Google Places API error: {e}")
        raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def _build_search_params(request: WhereInspirationRequest) -> SearchParams:
    """
    Build SearchParams from request.

    Smart handling: If 'what' contains location keywords, don't send locationBias
    to avoid conflicts with Google Places text query parsing.
    """
    # Extract preferences
    prefs = request.preferences or {}

    # Check if 'what' contains location indicators
    # Common patterns: "in Paris", "near Tokyo", "at Barcelona", "Milano", etc.
    location_keywords = [' in ', ' near ', ' at ', ' around ']
    has_location_in_text = any(keyword in request.what.lower() for keyword in location_keywords)

    # Only use location bias if no location mentioned in text
    # This prevents conflicts where locationBias overrides the text query
    location_bias = None
    if request.location and not has_location_in_text:
        location_bias = Location(
            latitude=request.location.latitude,
            longitude=request.location.longitude,
        )
        logger.debug(f"Using locationBias from coordinates (no location in text)")
    elif request.location and has_location_in_text:
        logger.debug(f"Skipping locationBias - location detected in text: '{request.what}'")

    # Map price levels
    price_levels = None
    if prefs.price_level:
        price_levels = prefs.price_level

    return SearchParams(
        text_query=request.what,
        location_bias=location_bias,
        location_radius=request.location_radius or 5000.0,
        max_result_count=prefs.max_results if hasattr(prefs, 'max_results') else 8,
        min_rating=prefs.min_rating if hasattr(prefs, 'min_rating') else None,
        price_levels=price_levels,
        is_open_now=prefs.open_now if hasattr(prefs, 'open_now') else False,
        language="en-US",
    )


def _venue_to_response(venue) -> VenueResponse:
    """Convert Venue entity to VenueResponse schema."""
    return VenueResponse(
        place_id=venue.place_id,
        name=venue.name,
        display_name=venue.display_name,
        address=venue.address,
        location=LocationResponse(
            latitude=venue.location.latitude,
            longitude=venue.location.longitude,
        ),
        rating=venue.rating,
        total_ratings=venue.total_ratings,
        price_level=venue.price_level,
        types=venue.types,
        business_status=venue.business_status,
        phone=venue.phone,
        website=venue.website,
        is_open_now=venue.is_open_now,
        opening_hours=OpeningHoursResponse(
            open_now=venue.opening_hours.open_now if venue.opening_hours else None,
            weekday_descriptions=venue.opening_hours.weekday_descriptions if venue.opening_hours else None,
        ) if venue.opening_hours else None,
        google_maps_uri=venue.google_maps_uri,
    )


@router.get("/health", summary="Health check")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "inspiration"}
