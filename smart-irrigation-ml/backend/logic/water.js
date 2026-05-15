const cropWater = {
    wheat: 450,
    rice: 1200,
    maize: 600,
    sugarcane: 1800
};

function waterRequirement(crop) {
    return cropWater[crop.toLowerCase()] || 500;
}

module.exports = waterRequirement;
