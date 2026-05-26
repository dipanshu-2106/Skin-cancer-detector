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
MODEL_PATH = "skin_cancer_resnet50.h5"
IMG_SIZE = 224

# Load model
try:

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file '{MODEL_PATH}' not found!"
        )

    model = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False,
        safe_mode=False
    )

    print("✅ Model loaded successfully!")

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
            return jsonify({
                "error": "Model not loaded"
            })

        img = None

        # File Upload
        if "file" in request.files:

            file = request.files["file"]

            if file.filename == "":
                return jsonify({
                    "error": "No image selected"
                })

            filepath = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            file.save(filepath)

            img = image.load_img(
                filepath,
                target_size=(IMG_SIZE, IMG_SIZE)
            )

        # Webcam/Base64 Upload
        elif request.json and "image_base64" in request.json:

            img_data_str = request.json["image_base64"]

            if "," not in img_data_str:
                return jsonify({
                    "error": "Invalid image format"
                })

            img_data = img_data_str.split(",")[1]

            img_bytes = base64.b64decode(img_data)

            img = Image.open(
                io.BytesIO(img_bytes)
            ).convert("RGB")

            img = img.resize(
                (IMG_SIZE, IMG_SIZE)
            )

        else:
            return jsonify({
                "error": "No image provided"
            })

        # Preprocessing
        img_array = image.img_to_array(img)

        img_array = img_array / 255.0

        img_array = np.expand_dims(
            img_array,
            axis=0
        )

        # Prediction
        prediction = model.predict(img_array)

        prediction_value = float(prediction[0][0])

        if prediction_value > 0.5:

            label = "Cancer"

            confidence = round(
                prediction_value * 100,
                2
            )

        else:

            label = "Non Cancer"

            confidence = round(
                (1 - prediction_value) * 100,
                2
            )

        return jsonify({
            "result": label,
            "confidence": confidence
        })

    except Exception as e:

        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        })


if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )