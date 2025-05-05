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
    data.columns = data.columns.str.strip()  # Clean column names (remove extra spaces)
    logger.info(f"CSV Columns: {data.columns.tolist()}")
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
    if not data:
        return jsonify({"error": "Data not available"}), 500

    try:
        req = request.get_json()
        soil = req.get("soil_type", "").lower()  # Get soil_type from request
        fallow = req.get("fallow_period", "").lower()  # Get fallow_period from request

        # Filter using correct column names
        filtered = data[
            (data["Soil_type"].str.lower() == soil) &  # Correct column name
            (data["Fallow Period"].str.lower() == fallow)  # Correct column name
            ]

        if filtered.empty:
            return jsonify({"error": "No matching crop found"}), 404

        crop = filtered.iloc[0]["Crop_type"]  # Correct column name
        return jsonify({"recommended_crop": crop})
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Optional main block for local testing
if __name__ == "__main__":
    app.run(debug=True)
