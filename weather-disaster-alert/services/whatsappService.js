const client = require("../config/twilioConfig");

async function sendWhatsApp(message) {
    // Check if WHATSAPP_FROM and TO are set, else log warning (or rely on mock if client is mock)
    if (!process.env.WHATSAPP_FROM || !process.env.WHATSAPP_TO) {
        console.warn("⚠️  WhatsApp config missing in .env. Skipping WhatsApp alert.");
        return;
    }

    await client.messages.create({
        body: message,
        from: process.env.WHATSAPP_FROM,
        to: process.env.WHATSAPP_TO
    });
}

module.exports = sendWhatsApp;
