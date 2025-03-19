// src/components/MoodTrends.jsx
import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";

const MoodTrends = ({ moodData }) => {
  return (
    <div>
      <h3>📊 Mood Trends</h3>
      <LineChart width={400} height={250} data={moodData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="emotion" stroke="#82ca9d" />
      </LineChart>
    </div>
  );
};

export default MoodTrends;
