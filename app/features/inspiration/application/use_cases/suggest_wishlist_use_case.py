"""
Use case for generating wishlist suggestions.
"""
import logging
from typing import List

from app.features.inspiration.infrastructure.providers.groq_provider import GroqProvider
from app.features.inspiration.domain.entities.wishlist_suggestion import WishlistSuggestion

logger = logging.getLogger(__name__)


class SuggestWishlistUseCase:
    """Use case for suggesting items for an event wishlist."""

    def __init__(self, groq_provider: GroqProvider):
        """
        Initialize the use case with dependencies.

        Args:
            groq_provider: Groq LLM provider instance
        """
        self.groq_provider = groq_provider

    async def execute(
        self,
        event_name: str,
        max_items: int = 10
    ) -> WishlistSuggestion:
        """
        Generate wishlist suggestions for an event.

        Args:
            event_name: The name or description of the event
            max_items: Maximum number of items to suggest

        Returns:
            WishlistSuggestion with suggested items

        Raises:
            Various exceptions from the Groq provider
        """
        logger.info(f"Executing SuggestWishlistUseCase for event: {event_name}")

        # Call Groq provider to generate items
        items = await self.groq_provider.generate_wishlist(
            event_name=event_name,
            max_items=max_items
        )

        # Create domain entity
        suggestion = WishlistSuggestion(
            event_name=event_name,
            items=items
        )

        logger.info(f"Generated {suggestion.item_count} items for wishlist")

        return suggestion
