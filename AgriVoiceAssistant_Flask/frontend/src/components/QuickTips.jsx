export default function QuickTips() {
    return (
        <div className="bg-[#14181f] p-6 rounded-xl border border-gray-800 h-full">
            <h2 className="text-xl font-bold text-purple-400 mb-4">QUICK TIPS</h2>
            <ul className="text-gray-400 space-y-3">
                <li className="flex items-center gap-2">
                    <span className="text-green-500">➤</span> Ask Crops: "How to grow wheat"
                </li>
                <li className="flex items-center gap-2">
                    <span className="text-green-500">➤</span> Ask Soil: "Black soil crops"
                </li>
                <li className="flex items-center gap-2">
                    <span className="text-green-500">➤</span> Ask Disease: "Yellow leaves treatment"
                </li>
                <li className="flex items-center gap-2">
                    <span className="text-green-500">➤</span> Supported languages: English & Hindi
                </li>
            </ul>
        </div>
    );
}
