document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileInput");
    const fileName = document.querySelector(".file-name");
    const uploadForm = document.getElementById("uploadForm");
    const loading = document.querySelector(".loading");
    const results = document.querySelector(".results");

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            fileName.textContent = fileInput.files[0].name;
        } else {
            fileName.textContent = "No file selected";
        }
    });

    uploadForm.addEventListener("submit", function (e) {
        e.preventDefault();

        if (fileInput.files.length === 0) {
            results.innerHTML = '<p class="error">Please select a file to upload.</p>';
            return;
        }

        loading.style.display = "block";
        results.innerHTML = "";

        // Simulate file upload and analysis
        setTimeout(() => {
            loading.style.display = "none";

            // Simulated Score (Replace this with actual score from backend response)
            const simulatedScore = Math.floor(Math.random() * 11); // Random score between 0-10
            let colorDot = "";

            if (simulatedScore <= 3) {
                colorDot = "🟢"; // Green for low risk
            } else if (simulatedScore <= 6) {
                colorDot = "🟡"; // Yellow for medium risk
            } else {
                colorDot = "🔴"; // Red for high risk
            }

            results.innerHTML = `
                <p>File uploaded successfully: <strong>${fileInput.files[0].name}</strong></p>
                <p><strong>Phishing Score:</strong> ${simulatedScore}/10</p>
                <h4>Overview: ${colorDot} Suspicious Email</h4>
                <p>Detailed explanation about why this email was rated ${simulatedScore}.</p>
            `;
        }, 2000);
    });
});
