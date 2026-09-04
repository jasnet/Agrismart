const mongoose = require("mongoose");

const mongoUri = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/irrigation_ml";
mongoose.connect(mongoUri, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log("MongoDB Connected"))
    .catch(err => console.log("MongoDB Connection Warning:", err.message));
