from datetime import date
from typing import List
from .utils import get_crop_kc, effective_rainfall, mm_to_liters, volume_to_duration_minutes, SOIL_ADJUSTMENT, SOIL_MOISTURE_THRESH
from .weather import fetch_weather_for_location

async def schedule_for_field(field: dict, days: int = 7, lat: float | None = None, lon: float | None = None):
    """
    field: dict containing keys matching Field model (area_m2, soil_type, crop_type, crop_stage, irrigation_method)
    Returns: list of schedule entries suitable to insert into DB or return via API
    """
    area = field.get("area_m2")
    soil = field.get("soil_type", "loamy").lower()
    crop = field.get("crop_type", "vegetables").lower()
    stage = field.get("crop_stage", "vegetative").lower()
    irrigation_method = field.get("irrigation_method", "sprinkler").lower()
    measured_sm = field.get("soil_moisture_pct", None)

    kc = get_crop_kc(crop, stage)
    soil_adj = SOIL_ADJUSTMENT.get(soil, 1.0)
    sm_threshold = SOIL_MOISTURE_THRESH.get(soil, 30)

    weather = await fetch_weather_for_location(lat, lon, days=days)
    result = []
    for w in weather:
        d = w["date"]
        rain = w.get("rainfall_mm", 0.0)
        et0 = w.get("et0_mm", 0.0)
        eff_rain = effective_rainfall(rain)
        water_needed_mm = max(0.0, (et0 * kc) - eff_rain) * soil_adj
        skip_due_sm = False
        if measured_sm is not None and measured_sm >= sm_threshold:
            skip_due_sm = True
        volume = mm_to_liters(area, water_needed_mm)
        duration_min = volume_to_duration_minutes(volume, irrigation_method, area)
        entry = {
            "field_id": field.get("id"),
            "date": d,
            "water_mm": round(water_needed_mm, 3),
            "volume_liters": round(volume, 2),
            "duration_min": round(duration_min, 2),
            "status": "skipped" if skip_due_sm or water_needed_mm <= 0.01 else "scheduled",
        }
        result.append(entry)
    return result