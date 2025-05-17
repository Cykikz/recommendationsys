# 🌾 KrishiMitra Fertilizer Recommendation API

A simple Flask-based API that provides fertilizer recommendations based on soil and crop type, using nutrient data from the Chittorgarh region.

## 🚀 Features

- Get fertilizer suggestions based on soil and crop type.
- Nutrient classification into **Low**, **Medium**, or **High** for **Nitrogen (N)**, **Phosphorus (P)**, and **Potassium (K)**.
- JSON-based POST request/response.
- Designed to run locally or be deployed to services like Heroku.

---

## 📂 Project Structure
├── fertilizer_api.py # Flask API implementation

├── chittor_final1.csv # Dataset containing soil and crop nutrient information

├── requirements.txt # Python dependencies

├── runtime.txt # Python runtime for deployment (e.g., Railway)

└── Procfile # Deployment instructions for Railway or render or any other

## 🛠 Installation

### Clone the repository

git clone https://github.com/your-username/krishimitra-fertilizer-api.git

cd krishimitra-fertilizer-api

## Install dependencies

pip install -r requirements.txt

## 🧪 Running Locally

python fertilizer_api.py

Go to http://127.0.0.1:5000/ in your browser or use curl or Postman to test the API.

## 📬 API Endpoint
POST /recommend
Request Body (JSON):

{
  "soil_type": "Sandy",
  "crop_type": "Wheat"
}

Response Example:

{
  "soil_type": "sandy",
  
  "crop_type": "wheat",
  
  "recommendation": "Apply NPK fertilizer (Medium Nitrogen, Low Phosphorus, High Potassium)"
}

## 📌 Requirements
Python 3.9.7

Flask 2.0.3

Pandas, NumPy

Waitress (for production WSGI server)

## 📊 Data Source
Dataset used: chittor_final1.csv

Contains soil and crop-specific nutrient values from Chittorgarh district.

## 🙏 Credits
Created and maintained by Harshit Bhatt

GitHub: Cykikzz
