const express = require("express");
const cors = require("cors");
require("./db");

const getWeather = require("./weather");
const mlDecision = require("./logic/decision");
const waterReq = require("./logic/water");
const estimateYield = require("./logic/yield");
const Record = require("./models/Record");

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static("../frontend"));

app.get("/api/run/:crop", async (req, res) => {
    try {
        const crop = req.params.crop;
        const weather = await getWeather();
        const irrigateDecision = await mlDecision(weather);
        const irrigate = Boolean(irrigateDecision);

        const water = waterReq(crop);
        const yieldEst = estimateYield(crop, irrigate);

        // Save to DB (Optional, requires MongoDB running)
        try {
            const record = new Record({
                crop,
                ...weather,
                irrigate,
                waterRequired: water,
                estimatedYield: yieldEst
            });
            await record.save();
        } catch (dbErr) {
            console.error("DB Save Error (Is MongoDB running?):", dbErr.message);
        }

        res.json({
            crop,
            ...weather,
            irrigate,
            waterRequired: water,
            estimatedYield: yieldEst
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

const PORT = process.env.PORT || 5002;
app.listen(PORT, () => console.log(`Smart Irrigation ML Server running on port ${PORT}`));
