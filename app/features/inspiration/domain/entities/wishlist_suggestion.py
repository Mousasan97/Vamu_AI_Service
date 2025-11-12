"""
Domain entities for wishlist suggestions.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class WishlistItem:
    """Represents a single item suggestion for an event."""

    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class WishlistSuggestion:
    """Represents a complete wishlist suggestion for an event."""

    event_name: str
    items: List[str]

    @property
    def item_count(self) -> int:
        """Returns the number of suggested items."""
        return len(self.items)
