"""Custom exceptions for the application."""


class VAMUAIException(Exception):
    """Base exception for VAMU AI Service."""
    pass


class GooglePlacesAPIError(VAMUAIException):
    """Raised when Google Places API returns an error."""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class RateLimitError(GooglePlacesAPIError):
    """Raised when API rate limit is exceeded."""
    pass


class AuthenticationError(GooglePlacesAPIError):
    """Raised when API authentication fails."""
    pass


class ValidationError(VAMUAIException):
    """Raised when request validation fails."""
    pass


class LLMAPIError(VAMUAIException):
    """Raised when LLM API (like Groq) returns an error."""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
