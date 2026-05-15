import { useState, useEffect } from "react";
import ReactMarkdown from 'react-markdown';

export default function SmartAdvisoryBox() {
    const [advice, setAdvice] = useState(localStorage.getItem("advice") || "");

    useEffect(() => {
        const handleUpdate = () => {
            setAdvice(localStorage.getItem("advice") || "");
        };
        window.addEventListener("advice-updated", handleUpdate);
        return () => window.removeEventListener("advice-updated", handleUpdate);
    }, []);

    return (
        <div className="bg-[#14181f] p-6 rounded-xl mt-4 border border-gray-800 shadow-xl overflow-hidden relative group transition-all duration-300 hover:border-blue-500/50">


            <h2 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4 flex items-center gap-2">
                <span className="material-symbols-outlined text-blue-400">smart_toy</span>
                SMART ADVISORY
            </h2>

            <div className="text-gray-300 min-h-[4rem] text-sm leading-relaxed markdown-content">
                {advice ? (
                    <div className="formatted-response">
                        <ReactMarkdown
                            components={{
                                h1: ({ node, ...props }) => <h1 className="text-xl font-bold text-blue-300 mt-4 mb-2 border-b border-gray-700 pb-2" {...props} />,
                                h2: ({ node, ...props }) => <h2 className="text-lg font-semibold text-green-400 mt-4 mb-2" {...props} />,
                                h3: ({ node, ...props }) => <h3 className="text-md font-medium text-purple-300 mt-3 mb-1" {...props} />,
                                ul: ({ node, ...props }) => <ul className="list-disc list-inside space-y-1 my-2 text-gray-300" {...props} />,
                                ol: ({ node, ...props }) => <ol className="list-decimal list-inside space-y-1 my-2 text-gray-300" {...props} />,
                                li: ({ node, ...props }) => <li className="ml-2" {...props} />,
                                strong: ({ node, ...props }) => <strong className="text-white font-bold" {...props} />,
                                p: ({ node, ...props }) => <p className="mb-2" {...props} />,
                            }}
                        >
                            {advice}
                        </ReactMarkdown>
                    </div>
                ) : (
                    <div className="flex flex-col items-center justify-center py-8 text-gray-500 italic animate-pulse">
                        <span>Waiting for your question...</span>
                    </div>
                )}
            </div>
        </div>
    );
}
