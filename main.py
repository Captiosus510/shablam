import os
import time
import pickle
from fastapi import FastAPI, File, UploadFile, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from werkzeug.utils import secure_filename
from utils.compare import find_best_movie
from utils.tmdb import get_movie
import shutil

# Create FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

# Load data for movie comparison
with open("keyframedata.pkl", "rb") as f:
    data_dict = pickle.load(f)

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Dictionary with movie descriptions
movie_descriptions = {
    "Inception": ["Rating: 8.8/10", "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project and his team to disaster."],
    "Your Name": ["Rating: 8.4/10", "Two teenagers share a profound, magical connection upon discovering they are swapping bodies. Things become even more complicated when they decide to meet in person."],
    "Iron Man 1": ["Rating: 7.9/10", "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil."]
}

# Variable to store progress
progress_data = {"progress": 0}

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "upload_status": False})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global progress_data
    progress_data['progress'] = 0
    
    if not (file and allowed_file(file.filename)):
        return JSONResponse(content={"error": "File not allowed or not provided"}, status_code=400)

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run the prediction
    movie_scores = find_best_movie(filepath, data_dict, progress_data)
    movie_name, match_val = movie_scores[0]

    if match_val > 0.6:
        result = movie_name.title()
        movie_info = movie_descriptions.get(result, ["", ""])
        rating = movie_info[0]
        description = movie_info[1]
        image_url = get_movie(result)['poster_path']
        
        return JSONResponse({
            "success": True,
            "movie_name": result,
            "rating": rating,
            "description": description,
            "image": f"https://image.tmdb.org/t/p/w500/{image_url}" if image_url else None
        })
    else:
        return JSONResponse({
            "success": True,
            "movie_name": "No matching movie found.",
            "description": "We couldn't find a match for the uploaded clip. Please try another one."
        })

@app.get("/progress")
async def get_progress():
    progress = progress_data["progress"]
    return JSONResponse(content={"progress": int(progress)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
