# Shared constants for scheduling logic
CROP_KC = {
    "wheat": {"sowing": 0.7, "vegetative": 1.05, "flowering": 1.15, "maturity": 0.6},
    "rice": {"sowing": 0.9, "vegetative": 1.2, "flowering": 1.25, "maturity": 0.8},
    "maize": {"sowing": 0.6, "vegetative": 1.05, "flowering": 1.15, "maturity": 0.7},
    "vegetables": {"sowing": 0.7, "vegetative": 1.0, "flowering": 1.05, "maturity": 0.6},
    "pulses": {"sowing": 0.5, "vegetative": 0.9, "flowering": 1.0, "maturity": 0.5},
}

SOIL_ADJUSTMENT = {"sandy": 1.15, "loamy": 1.0, "clay": 0.9}
IRRIGATION_FLOW = {"drip": 8, "sprinkler": 60, "flood": 200}
SOIL_MOISTURE_THRESH = {"sandy": 25, "loamy": 30, "clay": 35}

from datetime import date


def get_crop_kc(crop: str, stage: str) -> float:
    crop = crop.lower()
    stage = stage.lower()
    if crop in CROP_KC and stage in CROP_KC[crop]:
        return CROP_KC[crop][stage]
    return 1.0


def effective_rainfall(rain_mm: float) -> float:
    if rain_mm <= 5:
        return rain_mm * 0.8
    return rain_mm * 0.6


def mm_to_liters(area_m2: float, depth_mm: float) -> float:
    return depth_mm * area_m2


def volume_to_duration_minutes(volume_liters: float, irrigation_method: str, area_m2: float) -> float:
    flow_per_min = IRRIGATION_FLOW.get(irrigation_method, 50) * (area_m2 / 100.0)
    if flow_per_min <= 0:
        return 0.0
    return volume_liters / flow_per_min