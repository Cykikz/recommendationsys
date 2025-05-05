from flask import Flask, request, jsonify
import pandas as pd
import logging

# Enable debug-level logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load CSV at startup
try:
    data = pd.read_csv("chittor_final1.csv")
    logger.info("CSV file loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load CSV: {e}")
    data = None  # Prevents app from crashing completely

# Root test route
@app.route("/")
def home():
    return "✅ KrishiMitra Flask API is running!"

@app.route("/recommend", methods=["POST"])
def recommend_crop():
    if not data:
        return jsonify({"error": "Data not available"}), 500

    try:
        req = request.get_json()
        soil_type = req.get("soil_type")
        fallow_period = req.get("fallow_period")

        filtered = data[
            (data["Soil Type"].str.lower() == soil_type.lower()) &
            (data["Fallow Period"].str.lower() == fallow_period.lower())
            ]

        if filtered.empty:
            return jsonify({"error": "No matching data found"}), 404

        crop = filtered.iloc[0]["Crop"]
        return jsonify({"recommended_crop": crop})
    except Exception as e:
        logger.error(f"Error in /recommend: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

