const { OpenAI } = require("openai");
const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function callOpenAI(payload, attempts = 3) {
  for (let i = 0; i < attempts; i++) {
    try {
      return await client.responses.create(payload);
    } catch (err) {
      const status = err?.status || err?.response?.status;
      const code = err?.code || err?.response?.data?.error?.code;
      // handle rate-limit / quota exhaustion
      if ((status === 429 || code === "insufficient_quota") && i < attempts - 1) {
        await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, i))); // exponential backoff
        continue;
      }
      // bubble up error so caller can surface an appropriate message
      throw err;
    }
  }
}
module.exports = { callOpenAI };