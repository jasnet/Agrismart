const mongoose = require("mongoose");

const RecordSchema = new mongoose.Schema({
    crop: String,
    temperature: Number,
    humidity: Number,
    rain: Number,
    irrigate: Boolean,
    waterRequired: Number,
    estimatedYield: Number,
    time: {
        type: Date,
        default: Date.now
    }
});

module.exports = mongoose.model("Record", RecordSchema);
