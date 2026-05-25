from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

# =========================
# CONFIG
# =========================
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MODEL_PATH = "skin_cancer_resnet50.keras"
IMG_SIZE = 224

# =========================
# MODEL LOAD (LOCAL ONLY)
# =========================
if not os.path.exists(MODEL_PATH):
    raise Exception(
        "Model file not found! Please ensure skin_cancer_resnet50.keras "
        "is present in the repo (Git LFS enabled)."
    )

print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully!")

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        img = None

        # -------------------------
        # CASE 1: FILE UPLOAD
        # -------------------------
        if "file" in request.files:
            file = request.files["file"]

            if file.filename == "":
                return jsonify({"error": "No image provided"})

            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            img = image.load_img(filepath, target_size=(IMG_SIZE, IMG_SIZE))

        # -------------------------
        # CASE 2: BASE64 IMAGE
        # -------------------------
        elif request.json and "image_base64" in request.json:
            img_data_str = request.json.get("image_base64", "")

            if not img_data_str or "," not in img_data_str:
                return jsonify({"error": "No image provided"})

            img_data = img_data_str.split(",")[1]
            img_bytes = base64.b64decode(img_data)

            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            img = img.resize((IMG_SIZE, IMG_SIZE))

        else:
            return jsonify({"error": "No image provided"})

        # -------------------------
        # PREPROCESS
        # -------------------------
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # -------------------------
        # PREDICT
        # -------------------------
        prediction = model.predict(img_array)[0][0]

        label = "Cancer" if prediction > 0.5 else "Non Cancer"

        confidence = round(float(prediction) * 100, 2) if label == "Cancer" else round((1 - float(prediction)) * 100, 2)

        return jsonify({
            "result": label,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        })


# =========================
# RUN (RENDER SAFE)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)