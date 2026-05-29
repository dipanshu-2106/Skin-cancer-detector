from flask import Flask, render_template, request, jsonify
<<<<<<< HEAD
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
=======
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

# Download weights from Google Drive if not exists
WEIGHTS_PATH = "skin_cancer.weights.h5"
if not os.path.exists(WEIGHTS_PATH):
    print("Downloading weights from Google Drive...")
    gdown.download(
        "https://drive.google.com/uc?id=1sm3_gYVSJiKHw1yuRXaeZvLW8UcCtlaa",
        WEIGHTS_PATH,
        quiet=False
    )

# CREATE MODEL
model = create_model()

# LOAD WEIGHTS
model.load_weights(WEIGHTS_PATH)
print("✅ MODEL LOADED SUCCESSFULLY")

>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1

@app.route("/")
def home():
    return render_template("index.html")

<<<<<<< HEAD
def preprocess_img(img):
    img = img.convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    arr = image.img_to_array(img)
    arr = arr / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr
=======
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1

@app.route("/predict", methods=["POST"])
def predict():
    try:
<<<<<<< HEAD
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
=======
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
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1

        return jsonify({"result": label, "confidence": confidence})

    except Exception as e:
<<<<<<< HEAD
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))  # ✅ Hugging Face ke liye 7860
    app.run(host="0.0.0.0", port=port, debug=False)
=======
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
>>>>>>> dcd74f296eb1d9918468141d946f6c6e8ee433a1
