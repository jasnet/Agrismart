const client = require("../config/twilioConfig");

async function sendSMS(message) {
    await client.messages.create({
        body: message,
        from: process.env.TWILIO_PHONE,
        to: process.env.USER_PHONE
    });
}

module.exports = sendSMS;
