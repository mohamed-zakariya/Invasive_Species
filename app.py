from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Load the final model globally
MODEL_PATH = "mobilenet_final.keras"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
model = load_model(MODEL_PATH)
print(f"Model loaded from {MODEL_PATH}")

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess the image to the format expected by the model.
    """
    img = image.load_img(image_path, target_size=target_size)  # Resize image
    img_array = image.img_to_array(img)  # Convert image to numpy array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize the image
    return img_array

def predict_image(image_path):
    """
    Preprocess the image and make a prediction using the loaded model.
    """
    # Preprocess the image
    img_array = preprocess_image(image_path)

    # Make prediction
    prediction = model.predict(img_array)

    # Return the predicted class
    return 1 if prediction >= 0.5 else 0

@app.route('/predict', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Ensure the 'uploads' directory exists
        uploads_dir = 'uploads'
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        # Save the file temporarily
        image_path = os.path.join(uploads_dir, file.filename)
        file.save(image_path)

        # Perform prediction
        predicted_class = predict_image(image_path)

        # Map prediction to class name
        if predicted_class == 0:
            predicted_class = 'Non Invasive'
        else:
            predicted_class = 'Invasive'
        
        print(predicted_class)
        return jsonify({'predicted_class': predicted_class, 'image_path': image_path})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
