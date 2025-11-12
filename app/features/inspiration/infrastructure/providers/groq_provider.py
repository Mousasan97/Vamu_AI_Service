"""
Groq LLM provider for generating wishlist suggestions.
"""
import logging
import json
from typing import List
import httpx

from app.config import settings
from app.shared.exceptions import LLMAPIError, AuthenticationError, RateLimitError

logger = logging.getLogger(__name__)


class GroqProvider:
    """Provider for Groq LLM API."""

    def __init__(self, api_key: str = None):
        """
        Initialize Groq provider.

        Args:
            api_key: Groq API key. If not provided, uses settings.GROQ_API_KEY
        """
        self.api_key = api_key or settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama-3.1-8b-instant"

        if not self.api_key:
            raise AuthenticationError("Groq API key is required")

    async def generate_wishlist(
        self,
        event_name: str,
        max_items: int = 10
    ) -> List[str]:
        """
        Generate wishlist items for an event using Groq LLM.

        Args:
            event_name: The name or description of the event
            max_items: Maximum number of items to suggest

        Returns:
            List of suggested item names

        Raises:
            AuthenticationError: If API key is invalid
            RateLimitError: If rate limit is exceeded
            LLMAPIError: For other API errors
        """
        try:
            logger.info(f"Generating wishlist for event: {event_name}")

            system_prompt = (
                "You are a recommendation system. Given the name of an event, "
                "respond with a list of necessary items in JSON format only. "
                "Do not include any explanations or text outside the JSON.\n\n"
                "Output format:\n"
                "{\n"
                '  "event": "<event_name_here>",\n'
                '  "items_needed": [\n'
                '    "item1",\n'
                '    "item2",\n'
                '    "item3"\n'
                "  ]\n"
                "}"
            )

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": event_name}
                ],
                "temperature": 1,
                "max_tokens": 1024,
                "top_p": 1,
                "stream": False,
                "response_format": {"type": "json_object"}
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            logger.debug(f"Sending request to Groq API: {self.base_url}/chat/completions")

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers
                )

                if response.status_code == 401:
                    logger.error("Groq API authentication failed")
                    raise AuthenticationError("Invalid Groq API key")

                if response.status_code == 429:
                    logger.error("Groq API rate limit exceeded")
                    raise RateLimitError("Rate limit exceeded for Groq API")

                if response.status_code != 200:
                    error_msg = f"Groq API error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise LLMAPIError(error_msg)

                data = response.json()
                content = data["choices"][0]["message"]["content"]

                logger.debug(f"Groq API response: {content}")

                # Parse JSON response
                try:
                    parsed = json.loads(content)
                    items = parsed.get("items_needed", [])

                    # Limit to max_items
                    items = items[:max_items]

                    logger.info(f"Successfully generated {len(items)} wishlist items")
                    return items

                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse Groq response as JSON: {e}")
                    raise LLMAPIError(f"Invalid JSON response from Groq: {content}")

        except (AuthenticationError, RateLimitError, LLMAPIError):
            raise
        except httpx.TimeoutException:
            logger.error("Groq API request timed out")
            raise LLMAPIError("Request to Groq API timed out")
        except Exception as e:
            logger.exception(f"Unexpected error calling Groq API: {e}")
            raise LLMAPIError(f"Unexpected error: {str(e)}")
