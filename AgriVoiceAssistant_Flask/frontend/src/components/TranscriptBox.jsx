import { useState, useEffect } from "react";

export default function TranscriptBox() {
    const [transcript, setTranscript] = useState(localStorage.getItem("transcript") || "");

    useEffect(() => {
        const handleUpdate = () => {
            setTranscript(localStorage.getItem("transcript") || "");
        };
        window.addEventListener("transcript-updated", handleUpdate);
        return () => window.removeEventListener("transcript-updated", handleUpdate);
    }, []);

    return (
        <div className="bg-[#14181f] p-4 rounded-xl mt-4 border border-gray-800">
            <h2 className="text-lg font-bold text-green-400 mb-2">TRANSCRIPT</h2>
            <p className="text-gray-300 min-h-[3rem] italic">
                {transcript || "Your question will appear here..."}
            </p>
        </div>
    );
}
