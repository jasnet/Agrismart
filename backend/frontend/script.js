document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const btn = form.querySelector('.primary-btn');
    const resultsContainer = document.getElementById('resultsContainer');

    // Loading state
    btn.classList.add('loading');
    btn.disabled = true;

    // Gather data
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Convert strings to floats
    for (let key in data) {
        data[key] = parseFloat(data[key]);
    }

    try {
        // 1. Get Prediction
        const predictResponse = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!predictResponse.ok) throw new Error('Prediction failed');

        const predictResult = await predictResponse.json();
        const crop = predictResult.fertility_or_crop;

        // 2. Get Crop Info
        const infoResponse = await fetch(`/crop-info/${crop}`);
        let cropInfo = null;

        if (infoResponse.ok) {
            cropInfo = await infoResponse.json();
        }

        // 3. Update UI
        document.getElementById('cropName').textContent = crop;

        const detailsContainer = document.getElementById('cropDetails');
        detailsContainer.innerHTML = ''; // Clear previous

        if (cropInfo && cropInfo.profile) {
            const p = cropInfo.profile;
            const fields = [
                { label: 'Nitrogen Req', value: p.nitrogen_req },
                { label: 'Phosphorus Req', value: p.phosphorus_req },
                { label: 'Potassium Req', value: p.potassium_req },
                { label: 'pH Range', value: p.pH_req },
                { label: 'Rainfall Req', value: p.rainfall_req },
                { label: 'Temp Req', value: p.temperature_req },
            ];

            fields.forEach(field => {
                const div = document.createElement('div');
                div.className = 'detail-item';
                div.innerHTML = `
                    <span class="detail-label">${field.label}</span>
                    <span class="detail-value">${field.value}</span>
                `;
                detailsContainer.appendChild(div);
            });
        } else {
            detailsContainer.innerHTML = '<div class="detail-item">No detailed profile available for this crop.</div>';
        }

        // Show results
        resultsContainer.classList.add('visible');

    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while processing your request.');
    } finally {
        btn.classList.remove('loading');
        btn.disabled = false;
    }
});
