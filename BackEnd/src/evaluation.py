import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# Load model and scaler
model = joblib.load("src/fraud_model.pkl")
scaler = joblib.load("src/scaler.pkl")

# Load dataset
df = pd.read_csv("data/creditcard.csv")

# Prepare data
X = df.drop("Class", axis=1)
y = df["Class"]
X_scaled = scaler.transform(X)

# Predict
y_pred = model.predict(X_scaled)

# Metrics
print("🔹 Classification Report:")
print(classification_report(y, y_pred))

print("\n🔹 Confusion Matrix:")
print(confusion_matrix(y, y_pred))

roc_score = roc_auc_score(y, model.predict_proba(X_scaled)[:, 1])
print(f"\n🔹 ROC-AUC Score: {roc_score:.4f}")
