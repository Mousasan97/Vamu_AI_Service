# VAMU AI Service

Python-based AI microservice for the VAMU platform providing intelligent features including venue suggestions, chatbot, and AI agents.

## Features

### Current
- **Where Inspiration** - AI-powered venue suggestions using Google Places API
- **Wishlist Inspiration** - Event items suggestions using Groq LLM

### Planned
- **When Inspiration** - Suggest optimal times for events
- **What Inspiration** - Event idea generation
- **Who Inspiration** - Attendee suggestions
- **Chatbot** - Conversational AI for event planning
- **AI Agent** - Autonomous event planning assistant

## Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Architecture**: Feature-Based Clean Architecture
- **APIs**: Google Places API, Groq LLM API
- **Deployment**: Docker containers

## Project Structure

```
vamu_ai_service/
├── app/
│   ├── main.py                      # FastAPI application
│   ├── config.py                    # Configuration management
│   ├── features/
│   │   └── inspiration/
│   │       ├── domain/              # Business entities
│   │       ├── application/         # Use cases
│   │       ├── infrastructure/      # External services
│   │       └── presentation/        # API routes
│   └── shared/
│       └── exceptions.py            # Custom exceptions
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Google Places API Key
- Groq API Key

### Installation

1. **Clone the repository**
   ```bash
   cd vamu_ai_service
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Add your Google Places API key**
   Edit `.env` and replace `your_google_places_api_key_here` with your actual API key

### Running Locally (Without Docker)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the service**
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

3. **Access the API**
   - API: http://localhost:8001
   - Swagger Docs: http://localhost:8001/docs
   - ReDoc: http://localhost:8001/redoc

### Running with Docker

1. **Build and run**
   ```bash
   docker-compose up --build
   ```

2. **Access the API**
   - API: http://localhost:8001
   - Swagger Docs: http://localhost:8001/docs

3. **Stop the service**
   ```bash
   docker-compose down
   ```

## API Endpoints

### Inspiration - Where

**POST** `/api/v1/inspiration/where`

Suggests venues for an event based on the event description.

**Request:**
```json
{
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
    "open_now": true
  }
}
```

**Response:**
```json
{
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
      "types": ["restaurant", "pizza_restaurant"],
      "phone": "+39 02 ...",
      "website": "https://...",
      "is_open_now": true,
      "google_maps_uri": "https://maps.google.com/?cid=..."
    }
  ],
  "total_count": 5,
  "query": "pizza restaurant Milan"
}
```

### Inspiration - Wishlist

**POST** `/api/v1/inspiration/wishlist`

Suggests items needed for an event using AI.

**Request:**
```json
{
  "event_name": "BBQ party",
  "max_items": 10
}
```

**Response:**
```json
{
  "event_name": "BBQ party",
  "items_needed": [
    "meat (steaks, burgers, sausages)",
    "BBQ sauce",
    "seasonings (salt, pepper, herbs)",
    "vegetables (bell peppers, onions, mushrooms)",
    "buns or bread",
    "salad or sides",
    "chips or snacks",
    "drinks (soft drinks, beer, water)",
    "utensils (tongs, forks, knives)",
    "plates and napkins"
  ],
  "total_items": 10
}
```

### Health Check

**GET** `/health`

Returns service health status.

## Integration with NestJS Backend

The Python AI service is called from the NestJS backend:

```typescript
// NestJS - Call Python AI Service
const response = await axios.post('http://python-ai-service:8001/api/v1/inspiration/where', {
  what: 'Pizza night in Milan',
  location: { latitude: 45.4642, longitude: 9.1900 },
  preferences: { max_results: 8, min_rating: 4.0 }
});

const venues = response.data.suggestions;
```

## Development

### Code Formatting
```bash
black app/
```

### Linting
```bash
ruff app/
```

### Testing
```bash
pytest tests/
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_PLACES_API_KEY` | Google Places API key | Required |
| `GROQ_API_KEY` | Groq API key for LLM features | Required |
| `ENVIRONMENT` | Environment (development/production) | development |
| `PORT` | Service port | 8001 |
| `BACKEND_API_URL` | NestJS backend URL | http://localhost:3000 |
| `LOG_LEVEL` | Logging level | INFO |

## Architecture

### Clean Architecture Layers

1. **Domain** - Core business entities (Venue, Location, SearchParams)
2. **Application** - Use cases and business logic
3. **Infrastructure** - External services (Google Places API)
4. **Presentation** - FastAPI routes and schemas

### Benefits

- ✅ Clear separation of concerns
- ✅ Easy to test
- ✅ Independent of frameworks
- ✅ Scalable and maintainable
- ✅ Easy to add new features

## Future Enhancements

- [ ] Add caching with Redis
- [ ] Implement other inspiration fields (when, what, who)
- [ ] Add chatbot feature with OpenAI/Anthropic
- [ ] Implement AI agent capabilities
- [ ] Add rate limiting
- [ ] Add authentication/authorization
- [ ] Implement async queue processing
- [ ] Add monitoring and metrics

## License

Proprietary - VAMU Platform

## Support

For issues and questions, contact the VAMU development team.
