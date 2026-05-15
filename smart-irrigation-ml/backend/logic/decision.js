const { spawn } = require("child_process");
const path = require("path");

function mlDecision(weather) {
    return new Promise((resolve, reject) => {
        const pythonExecutable = "/Applications/MCA PROJECT/backend/venv/bin/python3";
        const scriptPath = path.join(__dirname, "../ml/predict.py");

        const pythonProcess = spawn(pythonExecutable, [
            scriptPath,
            weather.temperature,
            weather.humidity,
            weather.rain
        ]);

        let dataString = "";

        pythonProcess.stdout.on("data", (data) => {
            dataString += data.toString();
        });

        pythonProcess.stderr.on("data", (data) => {
            console.error(`Python Error: ${data}`);
        });

        pythonProcess.on("close", (code) => {
            if (code !== 0) {
                console.error(`Python script exited with code ${code}`);
                resolve(0);
                return;
            }

            try {
                // Parse the accumulated JSON string
                // The script returns a JSON array: [{"irrigate": 1}]
                const output = JSON.parse(dataString.trim());
                let decision = 0;

                if (Array.isArray(output) && output.length > 0) {
                    decision = output[0].irrigate;
                } else if (output && output.irrigate !== undefined) {
                    decision = output.irrigate;
                }

                resolve(decision);
            } catch (e) {
                console.error("Failed to parse Python output:", dataString, e);
                resolve(0);
            }
        });

        pythonProcess.on("error", (err) => {
            console.error("Failed to start python process:", err);
            resolve(0);
        });
    });
}

module.exports = mlDecision;
