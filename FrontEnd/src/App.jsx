import React, { useState } from "react";
import LoginForm from "./components/LoginForm"
import PredictForm from "./components/PredictForm";
import Dashboard from "./components/Dashboard";

function App() {
  const [view, setView] = useState("predict");
  const [token, setToken] = useState(null);
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-8">
      <h1 className="text-3xl font-bold mb-6 text-blue-600">
        Credit Card Fraud Detection
      </h1>

      <div className="flex space-x-4 mb-6">
        <button
          onClick={() => setView("predict")}
          className={`px-4 py-2 rounded-lg ${
            view === "predict"
              ? "bg-blue-600 text-white"
              : "bg-white border border-gray-300"
          }`}
        >
          Predict
        </button>
        <button
          onClick={() => setView("dashboard")}
          className={`px-4 py-2 rounded-lg ${
            view === "dashboard"
              ? "bg-blue-600 text-white"
              : "bg-white border border-gray-300"
          }`}
        >
          Dashboard
        </button>
      </div>

      {view === "predict" ? <PredictForm /> : <Dashboard />}
    </div>
  );

}
const [token, setToken] = useState(null);

if (!token) return <Login setToken={setToken} />;

// Then attach token to axios calls
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
return (
    <div className="App">
      <nav>
        <button onClick={() => setView("predict")}>Predict</button>
        <button onClick={() => setView("dashboard")}>Dashboard</button>
      </nav>
      {view === "predict" ? <PredictForm token={token} /> : <Dashboard token={token} />}
    </div>
  );


export default App;
