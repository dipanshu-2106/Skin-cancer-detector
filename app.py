from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image
import os
import gdown

from model_architecture import create_model

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

IMG_SIZE = 224

WEIGHTS_PATH = "skin_cancer.weights.h5"
if not os.path.exists(WEIGHTS_PATH):
    print("Downloading weights from Google Drive...")
    gdown.download(
        "https://drive.google.com/uc?id=12HUnfBTkgx2ni3RoZdJlAO1kRVXIwytM",
        WEIGHTS_PATH,
        quiet=False
    )

model = create_model()
model.load_weights(WEIGHTS_PATH, by_name=True, skip_mismatch=True)
print("✅ MODEL LOADED SUCCESSFULLY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"})

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No image selected"})

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        img = image.load_img(filepath, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)[0][0]

        if prediction > 0.5:
            label = "Cancer"
            confidence = round(float(prediction) * 100, 2)
        else:
            label = "Non Cancer"
            confidence = round((1 - float(prediction)) * 100, 2)

        return jsonify({"result": label, "confidence": confidence})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)