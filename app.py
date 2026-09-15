from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
app = Flask(__name__)
# ==============================
# MODEL
# ==============================
MODEL_PATH = "model/skin_cancer_resnet50.keras"
IMG_SIZE = (224, 224)
model = load_model(MODEL_PATH)
# ==============================
# HOME
# ==============================
@app.route("/")
def home():
    return render_template("index.html")
# ==============================
# PREDICTION
# ==============================
@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image uploaded"
        }), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "Please select an image"
        }), 400
    try:
        # --------------------------
        # LOAD IMAGE
        # --------------------------
        image = Image.open(file).convert("RGB")
        image = image.resize(IMG_SIZE)
        # --------------------------
        # PREPROCESS
        # --------------------------
        img_array = np.array(
            image,
            dtype=np.float32
        )
        img_array = img_array / 255.0
        img_array = np.expand_dims(
            img_array,
            axis=0
        )
        # --------------------------
        # MODEL PREDICTION
        # --------------------------
        prediction = model.predict(
            img_array,
            verbose=0
        )
        # --------------------------
        # BINARY MODEL
        # --------------------------
        if prediction.shape[-1] == 1:
            cancer_score = float(
                prediction[0][0]
            )
            non_cancer_score = 1.0 - cancer_score
        # --------------------------
        # TWO OUTPUT MODEL
        # --------------------------
        elif prediction.shape[-1] == 2:
            probabilities = prediction[0]
            non_cancer_score = float(
                probabilities[0]
            )
            cancer_score = float(
                probabilities[1]
            )
        # --------------------------
        # MULTI CLASS FALLBACK
        # --------------------------
        else:
            probabilities = prediction[0]
            cancer_score = float(
                np.max(probabilities)
            )
            non_cancer_score = 1.0 - cancer_score
        # --------------------------
        # CONVERT TO PERCENTAGE
        # --------------------------
        cancer_percentage = (
            cancer_score * 100
        )
        non_cancer_percentage = (
            non_cancer_score * 100
        )
        # --------------------------
        # FINAL RESULT
        # --------------------------
        if cancer_score >= non_cancer_score:
            result = "Cancer"
        else:
            result = "Non-Cancer"
        return jsonify({
            "success": True,
            "result": result,
            "cancer_score": round(
                cancer_percentage,
                2
            ),
            "non_cancer_confidence": round(
                non_cancer_percentage,
                2
            )
        })
    except Exception as e:
        print("Prediction Error:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=7860
    )
