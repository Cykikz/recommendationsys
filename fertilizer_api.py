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
    # Check if the data is available
    if data is None or data.empty:
        logger.error("Data not loaded or is empty")
        return jsonify({"error": "Data not available"}), 500

    try:
        # Get JSON request from the client
        req = request.get_json()
        logger.debug(f"Request received: {req}")

        # Extract soil type and fallow period from the request
        soil = req.get("soil_type", "").lower()
        fallow = req.get("fallow_period", "").lower()

        # Filter data based on soil type and fallow period
        logger.debug(f"Filtering data for soil_type={soil} and fallow_period={fallow}")

        filtered = data[
            (data["Soil_type"].str.lower() == soil) &
            (data["Fallow_period"].str.lower() == fallow)
            ]

        if filtered.empty:
            logger.warning(f"No match found for soil_type={soil} and fallow_period={fallow}")
            return jsonify({"error": "No matching crop found"}), 404

        # Get the recommended crop
        crop = filtered.iloc[0]["Crop_type"]
        logger.debug(f"Recommended crop: {crop}")

        # Return the recommended crop as a JSON response
        return jsonify({"recommended_crop": crop})

    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Optional main block for local testing
if __name__ == "__main__":
    app.run(debug=True)
