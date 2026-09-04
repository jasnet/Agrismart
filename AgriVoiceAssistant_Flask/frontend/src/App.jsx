import { useState } from "react";
import Navbar from "./components/Navbar";
import DashboardOverview from "./components/DashboardOverview";
import SoilCropIntelligence from "./components/SoilCropIntelligence";
import SmartIrrigationPanel from "./components/SmartIrrigationPanel";
import WeatherDisasterPanel from "./components/WeatherDisasterPanel";
import PlantDiseaseScanner from "./components/PlantDiseaseScanner";
import VoiceRecorder from "./components/VoiceRecorder";
import TranscriptBox from "./components/TranscriptBox";
import SmartAdvisoryBox from "./components/SmartAdvisoryBox";
import QuickTips from "./components/QuickTips";

export default function App() {
  const [activeTab, setActiveTab] = useState("overview");
  const [language, setLanguage] = useState("English (India)");

  return (
    <div className="min-h-screen bg-[#0e1117] text-white flex flex-col">
      {/* Top Navigation */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === "overview" && (
          <DashboardOverview setActiveTab={setActiveTab} />
        )}

        {activeTab === "soil" && <SoilCropIntelligence />}

        {activeTab === "irrigation" && <SmartIrrigationPanel />}

        {activeTab === "weather" && <WeatherDisasterPanel />}

        {activeTab === "disease" && <PlantDiseaseScanner />}

        {activeTab === "voice" && (
          <div className="space-y-6">
            <div className="border-b border-gray-800 pb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              <div>
                <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                  <span>🎙️ AI Agricultural Voice Assistant</span>
                </h1>
                <p className="text-gray-400 text-sm mt-1">
                  Tap the microphone or type to ask about crop health, fertilizers, diseases, and market advice.
                </p>
              </div>

              <div className="flex items-center space-x-2">
                <span className="text-xs text-gray-400 font-medium">Language:</span>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="bg-gray-900 border border-gray-700 text-white text-xs rounded-lg px-3 py-1.5 focus:border-emerald-500 focus:outline-none"
                >
                  <option value="English (India)">English (India)</option>
                  <option value="Hindi">हिंदी (Hindi)</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
              <div className="lg:col-span-4">
                <VoiceRecorder language={language} />
              </div>
              <div className="lg:col-span-5 space-y-4">
                <TranscriptBox />
                <SmartAdvisoryBox />
              </div>
              <div className="lg:col-span-3">
                <QuickTips />
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Global Footer */}
      <footer className="border-t border-gray-800/80 py-6 bg-[#14181f]/40 text-center text-xs text-gray-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-2">
          <span>🌾 AgriSmart — AI Precision Agriculture Platform</span>
          <span>FastAPI • Express • React • Vite • Tailwind • TensorFlow</span>
        </div>
      </footer>
    </div>
  );
}
