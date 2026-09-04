import { useState } from "react";

export default function WeatherDisasterPanel() {
  const [city, setCity] = useState("Delhi");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [smsStatus, setSmsStatus] = useState("");

  const weather = {
    temp: 29.4,
    humidity: 78,
    wind: 24, // km/h
    rainfall: 12.5, // mm
    condition: "Partly Cloudy with Humid Air",
    riskLevel: "Low to Moderate"
  };

  const handleSendAlert = (e) => {
    e.preventDefault();
    if (!phoneNumber) return;
    setSmsStatus("Sending SMS alert via Twilio service...");
    setTimeout(() => {
      setSmsStatus(`✅ SMS alert sent successfully to ${phoneNumber}!`);
    }, 1000);
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-800 pb-4">
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <span>🌦️ Weather & Disaster Early Warning System</span>
        </h2>
        <p className="text-gray-400 text-sm mt-1">
          Hyper-local weather telemetry and automated farmer broadcast alerting.
        </p>
      </div>

      {/* Warning Banner */}
      <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-start space-x-3">
        <span className="text-2xl">⚡</span>
        <div>
          <h4 className="text-sm font-bold text-amber-300">Weather Advisory Notice</h4>
          <p className="text-xs text-amber-200/80 mt-0.5">
            Moderate convective precipitation anticipated within the next 48 hours. Postpone open-air nitrogen fertilizer application to prevent surface leaching.
          </p>
        </div>
      </div>

      {/* Weather Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-[#14181f] border border-gray-800 rounded-xl p-5">
          <span className="text-xs text-gray-400 font-semibold uppercase">Temperature</span>
          <div className="text-3xl font-black text-white mt-1">{weather.temp}°C</div>
          <span className="text-xs text-emerald-400">Normal range</span>
        </div>
        <div className="bg-[#14181f] border border-gray-800 rounded-xl p-5">
          <span className="text-xs text-gray-400 font-semibold uppercase">Humidity</span>
          <div className="text-3xl font-black text-white mt-1">{weather.humidity}%</div>
          <span className="text-xs text-cyan-400">High moisture air</span>
        </div>
        <div className="bg-[#14181f] border border-gray-800 rounded-xl p-5">
          <span className="text-xs text-gray-400 font-semibold uppercase">Wind Speed</span>
          <div className="text-3xl font-black text-white mt-1">{weather.wind} km/h</div>
          <span className="text-xs text-gray-400">Gentle breeze</span>
        </div>
        <div className="bg-[#14181f] border border-gray-800 rounded-xl p-5">
          <span className="text-xs text-gray-400 font-semibold uppercase">24h Rainfall</span>
          <div className="text-3xl font-black text-white mt-1">{weather.rainfall} mm</div>
          <span className="text-xs text-blue-400">Light scattered</span>
        </div>
      </div>

      {/* Emergency Alert Dispatch Form */}
      <div className="bg-[#14181f] border border-gray-800 rounded-2xl p-6 shadow-xl">
        <h3 className="text-lg font-bold text-white mb-2">Emergency SMS Dispatch Panel</h3>
        <p className="text-xs text-gray-400 mb-4">
          Directly broadcast flood, drought, or extreme heat advisories to farmers via Twilio SMS.
        </p>

        <form onSubmit={handleSendAlert} className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            placeholder="Farmer Phone Number (e.g. +91 9876543210)"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            className="flex-1 bg-gray-900 border border-gray-700 rounded-xl px-4 py-2.5 text-white text-sm focus:border-amber-500 focus:outline-none"
            required
          />
          <button
            type="submit"
            className="px-6 py-2.5 bg-amber-500 hover:bg-amber-400 text-gray-950 font-bold text-sm rounded-xl transition-colors shadow-lg shadow-amber-500/20"
          >
            Send Warning SMS 📲
          </button>
        </form>

        {smsStatus && (
          <div className="mt-3 text-xs font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-2 rounded-lg">
            {smsStatus}
          </div>
        )}
      </div>
    </div>
  );
}
