const twilio = require("twilio");

let client;

if (process.env.TWILIO_SID && process.env.TWILIO_SID.startsWith("AC")) {
    client = twilio(process.env.TWILIO_SID, process.env.TWILIO_AUTH);
} else {
    console.log("⚠️  Twilio SID invalid or missing. Using MOCK SMS client.");
    client = {
        messages: {
            create: async (data) => {
                console.log("\n[MOCK SMS SENDING]");
                console.log(`To: ${data.to}`);
                console.log(`From: ${data.from}`);
                console.log(`Body: ${data.body}\n`);
                return Promise.resolve({ sid: "SM_MOCK_" + Date.now() });
            }
        }
    };
}

module.exports = client;
