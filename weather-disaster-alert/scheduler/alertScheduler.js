const cron = require("node-cron");

const getWeatherData = require("../services/weatherService");
const checkDisaster = require("../services/disasterLogic");
const sendSMS = require("../services/smsService");
const sendWhatsApp = require("../services/whatsappService");

// Store latest alerts in memory
let latestAlerts = [];

const runCheck = async () => {
    console.log("Checking weather conditions...");

    const weather = await getWeatherData();
    const rawAlerts = checkDisaster(weather);

    // Format for Frontend
    if (rawAlerts.length > 0) {
        const message =
            "⚠️ WEATHER & LAND ALERT\n\n" +
            rawAlerts.join("\n") +
            "\n\nStay safe.";

        // Send Notifications
        try {
            await sendSMS(message);
            console.log("SMS alert sent successfully");
        } catch (err) {
            console.error("❌ SMS Failed:", err.message);
        }

        try {
            await sendWhatsApp(message);
            console.log("WhatsApp alert sent successfully");
        } catch (err) {
            console.error("❌ WhatsApp Failed:", err.message);
        }


        // Update in-memory storage for API
        latestAlerts = rawAlerts.map((msg, index) => ({
            id: "live-" + Date.now() + "-" + index,
            type: "critical", // Assume critical for these disasters
            category: "Weather",
            title: msg,
            location: process.env.CITY || "Local User Area",
            time: "Just now",
            icon: "warning",
            details: {
                severity: "Critical",
                affectedArea: process.env.CITY || "Local",
                symptoms: "Detected via Live Weather API",
                recommendations: ["Seek shelter", "Monitor local news", "Secure crops"],
                estimatedImpact: "High risk of damage"
            }
        }));
    } else {
        console.log("No danger detected");
        latestAlerts = [];
    }
};

// Run immediately on startup
runCheck();

// Schedule for every 30 mins
cron.schedule("*/30 * * * *", runCheck);

module.exports = { getLatestAlerts: () => latestAlerts, runCheck };

