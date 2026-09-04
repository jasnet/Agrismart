import { useState } from "react";

export default function SmartIrrigationPanel() {
  const [selectedCrop, setSelectedCrop] = useState("wheat");
  const [soilMoisture, setSoilMoisture] = useState(48); // %
  const [valveStatus, setValveStatus] = useState("Standby");
  const [isAutomated, setIsAutomated] = useState(true);

  const cropWaterData = {
    wheat: { dailyReq: "4.5 mm/day", cycle: "Every 4 days", optimalMoisture: "50-70%", status: "Good" },
    rice: { dailyReq: "8.0 mm/day", cycle: "Continuous flood (2-5cm)", optimalMoisture: "80-100%", status: "Needs Water" },
    maize: { dailyReq: "5.2 mm/day", cycle: "Every 3 days", optimalMoisture: "55-65%", status: "Optimal" },
    sugarcane: { dailyReq: "7.1 mm/day", cycle: "Every 5 days", optimalMoisture: "65-75%", status: "Optimal" },
    cotton: { dailyReq: "5.8 mm/day", cycle: "Every 4 days", optimalMoisture: "50-60%", status: "Optimal" }
  };

  const handleTriggerValve = () => {
    if (valveStatus === "Irrigating") {
      setValveStatus("Standby");
    } else {
      setValveStatus("Irrigating");
      setSoilMoisture((prev) => Math.min(prev + 15, 85));
    }
  };

  const current = cropWaterData[selectedCrop];

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-800 pb-4 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <span>💧 Smart Irrigation Command Center</span>
          </h2>
          <p className="text-gray-400 text-sm mt-1">
            Automated sensor monitoring, evapotranspiration balance, and valve automation.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400">Automation Mode:</span>
          <button
            onClick={() => setIsAutomated(!isAutomated)}
            className={`px-3 py-1 rounded-full text-xs font-bold transition-colors ${
              isAutomated ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30" : "bg-gray-800 text-gray-400"
            }`}
          >
            {isAutomated ? "ENABLED (AI Controlled)" : "MANUAL OVERRIDE"}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Soil Moisture Gauge */}
        <div className="bg-[#14181f] border border-gray-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs text-gray-400 font-semibold uppercase">
              <span>Live Soil Moisture</span>
              <span className="text-blue-400">Sensor #A-102</span>
            </div>
            <div className="mt-4 flex items-baseline gap-2">
              <span className="text-4xl font-black text-white">{soilMoisture}%</span>
              <span className="text-xs text-cyan-400 font-medium">Volumetric Water Content</span>
            </div>
            {/* Progress bar */}
            <div className="w-full bg-gray-800 h-3 rounded-full mt-4 overflow-hidden">
              <div
                className={`h-full transition-all duration-500 rounded-full ${
                  soilMoisture < 45 ? "bg-amber-500" : soilMoisture > 75 ? "bg-cyan-400" : "bg-emerald-500"
                }`}
                style={{ width: `${soilMoisture}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-400 mt-2">
              {soilMoisture < 45 ? "⚠️ Moisture dropped below threshold. Valve triggered." : "Moisture is within target range for chosen crop."}
            </p>
          </div>

          <div className="mt-6 pt-4 border-t border-gray-800 flex justify-between items-center">
            <span className="text-xs text-gray-400">Valve State:</span>
            <span className={`text-xs font-bold px-2 py-0.5 rounded ${valveStatus === "Irrigating" ? "bg-blue-500/20 text-blue-400 animate-pulse" : "bg-gray-800 text-gray-300"}`}>
              {valveStatus}
            </span>
          </div>
        </div>

        {/* Crop Water Requirement */}
        <div className="bg-[#14181f] border border-gray-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs text-gray-400 font-semibold uppercase">
              <span>Target Crop Dynamics</span>
              <span>ET-ML Model</span>
            </div>
            <div className="mt-3">
              <label className="text-xs text-gray-400 block mb-1">Select Field Crop:</label>
              <select
                value={selectedCrop}
                onChange={(e) => setSelectedCrop(e.target.value)}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white text-sm focus:border-blue-500 focus:outline-none capitalize"
              >
                <option value="wheat">Wheat</option>
                <option value="rice">Rice</option>
                <option value="maize">Maize</option>
                <option value="sugarcane">Sugarcane</option>
                <option value="cotton">Cotton</option>
              </select>
            </div>

            <div className="mt-4 space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-gray-800">
                <span className="text-gray-400">Water Consumption:</span>
                <span className="font-bold text-white">{current.dailyReq}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-gray-800">
                <span className="text-gray-400">Irrigation Interval:</span>
                <span className="font-bold text-white">{current.cycle}</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-gray-400">Optimal Moisture:</span>
                <span className="font-bold text-cyan-400">{current.optimalMoisture}</span>
              </div>
            </div>
          </div>

          <button
            onClick={handleTriggerValve}
            className={`w-full py-2.5 px-4 rounded-xl text-xs font-bold transition-colors mt-4 ${
              valveStatus === "Irrigating"
                ? "bg-red-500/20 text-red-400 border border-red-500/40 hover:bg-red-500/30"
                : "bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20"
            }`}
          >
            {valveStatus === "Irrigating" ? "Stop Active Irrigation 🛑" : "Activate Main Irrigation Valve 💧"}
          </button>
        </div>

        {/* Active Schedule Overview */}
        <div className="bg-[#14181f] border border-gray-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
          <div>
            <div className="text-xs text-gray-400 font-semibold uppercase mb-3">
              Automated Schedule
            </div>
            <div className="space-y-3">
              <div className="p-3 bg-gray-900/60 rounded-xl border border-gray-800">
                <div className="flex justify-between text-xs font-bold text-white">
                  <span>Field Sector A (North)</span>
                  <span className="text-emerald-400">06:00 AM</span>
                </div>
                <span className="text-[11px] text-gray-400">Duration: 45 mins • Drip Method</span>
              </div>
              <div className="p-3 bg-gray-900/60 rounded-xl border border-gray-800">
                <div className="flex justify-between text-xs font-bold text-white">
                  <span>Field Sector B (South)</span>
                  <span className="text-cyan-400">06:45 PM</span>
                </div>
                <span className="text-[11px] text-gray-400">Duration: 30 mins • Sprinkler</span>
              </div>
              <div className="p-3 bg-gray-900/60 rounded-xl border border-gray-800">
                <div className="flex justify-between text-xs font-bold text-white">
                  <span>Field Sector C (Nursery)</span>
                  <span className="text-purple-400">08:00 AM</span>
                </div>
                <span className="text-[11px] text-gray-400">Duration: 20 mins • Micro-misting</span>
              </div>
            </div>
          </div>
          <div className="text-[11px] text-gray-500 mt-4 text-center">
            Synced with SQLite & FastAPI Scheduler
          </div>
        </div>
      </div>
    </div>
  );
}
