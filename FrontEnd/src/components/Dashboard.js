import React, { useEffect, useState } from "react";
import axios from "axiosConfig";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = ["#0088FE", "#FF8042"];

const Dashboard = () => {
  const [stats, setStats] = useState({ fraud: 0, legit: 0 });

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/stats")
      .then((res) => setStats(res.data))
      .catch((err) => console.error("Error fetching stats:", err));
  }, []);

  const data = [
    { name: "Fraud", value: stats.fraud },
    { name: "Legit", value: stats.legit },
  ];

  return (
    <div className="bg-white shadow-md rounded-2xl p-6 w-full max-w-lg mt-6">
      <h2 className="text-2xl font-semibold mb-4 text-gray-700">Fraud vs Legit</h2>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            dataKey="value"
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#8884d8"
            label
          >
            {data.map((entry, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Dashboard;
