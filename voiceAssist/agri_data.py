
# Detailed Agriculture Knowledge Base (Hindi)
AGRICULTURE_KNOWLEDGE = {
    "गेहूं": {
        "grow": "गेहूं ठंडे मौसम में उगाया जाता है। बुवाई अक्टूबर से नवंबर में होती है।",
        "soil": "गेहूं के लिए दोमट मिट्टी सबसे अच्छी होती है।",
        "fertilizer": "गेहूं के लिए यूरिया, डीएपी और पोटाश उपयोग करें।",
        "irrigation": "3 से 4 सिंचाई पर्याप्त होती है।"
    },

    "धान": {
        "grow": "धान गर्म और नम मौसम में उगता है। रोपाई जून से जुलाई में होती है।",
        "soil": "धान के लिए चिकनी और जलधारण वाली मिट्टी अच्छी होती है।",
        "fertilizer": "धान के लिए यूरिया और डीएपी उपयोगी है।",
        "irrigation": "धान में पानी खड़ा रहना चाहिए।"
    },
    
    "चावल": { # Alias for Dhan
        "grow": "चावल (धान) गर्म और नम मौसम में उगता है। रोपाई जून से जुलाई में होती है।",
        "soil": "चावल के लिए चिकनी और जलधारण वाली मिट्टी अच्छी होती है।",
        "fertilizer": "चावल के लिए यूरिया और डीएपी उपयोगी है।",
        "irrigation": "खेत में पानी खड़ा रहना चाहिए।"
    },

    "कपास": {
        "grow": "कपास गर्म और शुष्क जलवायु में उगती है।",
        "soil": "कपास के लिए काली मिट्टी सर्वोत्तम होती है।",
        "fertilizer": "नाइट्रोजन और फास्फोरस की आवश्यकता होती है।",
        "irrigation": "हल्की लेकिन नियमित सिंचाई करें।"
    },

    "सब्जी": {
        "grow": "सब्जियों के लिए अच्छी धूप और पानी आवश्यक है।",
        "fertilizer": "गोबर की खाद और वर्मी कंपोस्ट सर्वोत्तम है।",
        "irrigation": "हर 2 से 3 दिन में पानी दें।"
    },

    "फल": {
        "grow": "फलदार पौधों को ज्यादा जगह और धूप चाहिए।",
        "fertilizer": "जैविक खाद और पोटाश उपयोग करें।",
        "irrigation": "सप्ताह में 1 से 2 बार सिंचाई करें।"
    },

    "organic": {
        "fertilizer": "गोबर की खाद, वर्मी कंपोस्ट, नीम खली उपयोग करें।",
        "pest": "नीम का तेल और गोमूत्र छिड़काव करें।"
    },
    
    "जैविक": {
        "fertilizer": "गोबर की खाद, वर्मी कंपोस्ट, नीम खली उपयोग करें।",
        "pest": "नीम का तेल और गोमूत्र छिड़काव करें।"
    }
}

# Keep existing data for compatibility if needed (Previous basic data)
SOIL_DATA = {
    "english": {
        "clay": "Clay soil is best for Rice, Lettuce, and Broccoli.",
        "sandy": "Sandy soil is suitable for Watermelon, Peanuts, and Potatoes.",
        "loamy": "Loamy soil is excellent for Wheat, Sugarcane, Cotton, and most vegetables.",
        "black": "Black soil is effectively 'Black Cotton Soil', perfect for Cotton, Soybeans, and Millets.",
        "red": "Red soil is good for Groundnut, Pulses, and Millets."
    },
    "hindi": {
        "चिकनी": "चिकनी मिट्टी (Clay) धान, सलाद और ब्रोकली के लिए उत्तम है।",
        "रेतीली": "रेतीली मिट्टी (Sandy) तरबूज, मूंगफली और आलू के लिए उपयुक्त है।",
        "बालू": "रेतीली मिट्टी (Sandy) तरबूज और आलू के लिए अच्छी है।",
        "दोमट": "दोमट मिट्टी (Loamy) गेहूं, गन्ना, कपास और अधिकांश सब्जियों के लिए बेहतरीन है।",
        "काली": "काली मिट्टी (Black) कपास, सोयाबीन और बाजरा के लिए सबसे अच्छी है।",
        "लाल": "लाल मिट्टी (Red) मूंगफली, दालें और बाजरा के लिए अच्छी है।",
        "मिट्टी": "मिट्टी के प्रकार पूछें: जैसे 'काली मिट्टी' या 'रेतीली मिट्टी'।"
    }
}

DISEASE_DATA = {
    "english": {
        "yellow": "Yellow leaves often indicate Nitrogen deficiency. Recommendation: Apply Nitrogen-rich fertilizer like Urea.",
        "brown spots": "Brown spots may indicate Fungal infection (Leaf Spot). Recommendation: Spray appropriate Fungicide like Mancozeb.",
        "white powder": "White powder on leaves suggests Powdery Mildew. Recommendation: Spray Sulfur-based fungicide or Neem oil.",
        "holes": "Holes in leaves are likely caused by Caterpillars or Beetles. Recommendation: Use organic pesticides or Neem oil.",
        "curling": "Leaf curling can be due to Aphids or Virus. Recommendation: Check for pests and remove infected parts."
    },
    "hindi": {
        "पीले": "पत्ते पीले होना अक्सर नाइट्रोजन की कमी है। सुझाव: यूरिया जैसी नाइट्रोजन खाद डालें।",
        "भूरे": "भूरे धब्बे कवक संक्रमण (Fungal) हो सकते हैं। सुझाव: मैंकोजेब (Mancozeb) जैसा फफूंदनाशक छिड़कें।",
        "सफेद": "पत्तों पर सफेद पाउडर 'पाउडरी मिलड्यू' रोग है। सुझाव: गंधक (Sulfur) या नीम का तेल छिड़कें।",
        "छेद": "पत्तों में छेद इल्ली या कीड़ों के कारण होते हैं। सुझाव: जैविक कीटनाशक या नीम के तेल का प्रयोग करें।",
        "मुड़": "पत्तों का मुड़ना एफिड्स या वायरस के कारण हो सकता है। सुझाव: कीड़ों की जाँच करें और संक्रमित हिस्से हटा दें।"
    }
}
