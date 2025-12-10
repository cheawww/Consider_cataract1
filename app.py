from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
import json
import base64
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

model = load_model('my_model.h5')

UPLOAD_DIR = 'uploads'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def preprocess_image(img_path, target_size=(170, 200)):
    """Loads, resizes, and normalizes an image for prediction."""
    img = load_img(img_path, target_size=target_size)
    img_array = img_to_array(img) 
    img_array = img_array / 255.0 
    return np.expand_dims(img_array, axis=0) 

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.json'):
        try:
            json_data = json.load(file)
            base64_image = json_data.get('image')
            if not base64_image:
                return jsonify({"error": "No image found in JSON"}), 400
            image_data = base64.b64decode(base64_image.split(',')[1])
            image_path = os.path.join(UPLOAD_DIR, 'uploaded_photo.jpg')
            with open(image_path, 'wb') as f:
                f.write(image_data)
            img = preprocess_image(image_path)
            val = model.predict(img)
            percentage = val[0][0] * 100
            prediction = "No Cataract" if percentage > 40 else "Cataract"
            if percentage < 40:
                percentage = 100 - percentage
            confidence = f"{percentage:.2f}%"

            if prediction == "Cataract":
                return redirect(url_for('result_page_cataract', prediction=prediction, confidence=confidence))
            else:
                return redirect(url_for('result_page_no_cataract', prediction=prediction, confidence=confidence))

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/result/cataract')
def result_page_cataract():
    return send_from_directory(directory='static', path='eye1.html')

@app.route('/result/no_cataract')
def result_page_no_cataract():
    return send_from_directory(directory='static', path='eye2.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)



