import { useState, useEffect } from "react";
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

export default function VoiceRecorder() {
    const [manualInput, setManualInput] = useState("");

    const {
        transcript,
        listening,
        resetTranscript,
        browserSupportsSpeechRecognition,
        isMicrophoneAvailable
    } = useSpeechRecognition();

    // Send to backend when user stops speaking (listen logic)
    useEffect(() => {
        if (!listening && transcript) {
            localStorage.setItem("transcript", transcript);
            window.dispatchEvent(new Event("transcript-updated"));
            sendToBackend(transcript);
        }
    }, [listening, transcript]);

    async function sendToBackend(text) {
        try {
            const res = await fetch("http://127.0.0.1:5003/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: text })
            });
            const data = await res.json();
            localStorage.setItem("advice", data.answer);
            window.dispatchEvent(new Event("advice-updated"));
        } catch (err) {
            console.error(err);
            localStorage.setItem("advice", "Error calling backend. Ensure Flask is running on port 5003.");
            window.dispatchEvent(new Event("advice-updated"));
        }
    }

    const toggleListening = () => {
        if (!browserSupportsSpeechRecognition) {
            alert("Browser doesn't support speech recognition. Please use Chrome.");
            return;
        }

        if (listening) {
            SpeechRecognition.stopListening();
        } else {
            resetTranscript();
            // Requesting permission is handled by the browser when startListening is called
            SpeechRecognition.startListening({ continuous: false, language: 'en-IN' }).catch(e => {
                console.error("Speech Recognition Error:", e);
                alert("Microphone access denied. Please allow access in browser settings.");
            });
        }
    };

    if (!browserSupportsSpeechRecognition) {
        return (
            <div className="bg-[#14181f] rounded-xl p-6 flex flex-col items-center border border-red-500">
                <p className="text-red-500 font-bold mb-2">Browser Not Supported</p>
                <p className="text-gray-400 text-center text-sm mb-4">
                    Your browser does not support Speech Recognition.
                    <br />Please use <strong>Google Chrome</strong>.
                </p>

                {/* Manual Input Fallback */}
                <div className="w-full mt-2 border-t border-gray-700 pt-4">
                    <p className="text-sm text-gray-400 text-center mb-2">Type your question instead:</p>
                    <form
                        onSubmit={(e) => {
                            e.preventDefault();
                            const input = e.target.elements.manualQuery.value;
                            if (input.trim()) {
                                localStorage.setItem("transcript", input);
                                window.dispatchEvent(new Event("transcript-updated"));
                                sendToBackend(input);
                                e.target.elements.manualQuery.value = "";
                            }
                        }}
                        className="flex gap-2"
                    >
                        <input
                            name="manualQuery"
                            type="text"
                            placeholder="e.g., How to grow wheat?"
                            className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-green-500"
                        />
                        <button
                            type="submit"
                            className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 transition-colors"
                        >
                            Send
                        </button>
                    </form>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-[#14181f] rounded-xl p-6 flex flex-col items-center">
            <button
                onClick={toggleListening}
                className={`${listening ? "bg-red-500 animate-pulse" : "bg-green-500"
                    } w-28 h-28 rounded-full text-4xl flex items-center justify-center hover:scale-105 transition-transform shadow-lg shadow-green-500/20`}
            >
                {listening ? "🛑" : "🎤"}
            </button>
            <p className="text-center mt-4 text-gray-300 font-medium">
                {listening ? "Listening..." : "Tap to Speak"}
            </p>

            {/* Debug Info */}
            <div className="mt-4 text-xs text-gray-500 border border-gray-800 p-2 rounded w-full bg-black/20">
                <p className="font-bold text-gray-400 mb-1">Diagnose Info:</p>
                <div className="grid grid-cols-2 gap-x-2">
                    <span>• Mic Available:</span>
                    <span className={isMicrophoneAvailable ? "text-green-500" : "text-orange-500"}>
                        {isMicrophoneAvailable ? "Ready" : "Waiting for permission..."}
                    </span>

                    <span>• Listening:</span>
                    <span className={listening ? "text-green-500" : "text-gray-500"}>
                        {listening ? "Active" : "Idle"}
                    </span>
                </div>
            </div>

            <div className="w-full mt-6 border-t border-gray-700 pt-4">
                <p className="text-sm text-gray-400 text-center mb-2">Or type your question:</p>
                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        const input = e.target.elements.manualQuery.value;
                        if (input.trim()) {
                            // Manually triggering the same flow as voice
                            localStorage.setItem("transcript", input);
                            window.dispatchEvent(new Event("transcript-updated"));
                            sendToBackend(input);
                            e.target.elements.manualQuery.value = "";
                        }
                    }}
                    className="flex gap-2"
                >
                    <input
                        name="manualQuery"
                        type="text"
                        placeholder="e.g., How to grow wheat?"
                        className="flex-1 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-green-500"
                    />
                    <button
                        type="submit"
                        className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 transition-colors"
                    >
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
}
