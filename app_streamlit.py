import streamlit as st
import numpy as np
import pandas as pd
import joblib
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import os

#Exception handling for missing files
def load_resource(file_path):
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return None
    if os.path.getsize(file_path) == 0:
        st.error(f"File is empty (0 bytes): {file_path}")
        return None
    try:
        return joblib.load(file_path)
    except EOFError:
        st.error(f"EOFError: {file_path} is corrupted or incomplete.")
        return None
# -----------------------------
# Load model and scaler
# -----------------------------
model = load_resource("src/fraud_model.pkl")
scaler = load_resource("src/scaler.pkl")
if model is None or scaler is None:
    st.stop()

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(page_title="Credit Card Fraud Detection", layout="wide")
st.title("💳 Credit Card Fraud Detection System")

menu = ["Transaction Checker", "Admin Dashboard"]
choice = st.sidebar.selectbox("Navigation", menu)

# -----------------------------
# Transaction Checker Page
# -----------------------------
if choice == "Transaction Checker":
    st.subheader("🔍 Single Transaction Fraud Check")

    st.info("Enter the transaction details below (30 features: Time, V1–V28, Amount).")

    input_values = []
    cols = st.columns(3)
    for i in range(30):
        with cols[i % 3]:
            val = st.number_input(f"Feature {i+1}", value=0.0, step=0.01)
            input_values.append(val)

    if st.button("Predict"):
        X_scaled = scaler.transform([input_values])
        pred = model.predict(X_scaled)[0]
        prob = model.predict_proba(X_scaled)[0][1]

        st.success(f"**Result:** {'🚨 Fraud' if pred == 1 else '✅ Normal'}")
        st.metric("Fraud Probability", f"{prob*100:.2f}%")

# -----------------------------
# Admin Dashboard Page
# -----------------------------
elif choice == "Admin Dashboard":
    st.subheader("📊 Batch Fraud Analysis")

    uploaded_file = st.file_uploader("Upload Transactions CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview:", df.head())

        X_scaled = scaler.transform(df)
        preds = model.predict(X_scaled)
        probs = model.predict_proba(X_scaled)[:, 1]

        df["Fraud_Prediction"] = preds
        df["Fraud_Probability"] = probs

        st.write("Predictions:")
        st.dataframe(df.head())

        # Visualization
        st.subheader("Fraud Distribution")
        sns.countplot(x=df["Fraud_Prediction"])
        st.pyplot(plt.gcf())
        plt.clf()

        fraud_count = (df["Fraud_Prediction"] == 1).sum()
        total = len(df)
        st.info(f"Fraudulent Transactions: {fraud_count}/{total} ({fraud_count/total*100:.2f}%)")

        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results", csv, "fraud_predictions.csv", "text/csv")
