import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from preprocessing import load_and_preprocess

def train_and_save_model():
    X_train, X_test, y_train, y_test, scaler = load_and_preprocess()

    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save model + scaler
    joblib.dump(model, "fraud_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    print("✅ Model and Scaler saved!")

if __name__ == "__main__":
    train_and_save_model()
