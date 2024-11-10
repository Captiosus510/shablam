// JavaScript to handle drag-and-drop functionality
const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("file");
const progressContainer = document.querySelector(".progress-container");
const progressFill = document.getElementById("progress-fill");
const progressText = document.getElementById("progress-text");
const form = document.getElementById("upload-form");

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

form.addEventListener("submit", function(event) {
    // Ensure a file is selected before showing progress
    if (fileInput.files.length === 0) {
        event.preventDefault();
        alert("Please select a file to upload.");
        return;
    }

    // Show progress bar container
    progressContainer.style.display = "block";
    
    // Reset progress bar
    progressFill.style.width = "0%";
    progressText.textContent = "0%";

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
