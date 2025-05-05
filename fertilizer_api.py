from flask import Flask, request, jsonify
import pandas as pd
import logging

# Initialize Flask app and logger
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

# Root route for health check
@app.route("/")
def home():
    return "✅ KrishiMitra Fertilizer API is running!"

# Fertilizer recommendation route
@app.route("/recommend", methods=["POST"])
def recommend_fertilizer():
    if data is None or data.empty:
        return jsonify({"error": "Data not available"}), 500

    try:
        req = request.get_json()
        soil = req.get("soil_type", "").strip().lower()
        crop = req.get("crop_type", "").strip().lower()

        logger.debug(f"Request received: soil_type={soil}, crop_type={crop}")

        # Filter based on soil and crop
        filtered = data[
            (data["Soil_type"].str.lower() == soil) &
            (data["Crop_type"].str.lower() == crop)
            ]

        if filtered.empty:
            return jsonify({"error": "No matching data found"}), 404

        # Get average nutrient values for the match
        nutrient_data = filtered[["Avail_N", "Avail_P", "Exch_K"]].mean()

        def classify(value, nutrient_type):
            if nutrient_type == "N":
                return "Low" if value < 100 else "Medium" if value < 250 else "High"
            elif nutrient_type == "P":
                return "Low" if value < 10 else "Medium" if value < 25 else "High"
            elif nutrient_type == "K":
                return "Low" if value < 100 else "Medium" if value < 200 else "High"

        n_status = classify(nutrient_data["Avail_N"], "N")
        p_status = classify(nutrient_data["Avail_P"], "P")
        k_status = classify(nutrient_data["Exch_K"], "K")

        recommendation = f"Apply NPK fertilizer ({n_status} Nitrogen, {p_status} Phosphorus, {k_status} Potassium)"

        return jsonify({
            "soil_type": soil,
            "crop_type": crop,
            "recommendation": recommendation
        })

    except Exception as e:
        logger.error(f"Fertilizer recommendation error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Run locally (optional)
if __name__ == "__main__":
    app.run(debug=True)
