from flask import Flask, request, jsonify
import mlflow
import mlflow.sklearn
import numpy as np

app = Flask(__name__)

MLFLOW_URI = "http://localhost:5000"
MODEL_NAME = "iris-classifier"
mlflow.set_tracking_uri(MLFLOW_URI)

# Load Champion model at startup
model = None

def load_champion_model():
    global model
    try:
        model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@Champion")
        print("[API] Champion model loaded successfully")
    except Exception as e:
        print(f"[API] Could not load Champion model: {e}")
        model = None

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "running",
        "project": "MLOps Project 2",
        "student": "Syed Aun Ali Kazmi",
        "SAP": "70149156",
        "model": MODEL_NAME,
        "endpoint": "/predict"
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    if not data or 'features' not in data:
        return jsonify({
            "error": "Missing 'features' in request body",
            "expected_format": {
                "features": [5.1, 3.5, 1.4, 0.2]
            }
        }), 400

    features = data['features']
    if len(features) != 4:
        return jsonify({
            "error": "Exactly 4 features required",
            "received": len(features),
            "features": ["sepal length", "sepal width", "petal length", "petal width"]
        }), 400

    input_array = np.array(features).reshape(1, -1)
    prediction = model.predict(input_array)[0]
    probability = model.predict_proba(input_array)[0].tolist()

    class_names = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}

    return jsonify({
        "prediction": int(prediction),
        "class_name": class_names[int(prediction)],
        "probabilities": {
            "Setosa": round(probability[0], 4),
            "Versicolor": round(probability[1], 4),
            "Virginica": round(probability[2], 4)
        },
        "input_features": {
            "sepal_length": features[0],
            "sepal_width": features[1],
            "petal_length": features[2],
            "petal_width": features[3]
        },
        "model": MODEL_NAME,
        "alias": "Champion"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

if __name__ == '__main__':
    load_champion_model()
    app.run(host='0.0.0.0', port=7000, debug=False)
