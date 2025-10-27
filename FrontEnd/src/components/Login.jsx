import React, { useState } from "react";
import axios from "axios";

const Login = ({ setToken }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await axios.post("http://127.0.0.1:5000/login", { username, password });
    setToken(res.data.access_token);
  };

  return (
    <div className="p-6 bg-white rounded-2xl shadow-md">
      <input value={username} onChange={(e)=>setUsername(e.target.value)} placeholder="Username" className="border p-2 w-full rounded mb-2"/>
      <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="Password" className="border p-2 w-full rounded mb-4"/>
      <button onClick={handleSubmit} className="bg-blue-600 text-white p-2 w-full rounded">Login</button>
    </div>
  );
};
export default Login;
