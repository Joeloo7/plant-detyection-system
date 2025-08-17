import os
from flask import Flask, render_template, request

# 1. SETUP: Create the Flask application
app = Flask(__name__)

# 2. THE ROUTE: This is the main page of your website
@app.route('/', methods=['GET', 'POST'])
def home():
    
    # 3. POST LOGIC: This block runs ONLY when a user uploads a file
    if request.method == 'POST':
        # Safety check: see if a file was actually uploaded
        if 'plant_image' in request.files:
            uploaded_file = request.files['plant_image']
            
            # If the user selected a file, save it
            if uploaded_file.filename != '':
                # Create the full path to the uploads folder
                base_dir = os.path.abspath(os.path.dirname(__file__))
                uploads_dir = os.path.join(base_dir, 'static/uploads')
                os.makedirs(uploads_dir, exist_ok=True) # Make the folder if it doesn't exist

                # Save the file
                file_path = os.path.join(uploads_dir, uploaded_file.filename)
                uploaded_file.save(file_path)

                # This is our fake prediction for now
                prediction = "This looks like a Rose! 🌹"
                
                # Show the results page
                return render_template('results.html', prediction=prediction, image_path=uploaded_file.filename)

    # 4. GET LOGIC: This runs when a user first visits the page
    return render_template('index.html')

# 5. START THE APP: This runs the web server
if __name__ == '__main__':
    app.run(debug=True)