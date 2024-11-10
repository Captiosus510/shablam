// JavaScript to handle drag-and-drop functionality
const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("file");  // Corrected reference here

// Handle drag events for file input
dropArea.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropArea.classList.add("hover");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("hover");
});

dropArea.addEventListener("drop", (event) => {
    event.preventDefault();
    dropArea.classList.remove("hover");

    const files = event.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
    }
});

dropArea.addEventListener("click", () => {
    fileInput.click();
});

document.getElementById("upload-form").addEventListener("submit", function(event) {
    // Show progress bar container
    document.querySelector(".progress-container").style.display = "block";

    // Initialize progress values
    const progressFill = document.getElementById("progress-fill");
    const progressText = document.getElementById("progress-text");

    // Poll the progress endpoint
    function updateProgress() {
        fetch("/progress")
            .then(response => response.json())
            .then(data => {
                const progress = data.progress;

                // Update progress bar width and text
                progressFill.style.width = `${progress}%`;
                progressText.textContent = `${progress}%`;

                // Continue polling if progress is less than 100
                if (progress < 100) {
                    setTimeout(updateProgress, 500);
                }
            })
            .catch(error => console.error("Error fetching progress:", error));
    }

    // Start polling for progress updates
    updateProgress();
});
