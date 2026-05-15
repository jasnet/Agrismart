function estimateYield(crop, irrigate) {
    let baseYield;
    const c = crop.toLowerCase();

    switch (c) {
        case "wheat": baseYield = 3.5; break;
        case "rice": baseYield = 4.0; break;
        case "maize": baseYield = 5.5; break;
        case "sugarcane": baseYield = 70; break;
        default: baseYield = 3;
    }

    return irrigate ? baseYield * 1.1 : baseYield * 0.9;
}

module.exports = estimateYield;
