# Implementation Notes - VAMU AI Service

## Current Status: ✅ PRODUCTION READY

The "Where" inspiration feature is fully implemented and tested.

## Key Implementation Details

### Location Handling Logic

The service implements smart location handling to prioritize text query locations over coordinate-based bias:

**Priority Order:**
1. **Text query location** (e.g., "Pizza in Paris") - HIGHEST
2. **Provided coordinates** (latitude/longitude)
3. **IP-based location** (Google's fallback)

**How it works:**
- If text contains location keywords (" in ", " near ", " at ", " around "), we skip `locationBias` entirely
- This prevents conflicts where Google would use coordinates instead of the text location
- If no location in text but coordinates provided, we send them as `locationBias`
- If neither, Google uses IP-based geolocation

### Test Scenarios Verified

✅ **Scenario 1:** "Pizza night" + Milan coordinates → Milan results
✅ **Scenario 2:** "Pizza in Paris" + Milan coordinates → Paris results (text wins)
✅ **Scenario 3:** "Pizza night" + no coordinates → IP-based location results

### Google Places API Configuration

**Field Mask (Optimized for cost):**
- Essentials: place_id, name
- Pro: displayName, formattedAddress, location, types, photos, etc.
- Enterprise: rating, priceLevel, opening hours, contact info

**Default Parameters:**
- maxResultCount: 8 (user configurable via preferences)
- language: en-US
- rankPreference: RELEVANCE

## Known Limitations

1. **Location detection is keyword-based** - Only detects " in ", " near ", " at ", " around "
   - "Pizza Paris" (no keyword) won't trigger smart handling
   - Future: Could use NLP for better detection

2. **Google Places API behavior** - locationBias sometimes overrides text query despite documentation saying otherwise
   - Our workaround: Skip locationBias when location detected in text

3. **No geocoding** - We don't validate or convert city names to coordinates
   - Relies entirely on Google's text parsing

## Environment Variables

Required:
- `GOOGLE_PLACES_API_KEY` - Your Google Places API key
- All others have sensible defaults

See `.env.example` for full list.

## API Endpoint

**POST** `/api/v1/inspiration/where`

**Request:**
```json
{
  "what": "Pizza night in Milan",
  "location": {
    "latitude": 45.4642,
    "longitude": 9.1900
  },
  "preferences": {
    "max_results": 8,
    "min_rating": 4.0,
    "price_level": ["PRICE_LEVEL_MODERATE"],
    "open_now": true
  }
}
```

**Response:** Real venue data from Google Places with ratings, addresses, hours, etc.

## Next Steps

Future enhancements ready to implement:
- `/when` - Time suggestions
- `/what` - Event idea generation  
- `/who` - Attendee suggestions
- `/wishlist` - Items/rules suggestions
- Chatbot integration
- Redis caching
- Rate limiting

## Testing

**Local:**
```bash
docker-compose up
# Visit http://localhost:8001/docs
```

**Production:**
Update `ENVIRONMENT=production` and deploy container.

---
**Last Updated:** 2025-11-09
**Status:** Working and tested
