async function run() {
    const crop = document.getElementById("crop").value;
    const outputDiv = document.getElementById("output");
    const card = document.getElementById("output-card");

    outputDiv.innerHTML = "Processing...";
    card.style.display = "block";

    try {
        const res = await fetch(`/api/run/${crop}`);
        if (!res.ok) throw new Error("API Request Failed");

        const data = await res.json();

        document.getElementById("output").innerHTML = `
        <strong>Crop:</strong> ${data.crop.toUpperCase()}<br>
        <strong>Temperature:</strong> ${data.temperature}°C<br>
        <strong>Humidity:</strong> ${data.humidity}%<br>
        <strong>Irrigation Decision:</strong> <span style="color:${data.irrigate ? 'blue' : 'grey'}">${data.irrigate ? "TURN ON WATER" : "NO IRRIGATION NEEDED"}</span><br>
        <strong>Water Required:</strong> ${data.waterRequired} mm<br>
        <strong>Estimated Yield:</strong> ${data.estimatedYield.toFixed(2)} tons/ha
      `;
    } catch (err) {
        document.getElementById("output").innerHTML = `<span style="color:red">Error: ${err.message}</span>`;
    }
}
