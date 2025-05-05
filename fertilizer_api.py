from flask import Flask, request, jsonify
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load and prepare data
data = pd.read_csv("chittor_final1.csv")
encode_soil = LabelEncoder()
encode_crop = LabelEncoder()
data['Soil_Type'] = encode_soil.fit_transform(data['Soil_type'])
data['Crop_Type'] = encode_crop.fit_transform(data['Crop_type'])

thresholds = {
    'Avail_P': 10, 'Exch_K': 50, 'Avail_Ca': 200, 'Avail_Mg': 50,
    'Avail_S': 10, 'Avail_Zn': 1, 'Avail_B': 0.5, 'Avail_Fe': 4,
    'Avail_Cu': 0.3, 'Avail_N': 5
}
application_rates = {
    'P': 30, 'K': 50, 'Ca': 40, 'Mg': 20, 'S': 25, 'Zn': 5,
    'B': 2, 'Fe': 10, 'Cu': 1, 'N': 4
}

@app.route("/recommend", methods=["POST"])
def recommend():
    content = request.json
    soil_type = content.get("soil_type")
    crop_type = content.get("crop_type")
    land_size = float(content.get("land_size_m2", 0))
    fallow_years = int(content.get("fallow_years", 0))

    row = data[(data['Soil_type'] == soil_type) & (data['Crop_type'] == crop_type)]
    if row.empty:
        return jsonify({"error": "No matching data found"}), 404

    row = row.iloc[0]
    recommendation = {}
    for key in thresholds:
        if row[key] < thresholds[key]:
            nutrient = key.split('_')[-1]
            amount = (application_rates[nutrient] / 10000) * land_size * (1 + 0.1 * fallow_years)
            recommendation[nutrient] = round(amount, 2)

    if recommendation:
        return jsonify({"message": "Fertilizer needed", "recommendation": recommendation})
    else:
        return jsonify({"message": "No deficiency, manure recommended"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
