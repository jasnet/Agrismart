require("dotenv").config();
const express = require("express");
const cors = require("cors");
const { getLatestAlerts } = require("./scheduler/alertScheduler");

const app = express();
const PORT = process.env.PORT || 5001;

app.use(cors());
app.use(express.json());

// API Endpoint for Live Alerts
app.get("/api/alerts", (req, res) => {
    const alerts = getLatestAlerts();
    res.json(alerts);
});

const sendSMS = require("./services/smsService");

// API Endpoint to Manually Send Alert via SMS
app.post("/api/send-alert", async (req, res) => {
    const { message } = req.body;
    if (!message) {
        return res.status(400).json({ error: "Message is required" });
    }

    try {
        await sendSMS(message);
        res.json({ success: true, message: "SMS triggered successfully" });
    } catch (error) {
        console.error("Manual SMS Error:", error);
        res.status(500).json({ error: "Failed to send SMS" });
    }
});

app.listen(PORT, () => {
    console.log(`Weather & Disaster Alert System running on port ${PORT}`);
});
