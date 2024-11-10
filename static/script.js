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