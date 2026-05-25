from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import io
import base64
import os
import gdown

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Model download from Google Drive
MODEL_PATH = "skin_cancer_resnet50.keras"

if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    gdown.download(
        "https://drive.google.com/uc?id=1sm3_gYVSJiKHw1yuRXaeZvLW8UcCtlaa",
        MODEL_PATH,
        quiet=False
    )

model = load_model(MODEL_PATH)
img_size = 224


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" in request.files:
            file = request.files["file"]

            if file.filename == "":
                return jsonify({"error": "No image provided"})

            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            img = image.load_img(
                filepath,
                target_size=(img_size, img_size)
            )

        elif request.json and "image_base64" in request.json:

            img_data_str = request.json.get("image_base64", "")

            if not img_data_str or ',' not in img_data_str:
                return jsonify({"error": "No image provided"})

            img_data = img_data_str.split(",")[1]
            img_bytes = base64.b64decode(img_data)

            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            img = img.resize((img_size, img_size))

        else:
            return jsonify({"error": "No image provided"})

        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)[0][0]

        label = "Cancer" if prediction > 0.5 else "Non Cancer"

        confidence = (
            round(float(prediction) * 100, 2)
            if label == "Cancer"
            else round((1 - float(prediction)) * 100, 2)
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
    