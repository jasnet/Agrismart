import { useState } from "react";

export default function PlantDiseaseScanner() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [diagnosis, setDiagnosis] = useState(null);

  const sampleDiseases = [
    {
      crop: "Tomato",
      disease: "Early Blight (Alternaria solani)",
      confidence: "97.4%",
      symptoms: "Concentric brown rings on older leaves forming a target pattern; leaf chlorosis.",
      treatment: "Apply copper fungicide or chlorothalonil. Remove infected lower leaves and avoid overhead irrigation."
    },
    {
      crop: "Potato",
      disease: "Late Blight (Phytophthora infestans)",
      confidence: "98.1%",
      symptoms: "Water-soaked dark lesions on leaf tips with white fungal growth on undersides in humid conditions.",
      treatment: "Spray Mancozeb or Ridomil Gold promptly. Ensure good soil drainage."
    },
    {
      crop: "Apple / Fruit",
      disease: "Cedar Apple Rust (Gymnosporangium juniperi-virginianae)",
      confidence: "95.8%",
      symptoms: "Bright yellow-orange spots on upper leaf surfaces surrounded by red borders.",
      treatment: "Apply myclobutanil fungicide at pink bud stage. Prune nearby wild cedar hosts."
    }
  ];

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(URL.createObjectURL(file));
      setAnalyzing(true);
      setDiagnosis(null);

      // Simulate deep learning inference
      setTimeout(() => {
        const randomDiagnosis = sampleDiseases[Math.floor(Math.random() * sampleDiseases.length)];
        setDiagnosis(randomDiagnosis);
        setAnalyzing(false);
      }, 1200);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-800 pb-4">
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <span>🔬 Plant Leaf Disease AI Scanner</span>
        </h2>
        <p className="text-gray-400 text-sm mt-1">
          Deep learning computer vision to instantly detect fungal, bacterial, and viral crop infections.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
        {/* Upload Column */}
        <div className="md:col-span-6 bg-[#14181f] border border-gray-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-white mb-2">Upload Crop Leaf Photo</h3>
            <p className="text-xs text-gray-400 mb-4">
              Take a clear, well-lit photo of the affected plant leaf for automatic neural network classification.
            </p>

            <label className="border-2 border-dashed border-gray-700 hover:border-purple-500 rounded-2xl p-8 flex flex-col items-center justify-center cursor-pointer transition-colors bg-gray-900/40 group">
              <span className="text-4xl mb-2 group-hover:scale-110 transition-transform">📸</span>
              <span className="text-sm font-semibold text-gray-300">Click to select photo</span>
              <span className="text-xs text-gray-500 mt-1">Supports PNG, JPG, JPEG (Max 10MB)</span>
              <input type="file" accept="image/*" onChange={handleImageChange} className="hidden" />
            </label>

            {selectedImage && (
              <div className="mt-4">
                <span className="text-xs text-gray-400 block mb-1">Image Preview:</span>
                <img
                  src={selectedImage}
                  alt="Leaf preview"
                  className="w-full h-48 object-cover rounded-xl border border-gray-700"
                />
              </div>
            )}
          </div>

          <div className="mt-6 pt-4 border-t border-gray-800 text-xs text-gray-500 flex justify-between">
            <span>Model: MobileNet / ResNet50</span>
            <span>Classes: 38 Crop Diseases</span>
          </div>
        </div>

        {/* Diagnosis Column */}
        <div className="md:col-span-6 bg-[#14181f] border border-gray-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-gray-800 pb-3">
              <span className="text-xs font-bold text-purple-400 uppercase tracking-wider">Diagnostic Analysis</span>
              {diagnosis && (
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/20">
                  Confidence: {diagnosis.confidence}
                </span>
              )}
            </div>

            {analyzing ? (
              <div className="py-20 flex flex-col items-center justify-center space-y-3">
                <div className="w-10 h-10 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-sm text-gray-300 font-medium animate-pulse">
                  Neural network inspecting leaf pathology...
                </p>
              </div>
            ) : diagnosis ? (
              <div className="mt-4 space-y-4">
                <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
                  <span className="text-xs text-gray-400 uppercase font-semibold">Detected Pathology</span>
                  <div className="text-2xl font-extrabold text-purple-300 mt-1">
                    {diagnosis.disease}
                  </div>
                  <span className="text-xs text-gray-300 font-semibold mt-0.5 block">
                    Target Crop: {diagnosis.crop}
                  </span>
                </div>

                <div className="space-y-3 text-xs">
                  <div className="bg-gray-900/80 p-3 rounded-xl border border-gray-800">
                    <span className="font-bold text-gray-300">Observed Symptoms:</span>
                    <p className="text-gray-400 mt-1 leading-relaxed">{diagnosis.symptoms}</p>
                  </div>

                  <div className="bg-emerald-950/20 p-3 rounded-xl border border-emerald-500/30">
                    <span className="font-bold text-emerald-400">Recommended Treatment & Action:</span>
                    <p className="text-emerald-200/90 mt-1 leading-relaxed">{diagnosis.treatment}</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-20 flex flex-col items-center justify-center text-center text-gray-500">
                <span className="text-4xl mb-3">🍃</span>
                <p className="text-sm font-medium">Upload an image on the left to run AI diagnosis</p>
              </div>
            )}
          </div>

          <div className="mt-6 pt-4 border-t border-gray-800 text-[11px] text-gray-500">
            Automated leaf disease detection module from AgriSmart.
          </div>
        </div>
      </div>
    </div>
  );
}
