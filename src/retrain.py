import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def retrain_model(new_data_path="data/retrain_data.csv"):
    df = pd.read_csv(new_data_path)
    X = df.drop("Class", axis=1)
    y = df["Class"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)

    joblib.dump(model, "src/fraud_model.pkl")
    joblib.dump(scaler, "src/scaler.pkl")
    print("✅ Model retrained and saved successfully!")

if __name__ == "__main__":
    retrain_model()
