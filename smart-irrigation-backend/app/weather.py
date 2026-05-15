from .config import settings

async def fetch_weather_for_location(lat: float, lon: float, days: int = 7):
    """
    Placeholder. If you add an API key, implement call to OpenWeatherMap or other provider.
    Return list of dicts with keys: date (date), rainfall_mm (float), et0_mm (float)
    """
    # Simple stub: return DEFAULT_ET0 and no rain
    from datetime import date, timedelta
    results = []
    for i in range(days):
        results.append({"date": date.today() + timedelta(days=i), "rainfall_mm": 0.0, "et0_mm": settings.DEFAULT_ET0})
    return results