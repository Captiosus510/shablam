from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

# Create Flask app
app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}  # Modify this based on your input types
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to handle file upload
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the uploaded file and get the movie name (replace with your algorithm)
            movie_name = analyze_file(filepath)  # Call your algorithm here
            
            # Return result to frontend
            return render_template('index.html', movie_name=movie_name)
    
    return render_template('index.html')

# Example function to analyze the file (replace with your own algorithm)
def analyze_file(filepath):
    # This is where you can use any image/video processing algorithm
    # For example, use OpenCV or machine learning models to analyze the file and return a movie name
    # For now, we'll just return a dummy movie name
    return "Inception"  # Replace with actual result from your algorithm

if __name__ == '__main__':
    app.run(debug=True)
