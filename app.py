import os
from flask import Flask, render_template, request


import tensorflow as tf
from PIL import Image
import numpy as np


app = Flask(__name__)


#Load the Pre-trained Model 
model = tf.keras.applications.MobileNetV2(weights='imagenet')


def get_plant_prediction(image_path):
    """
    Takes an image path pre-processes the image and returns a prediction.
    """
    # 1. Load the image
    img = Image.open(image_path).resize((224, 224))

    # 2. Pre-process the image for the model
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    processed_image = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    # 3. Get the prediction from the model
    predictions = model.predict(processed_image)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0]
    
    # 4. Return the top prediction
    top_prediction = decoded_predictions[0]
    plant_name = top_prediction[1].replace('_', ' ').title()
    confidence = top_prediction[2]
    
    return f"{plant_name} ({confidence:.2%})"



# 2. THE ROUTE: This is the main page of your website
@app.route('/', methods=['GET', 'POST'])
def home():
    
    # 3. POST LOGIC: This block runs ONLY when a user uploads a file
    if request.method == 'POST':
        if 'plant_image' in request.files:
            uploaded_file = request.files['plant_image']
            if uploaded_file.filename != '':
                # Create the full path and save the file
                base_dir = os.path.abspath(os.path.dirname(__file__))
                uploads_dir = os.path.join(base_dir, 'static/uploads')
                os.makedirs(uploads_dir, exist_ok=True)
                file_path = os.path.join(uploads_dir, uploaded_file.filename)
                uploaded_file.save(file_path)

                # --- Use the REAL prediction function ---
                prediction = get_plant_prediction(file_path)
                # --------------------------------------
                
                # Show the results page
                return render_template('results.html', prediction=prediction, image_path=uploaded_file.filename)

    # 4. GET LOGIC: This runs when a user first visits the page
    return render_template('index.html')


# 5. START THE APP: This runs the web server
if __name__ == '__main__':
    app.run(debug=True)