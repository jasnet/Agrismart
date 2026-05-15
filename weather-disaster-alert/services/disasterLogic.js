const config = require("../config/weatherConfig");

function checkDisaster(weather) {
    let alerts = [];

    if (weather.rain >= config.RAIN_THRESHOLD) {
        alerts.push("Heavy rainfall detected. Flood/Landslide risk.");
    }

    if (weather.wind >= config.WIND_THRESHOLD) {
        alerts.push("Strong wind detected. Cyclone risk.");
    }

    if (weather.temperature >= config.TEMP_THRESHOLD) {
        alerts.push("Extreme heat detected.");
    }

    return alerts;
}

module.exports = checkDisaster;
