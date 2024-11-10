import os
import time
import pickle
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from utils.compare import find_best_movie
import shutil

# Create Flask app
app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    "Iron Man": ["Rating: 7.9/10", "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil."]
}

# Variable to store progress
progress_data = {"progress": 0}

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to handle file upload and prediction
@app.route('/', methods=['GET', 'POST'])
def index():
    global progress_data
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        # Reset progress for new upload
        progress_data['progress'] = 0
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Simulate processing and update progress
            def run_prediction():
                global progress
                movie_scores = find_best_movie(filepath, data_dict, progress_data)

                movie_name, match_val = movie_scores[0]
                if match_val > 0.6:
                    result = movie_name.title()
                else:
                    result = "No matching movie found."

    
                return result

            # Run the prediction
            result = run_prediction()
            # os.remove(filepath)
            return render_template(
                'index.html',
                movie_name=result,
                movie_descriptions=movie_descriptions,
                upload_status=True
            )

    return render_template('index.html', upload_status=False)

# Endpoint to get the current progress
@app.route('/progress')
def get_progress():
    progress = progress_data["progress"]
    return jsonify(progress=int(progress))

if __name__ == '__main__':
    app.run(debug=True)
    shutil.rmtree('uploads')
