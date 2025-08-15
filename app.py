import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
       
        if 'plant_image' in request.files:
            uploaded_file = request.files['plant_image']
            
            
            if uploaded_file.filename != '':
    
                base_dir = os.path.abspath(os.path.dirname(__file__))
                uploads_dir = os.path.join(base_dir, 'static/uploads')
                os.makedirs(uploads_dir, exist_ok=True) # Ensure the folder exists

                
                file_path = os.path.join(uploads_dir, uploaded_file.filename)
                uploaded_file.save(file_path)

                
                print(f"File saved successfully to: {file_path}")

    # This runs on a GET request
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)