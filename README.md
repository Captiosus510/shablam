# Shablam

Have you ever scrolled on Instagram and seen a scene from a movie or show that was not credited? Have you ever wanted to know where the material is from, but had to scroll through the comments to find it from some good samaritan who posted it? Well with Shablam, this will not be a problem any longer!

## Technologies Used

This project is built with:
- **FastAPI** - Modern, fast web framework for building APIs with Python
- **JavaScript (AJAX)** - For dynamic, asynchronous file uploads and real-time updates
- **OpenCV** - Computer vision for video processing and feature extraction
- **PyTorch** - Deep learning framework for CNN-based feature extraction
- **Scikit-learn** - Machine learning for similarity matching
- **TMDB API** - The Movie Database API for fetching movie posters and metadata
- **HTML/CSS** - Clean, responsive frontend design

## Installation

Clone the repository into your folder and then use [pip](https://pip.pypa.io/en/stable/) to install the required dependencies.

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Create the Movie Database
First we need to use a script to compile a "database" (it's really just a dictionary that's been dumped into a pickle file for later use). Add the movies/scenes to the "movie_scenes" folder and then run compile.py. Don't worry if this takes a while.

```bash
python compile.py
```

### Step 2: Start the FastAPI Server
Run the FastAPI application with uvicorn. This will spawn a locally hosted instance of the website.

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`

### Step 3: Upload and Identify
1. Open your web browser and navigate to `http://127.0.0.1:8000`
2. Upload a movie scene by dragging and dropping or clicking to select a file
3. Click "What movie is this?" and wait for the AJAX-powered processing
4. Get real-time results without page reloads!

The application uses AJAX for seamless file uploads and dynamic content updates, providing instant feedback and a smooth user experience.

## Features

- **Drag & Drop Upload** - Easy file selection with visual feedback
- **Real-time Progress** - AJAX-powered progress tracking during processing
- **Dynamic Results** - Instant result display without page reloads
- **Movie Metadata** - Fetches ratings, descriptions, and posters from TMDB
- **Responsive Design** - Clean, modern UI that works on all devices

This project was created by Mahd, Prem, Aditya, Dinara, and Fogil.

## More Info

Find more info at our devpost:
https://devpost.com/software/shabam
