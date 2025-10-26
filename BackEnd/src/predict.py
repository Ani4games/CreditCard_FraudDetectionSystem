import joblib
import numpy as np

def predict_transaction(transaction):
    model = joblib.load("src/fraud_model.pkl")
    scaler = joblib.load("src/scaler.pkl")

    # transaction = list of features (Amount, V1..V28, Time)
    transaction_scaled = scaler.transform([transaction])
    prediction = model.predict(transaction_scaled)[0]
    probability = model.predict_proba(transaction_scaled)[0][1]

    return prediction, probability

if __name__ == "__main__":
    # Example test (dummy values, adjust to dataset)
    sample = np.random.rand(30)  # dataset has 30 features (Time + V1–V28 + Amount)
    pred, prob = predict_transaction(sample)
    print(f"Prediction: {'Fraud' if pred==1 else 'Normal'}, Probability: {prob:.4f}")
