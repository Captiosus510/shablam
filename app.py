import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from utils import create_database

# Create Flask app
app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

upload_status = None

# Route to handle file upload
@app.route('/', methods=['GET', 'POST'])
def index():

    #dictionary with movie descriptions!
    movie_descriptions = {
        "Inception": ["Rating: 8.8/10", "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project and his team to disaster."], 
        "Your Name": ["Rating: 8.4/10", "Two teenagers share a profound, magical connection upon discovering they are swapping bodies. Things manage to become even more complicated when the boy and girl decide to meet in person."], 
        "Ironman": ["Rating: 7.9/10", "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil."]
    }
    

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Call your algorithm here to get the movie name
            # movie_name = find_best_movie(filepath)
            movie_name = ""

            upload_status = True
            
            # Pass the result to the template
            return render_template('index.html', movie_name=movie_name, movie_descriptions=movie_descriptions, upload_status=upload_status)
    
    upload_status = False
    return render_template('index.html', upload_status=upload_status)


# Example function to analyze the file
def analyze_file(filepath):
    return "Inception"  # Replace with actual result from your algorithm

if __name__ == '__main__':
    app.run(debug=True)
