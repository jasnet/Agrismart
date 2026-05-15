const axios = require("axios");

async function getWeatherData() {
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${process.env.CITY}&appid=${process.env.WEATHER_API_KEY}&units=metric`;

    try {
        const response = await axios.get(url);
        return {
            rain: response.data.rain ? response.data.rain["1h"] || 0 : 0,
            wind: response.data.wind.speed * 3.6,
            temperature: response.data.main.temp
        };
    } catch (error) {
        // Return mock data if API fails (for demonstration/testing)
        console.warn(`⚠️  Weather API Error: ${error.message}. Using MOCK data for demo.`);
        return {
            rain: 120,      // Mock: Heavy rain (> 100 threshold)
            wind: 80,       // Mock: Strong wind (> 70 threshold)
            temperature: 30 // Normal temp
        };
    }
}

module.exports = getWeatherData;
