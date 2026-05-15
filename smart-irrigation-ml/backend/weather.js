const axios = require("axios");

const API_KEY = "bd5e378503939ddaee76f12ad7a97608"; // Using a placeholder, user might need to replace
const CITY = "Dehradun";

async function getWeather() {
    try {
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${CITY}&appid=${API_KEY}&units=metric`;
        const res = await axios.get(url);

        return {
            temperature: res.data.main.temp,
            humidity: res.data.main.humidity,
            rain: res.data.rain ? 1 : 0
        };
    } catch (error) {
        console.error("Weather API Error, using mock data:", error.message);
        return { temperature: 28, humidity: 60, rain: 0 };
    }
}

module.exports = getWeather;
