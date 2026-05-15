import { useState } from "react";
import VoiceRecorder from "./components/VoiceRecorder";
import TranscriptBox from "./components/TranscriptBox";
import SmartAdvisoryBox from "./components/SmartAdvisoryBox";
import QuickTips from "./components/QuickTips";

export default function App() {
    const [language, setLanguage] = useState("English (India)");

    return (
        <div className="min-h-screen bg-[#0e1117] text-white p-8">
            <h1 className="text-4xl font-bold">How can we help today?</h1>
            <p className="text-gray-400 mt-2">Select your language & tap the microphone to ask about agriculture.</p>

            <div className="grid grid-cols-3 gap-6 mt-8">
                <div className="col-span-1">
                    <VoiceRecorder language={language} />
                </div>
                <div className="col-span-1">
                    <TranscriptBox />
                    <SmartAdvisoryBox />
                </div>
                <div className="col-span-1">
                    <QuickTips />
                </div>
            </div>
        </div>
    );
}
