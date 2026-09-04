export default function Navbar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: "overview", label: "Dashboard", icon: "📊" },
    { id: "soil", label: "Soil & Crop AI", icon: "🌱" },
    { id: "irrigation", label: "Smart Irrigation", icon: "💧" },
    { id: "weather", label: "Weather & Alerts", icon: "🌦️" },
    { id: "disease", label: "Leaf Disease Scanner", icon: "🔬" },
    { id: "voice", label: "Voice Assistant", icon: "🎙️" },
  ];

  return (
    <header className="bg-[#14181f]/90 backdrop-blur-md border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab("overview")}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-green-300 flex items-center justify-center text-xl shadow-lg shadow-emerald-500/20">
              🌾
            </div>
            <div>
              <span className="text-xl font-extrabold bg-gradient-to-r from-emerald-400 via-green-300 to-teal-200 bg-clip-text text-transparent">
                AgriSmart
              </span>
              <span className="block text-[10px] text-emerald-400 font-semibold tracking-wider uppercase">
                Precision Farming AI
              </span>
            </div>
          </div>

          <nav className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 shadow-sm"
                      : "text-gray-300 hover:text-white hover:bg-gray-800/60"
                  }`}
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-400 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="hidden sm:inline">Systems Online</span>
            </div>
          </div>
        </div>

        {/* Mobile Navigation bar */}
        <div className="flex md:hidden overflow-x-auto py-2 space-x-2 no-scrollbar border-t border-gray-800/60">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex-shrink-0 flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium ${
                activeTab === item.id
                  ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                  : "text-gray-400 bg-gray-900/60"
              }`}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
