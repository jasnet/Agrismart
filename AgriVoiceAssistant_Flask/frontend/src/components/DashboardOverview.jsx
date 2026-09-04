export default function DashboardOverview({ setActiveTab }) {
  const cards = [
    {
      tab: "soil",
      title: "Soil Fertility & Crop Intelligence",
      description: "Analyze Nitrogen, Phosphorus, Potassium & soil pH to predict optimal crop yields and fertilizer formulas.",
      icon: "🌱",
      badge: "FastAPI + ML",
      gradient: "from-emerald-500/20 to-green-500/5",
      border: "border-emerald-500/30",
      accent: "text-emerald-400"
    },
    {
      tab: "irrigation",
      title: "Smart Irrigation & Scheduling",
      description: "Automated moisture monitoring, water volume estimation, and dynamic field valve scheduling.",
      icon: "💧",
      badge: "Express + SQLite",
      gradient: "from-blue-500/20 to-cyan-500/5",
      border: "border-blue-500/30",
      accent: "text-blue-400"
    },
    {
      tab: "weather",
      title: "Weather & Disaster Early Warning",
      description: "Live rainfall, temperature, wind metrics and instant SMS emergency notifications via Twilio.",
      icon: "🌦️",
      badge: "OpenWeather + Twilio",
      gradient: "from-amber-500/20 to-orange-500/5",
      border: "border-amber-500/30",
      accent: "text-amber-400"
    },
    {
      tab: "disease",
      title: "Leaf Disease Diagnostic",
      description: "Deep learning computer vision for detecting plant pathogens, fungal infections, and treatment regimens.",
      icon: "🔬",
      badge: "TensorFlow Vision",
      gradient: "from-purple-500/20 to-pink-500/5",
      border: "border-purple-500/30",
      accent: "text-purple-400"
    },
    {
      tab: "voice",
      title: "AI Voice Agricultural Advisor",
      description: "Ask farming questions in English or Hindi using speech recognition powered by Gemini 2.0 & OpenAI.",
      icon: "🎙️",
      badge: "Gemini AI + WebSpeech",
      gradient: "from-teal-500/20 to-emerald-500/5",
      border: "border-teal-500/30",
      accent: "text-teal-400"
    }
  ];

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-emerald-900/40 via-gray-900 to-teal-900/40 border border-emerald-500/20 p-8 shadow-2xl">
        <div className="relative z-10 max-w-3xl">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-400/10 text-emerald-300 border border-emerald-400/20 mb-3">
            🌾 Precision Agriculture Dashboard v2.0
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Welcome to AgriSmart Central
          </h1>
          <p className="mt-3 text-gray-300 text-base leading-relaxed">
            Your unified artificial intelligence command center for soil analysis, intelligent irrigation schedules, real-time climate monitoring, and voice advisory.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <button
              onClick={() => setActiveTab("soil")}
              className="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-bold text-sm transition-colors shadow-lg shadow-emerald-500/20"
            >
              Analyze Soil Parameters →
            </button>
            <button
              onClick={() => setActiveTab("voice")}
              className="px-5 py-2.5 rounded-xl bg-gray-800 hover:bg-gray-700 text-white font-semibold text-sm transition-colors border border-gray-700"
            >
              🎙️ Talk with Agri Assistant
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#14181f] border border-gray-800 rounded-xl p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Monitored Crops</span>
            <span className="text-emerald-400 text-lg">🌾</span>
          </div>
          <div className="mt-2 text-2xl font-black text-white">22 Types</div>
          <span className="text-xs text-emerald-400 font-medium">Rice, Wheat, Cotton, Maize...</span>
        </div>

        <div className="bg-[#14181f] border border-gray-800 rounded-xl p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Field Moisture</span>
            <span className="text-blue-400 text-lg">💧</span>
          </div>
          <div className="mt-2 text-2xl font-black text-white">68%</div>
          <span className="text-xs text-cyan-400 font-medium">Optimal range maintained</span>
        </div>

        <div className="bg-[#14181f] border border-gray-800 rounded-xl p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Weather Risk</span>
            <span className="text-amber-400 text-lg">⚠️</span>
          </div>
          <div className="mt-2 text-2xl font-black text-emerald-400">Normal</div>
          <span className="text-xs text-gray-400 font-medium">No severe rainfall alerts</span>
        </div>

        <div className="bg-[#14181f] border border-gray-800 rounded-xl p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">AI Accuracy</span>
            <span className="text-purple-400 text-lg">🎯</span>
          </div>
          <div className="mt-2 text-2xl font-black text-white">99.2%</div>
          <span className="text-xs text-purple-400 font-medium">Random Forest Classifier</span>
        </div>
      </div>

      {/* Feature Modules Grid */}
      <div>
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <span>AgriSmart Modules & Microservices</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {cards.map((card) => (
            <div
              key={card.tab}
              onClick={() => setActiveTab(card.tab)}
              className={`bg-gradient-to-b ${card.gradient} bg-[#14181f] border ${card.border} rounded-2xl p-6 hover:translate-y-[-2px] transition-all cursor-pointer group shadow-xl flex flex-col justify-between`}
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="text-3xl p-2 rounded-xl bg-gray-900/60 border border-gray-800">
                    {card.icon}
                  </div>
                  <span className="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-gray-900/80 border border-gray-700 text-gray-300">
                    {card.badge}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-white group-hover:text-emerald-300 transition-colors">
                  {card.title}
                </h3>
                <p className="mt-2 text-sm text-gray-400 leading-relaxed">
                  {card.description}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-gray-800/80 flex items-center justify-between">
                <span className={`text-xs font-bold ${card.accent}`}>Launch Tool →</span>
                <span className="text-gray-500 text-xs">Active</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
