import React, { useState } from "react";
import axios from "../axiosConfig";

const PredictForm = ({ token }) => {
  const [formData, setFormData] = useState({
    amount: "",
    oldbalanceOrg: "",
    newbalanceOrig: "",
    transactionType: "",
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("/predict", formData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="predict-form">
      <h2>Transaction Prediction</h2>
      <form onSubmit={handleSubmit}>
        <input name="amount" placeholder="Amount" onChange={handleChange} />
        <input name="oldbalanceOrg" placeholder="Old Balance" onChange={handleChange} />
        <input name="newbalanceOrig" placeholder="New Balance" onChange={handleChange} />
        <select name="transactionType" onChange={handleChange}>
          <option value="">Select Type</option>
          <option value="CASH_IN">CASH_IN</option>
          <option value="CASH_OUT">CASH_OUT</option>
          <option value="DEBIT">DEBIT</option>
          <option value="PAYMENT">PAYMENT</option>
          <option value="TRANSFER">TRANSFER</option>
        </select>
        <button type="submit">Predict</button>
      </form>

      {result && (
        <div>
          <p>Prediction: {result.prediction}</p>
          <p>Probability: {result.probability.toFixed(2)}</p>
        </div>
      )}
    </div>
  );
};

export default PredictForm;
