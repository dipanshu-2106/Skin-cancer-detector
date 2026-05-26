from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Model settings
MODEL_PATH = "skin_cancer_resnet50.keras"
IMG_SIZE = 224

# Load model only once
try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found!")

    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded successfully")

except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:

        if model is None:
            return jsonify({"error": "Model not loaded"})

        img = None

        # File upload
        if "file" in request.files:

            file = request.files["file"]

            if file.filename == "":
                return jsonify({"error": "No image selected"})

            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            img = image.load_img(
                filepath,
                target_size=(IMG_SIZE, IMG_SIZE)
            )

        # Webcam/Base64 image
        elif request.json and "image_base64" in request.json:

            img_data_str = request.json["image_base64"]

            img_data = img_data_str.split(",")[1]
            img_bytes = base64.b64decode(img_data)

            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            img = img.resize((IMG_SIZE, IMG_SIZE))

        else:
            return jsonify({"error": "No image provided"})

        # Image preprocessing
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Prediction
        prediction = model.predict(img_array)[0][0]

        if prediction > 0.5:
            label = "Cancer"
            confidence = round(float(prediction) * 100, 2)
        else:
            label = "Non Cancer"
            confidence = round((1 - float(prediction)) * 100, 2)

        return jsonify({
            "result": label,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)