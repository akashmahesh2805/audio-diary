// src/components/AnalysisResult.jsx
import React from "react";

const AnalysisResult = ({ emotion }) => {
  if (!emotion) return null;

  return (
    <div>
      <h3>🧠 Analysis Result</h3>
      <p>Your emotion is detected as: <strong>{emotion}</strong></p>
    </div>
  );
};

export default AnalysisResult;
