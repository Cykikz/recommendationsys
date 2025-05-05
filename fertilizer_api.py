from flask import Flask, request, jsonify
import pandas as pd
import logging

# Initialize app and logger
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load CSV
try:
    data = pd.read_csv("chittor_final1.csv")
    logger.info("CSV loaded successfully.")
except Exception as e:
    logger.error(f"Error loading CSV: {e}")
    data = None

# Root route for testing
@app.route("/")
def home():
    return "✅ KrishiMitra API is running!"

# Recommendation route
@app.route("/recommend", methods=["POST"])
def recommend():
    if data is None or data.empty:
        return jsonify({"error": "Data not available"}), 500

    try:
        req = request.get_json()
        soil = req.get("soil_type", "").lower()
        fallow = req.get("fallow_period", "").lower()

        logger.info(f"Filtering for soil: {soil}, fallow: {fallow}")

        filtered = data[
            (data["Soil_type"].str.lower() == soil) &
            (data["Fallow_Period"].str.lower() == fallow)
            ]

        if filtered.empty:
            return jsonify({"error": "No matching crop found"}), 404

        crop = filtered.iloc[0]["Crop_type"]
        return jsonify({"recommended_crop": crop})
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Optional main block for local testing
if __name__ == "__main__":
    app.run(debug=True)
