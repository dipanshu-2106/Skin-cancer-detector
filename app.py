from flask import Flask, render_template, request, jsonify
import os
import io
import base64
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MODEL_PATH = os.path.join(BASE_DIR, "skin_cancer_resnet50.h5")
IMG_SIZE = 224

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

model = load_model(MODEL_PATH, compile=False)

@app.route("/")
def home():
    return render_template("index.html")

def preprocess_img(img):
    img = img.convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    arr = image.img_to_array(img)
    arr = arr / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

@app.route("/predict", methods=["POST"])
def predict():
    try:
        img = None

        if "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                return jsonify({"error": "No image selected"}), 400
            img = Image.open(file.stream)

        elif request.is_json and request.json and "image_base64" in request.json:
            data = request.json.get("image_base64")
            if "," in data:
                data = data.split(",")[1]
            img_bytes = base64.b64decode(data)
            img = Image.open(io.BytesIO(img_bytes))

        else:
            return jsonify({"error": "No image provided"}), 400

        x = preprocess_img(img)
        prediction = model.predict(x, verbose=0)
        pred = float(prediction[0][0])

        if pred > 0.5:
            label = "Cancer"
            confidence = round(pred * 100, 2)
        else:
            label = "Non Cancer"
            confidence = round((1 - pred) * 100, 2)

        return jsonify({"result": label, "confidence": confidence})

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)