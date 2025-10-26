from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
from .auth import auth_bp, bcrypt
from .db import db
from .models import Transaction
import joblib, numpy as np

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///transactions.db"
app.config["JWT_SECRET_KEY"] = "super-secret-key"
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/auth")

model = joblib.load("src/fraud_model.pkl")
scaler = joblib.load("src/scaler.pkl")

transaction_type_map = {
    "CASH_IN": 0, "CASH_OUT": 1, "DEBIT": 2, "PAYMENT": 3, "TRANSFER": 4
}

prediction_log = {"fraud": 0, "legit": 0}

@app.route("/")
def home():
    return jsonify({"message": "Fraud Detection API is running 🚀"})

@app.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    data = request.get_json()
    features = np.array([
        float(data["amount"]),
        float(data["oldbalanceOrg"]),
        float(data["newbalanceOrig"]),
        transaction_type_map[data["transactionType"]]
    ]).reshape(1, -1)

    features_scaled = scaler.transform(features)
    pred = model.predict(features_scaled)[0]
    prob = model.predict_proba(features_scaled)[0][1]

    label = "Fraud" if pred == 1 else "Legit"
    new_tx = Transaction(
        amount=data["amount"],
        oldbalanceOrg=data["oldbalanceOrg"],
        newbalanceOrig=data["newbalanceOrig"],
        transactionType=data["transactionType"],
        result=label,
        probability=prob
    )
    db.session.add(new_tx)
    db.session.commit()

    prediction_log[label.lower()] += 1
    return jsonify({"result": label, "probability": prob})

@app.route("/stats", methods=["GET"])
@jwt_required()
def stats():
    return jsonify(prediction_log)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
