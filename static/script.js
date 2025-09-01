// JavaScript to handle drag-and-drop functionality
console.log('External script.js is loading...');

document.addEventListener('DOMContentLoaded', function() {
    console.log('script.js loaded and DOM ready');
    
    const dropArea = document.getElementById("drop-area");
    const fileInput = document.getElementById("file");
    const progressContainer = document.querySelector(".progress-container");
    const progressFill = document.getElementById("progress-fill");
    const progressText = document.getElementById("progress-text");
    const form = document.getElementById("upload-form");

    console.log('Elements found:', {
        dropArea: !!dropArea,
        fileInput: !!fileInput,
        progressContainer: !!progressContainer,
        form: !!form
    });

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
            dropArea.querySelector('p').textContent = `File selected: ${files[0].name}`;
        }
    });

    dropArea.addEventListener("click", () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            const fileName = fileInput.files[0].name;
            dropArea.querySelector('p').textContent = `File selected: ${fileName}`;
        }
    });

    form.addEventListener("submit", function(event) {
        console.log('Form submit intercepted');
        event.preventDefault();
        
        if (fileInput.files.length === 0) {
            alert("Please select a file to upload.");
            return;
        }

        console.log('Starting upload...');
        progressContainer.style.display = "block";
        progressFill.style.width = "0%";
        progressText.textContent = "0%";
        
        const formData = new FormData(form);
        console.log('FormData created');

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => {
            console.log('Response received:', response.status);
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);
            progressFill.style.width = "100%";
            progressText.textContent = "100%";
            showConfirmation(data);
            updateOutput(data);
        })
        .catch(error => {
            console.error("Upload failed:", error);
            progressContainer.style.display = "none";
            showConfirmation({success: false});
            alert("Upload failed. See console for details.");
        });
    });

    function showConfirmation(data) {
        console.log('Showing confirmation:', data);
        let conf = document.querySelector('.content-input .confirmation-message');
        if (!conf) {
            conf = document.createElement('div');
            conf.className = 'confirmation-message';
            document.querySelector('.content-input').appendChild(conf);
        }
        conf.style.display = "block";
        if (data.success) {
            conf.textContent = "File uploaded successfully!";
            conf.style.color = "green";
            conf.style.fontWeight = "bold";
            conf.style.marginBottom = "10px";
        } else {
            conf.textContent = "File upload failed.";
            conf.style.color = "red";
            conf.style.fontWeight = "bold";
            conf.style.marginBottom = "10px";
        }
    }

    function updateOutput(data) {
        console.log('Updating output:', data);
        const outputDiv = document.querySelector('.content-output');
        if (data.movie_name && data.movie_name !== "No matching movie found.") {
            outputDiv.innerHTML = `
                <h2>${data.movie_name}</h2>
                <p><strong>${data.rating}</strong><br><br>${data.description}</p>
                ${data.image ? `<img src="${data.image}" alt="Movie Poster" class="movie-poster">` : ''}
            `;
        } else {
            outputDiv.innerHTML = `
                <h2>No matching movie found.</h2>
                <p>${data.description || "We couldn't find a match for the uploaded clip. Please try another one."}</p>
            `;
        }
    }
});