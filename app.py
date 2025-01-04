from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Paths to the model files
MODELS = {
    "mobilenet": "mobilenet_final.keras",
    "handcrafted": "mobilenet_final.keras"
}

# Ensure model files exist
for model_name, model_path in MODELS.items():
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file for {model_name} not found at: {model_path}")

# Load models into memory
loaded_models = {name: load_model(path) for name, path in MODELS.items()}
print(f"Models loaded: {', '.join(loaded_models.keys())}")

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess the image to the format expected by the model.
    """
    img = image.load_img(image_path, target_size=target_size)  # Resize image
    img_array = image.img_to_array(img)  # Convert image to numpy array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize the image
    return img_array

def predict_image(image_path, model):
    """
    Preprocess the image and make a prediction using the specified model.
    """
    # Preprocess the image
    img_array = preprocess_image(image_path)

    # Make prediction
    prediction = model.predict(img_array)

    # Return the predicted class
    return 1 if prediction >= 0.5 else 0

@app.route('/predict/<model_name>', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def predict(model_name):
    try:
        # Check if the model exists
        if model_name not in loaded_models:
            return jsonify({'error': f"Model '{model_name}' not found"}), 400

        # Ensure a file is included in the request
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

        # Perform prediction with the specified model
        model = loaded_models[model_name]
        predicted_class = predict_image(image_path, model)

        # Map prediction to class name
        predicted_class = 'Invasive' if predicted_class == 1 else 'Non Invasive'

        print(f"Model: {model_name}, Prediction: {predicted_class}")
        return jsonify({'predicted_class': predicted_class, 'image_path': image_path})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
