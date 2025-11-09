# Quick Start Guide

## Step 1: Set Up Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Google Places API key
# Replace: your_google_places_api_key_here
# With your actual API key
```

## Step 2: Choose Your Method

### Option A: Docker (Recommended)

```bash
# Build and start the service
docker-compose up --build

# The service will be available at:
# - API: http://localhost:8001
# - Docs: http://localhost:8001/docs

# To stop:
docker-compose down
```

### Option B: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --reload --port 8001

# The service will be available at:
# - API: http://localhost:8001
# - Docs: http://localhost:8001/docs
```

## Step 3: Test the API

### Using Swagger UI (Easy)

1. Open http://localhost:8001/docs
2. Click on `POST /api/v1/inspiration/where`
3. Click "Try it out"
4. Use this example request:

```json
{
  "what": "Pizza restaurant in New York",
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "preferences": {
    "max_results": 5,
    "min_rating": 4.0,
    "open_now": false
  }
}
```

5. Click "Execute"
6. See the venue suggestions in the response!

### Using curl

```bash
curl -X POST "http://localhost:8001/api/v1/inspiration/where" \
  -H "Content-Type: application/json" \
  -d '{
    "what": "Pizza restaurant in New York",
    "location": {
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "preferences": {
      "max_results": 5,
      "min_rating": 4.0
    }
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8001/api/v1/inspiration/where",
    json={
        "what": "Pizza restaurant in New York",
        "location": {
            "latitude": 40.7128,
            "longitude": -74.0060
        },
        "preferences": {
            "max_results": 5,
            "min_rating": 4.0
        }
    }
)

venues = response.json()
print(f"Found {venues['total_count']} venues:")
for venue in venues['suggestions']:
    print(f"- {venue['display_name']} (Rating: {venue['rating']})")
```

## Expected Response

```json
{
  "suggestions": [
    {
      "place_id": "ChIJ...",
      "display_name": "Joe's Pizza",
      "address": "7 Carmine St, New York, NY 10014, USA",
      "location": {
        "latitude": 40.7305,
        "longitude": -74.0028
      },
      "rating": 4.5,
      "total_ratings": 1234,
      "price_level": "PRICE_LEVEL_INEXPENSIVE",
      "types": ["restaurant", "pizza_restaurant"],
      "phone": "+1 212-555-0100",
      "website": "https://joespizzanyc.com",
      "is_open_now": true,
      "google_maps_uri": "https://maps.google.com/?cid=..."
    }
  ],
  "total_count": 5,
  "query": "Pizza restaurant in New York"
}
```

## Troubleshooting

### Error: "Google Places API authentication failed"
- Check that your API key is correct in `.env`
- Ensure Google Places API is enabled in Google Cloud Console
- Verify billing is enabled for your Google Cloud project

### Error: "Module not found"
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Check you're in the correct directory

### Port 8001 already in use
- Change the port in `.env`: `PORT=8002`
- Or in docker-compose.yml: `"8002:8001"`

## Next Steps

1. **Integrate with NestJS Backend**
   - Call this service from your NestJS API
   - See README.md for integration examples

2. **Add More Features**
   - Implement `/when`, `/what`, `/who`, `/wishlist` endpoints
   - Add chatbot and agent features

3. **Deploy to Production**
   - Update environment variables
   - Use managed PostgreSQL/Redis
   - Set up proper monitoring

## Need Help?

- Check the full README.md
- Review the API docs at http://localhost:8001/docs
- Contact the VAMU development team
