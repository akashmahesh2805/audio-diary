// src/App.jsx
import React, { useState } from "react";
import VoiceRecorder from "./components/VoiceRecorder";
import Analysis from "./components/Analysis";
import MoodTrends from "./components/MoodTrends";
import "./App.css";

function App() {
  const [audioData, setAudioData] = useState(null);

  return (
    <div className="app">
      <h1>AI-Based Mental Health Diary</h1>
      <VoiceRecorder onRecordingComplete={(data) => setAudioData(data)} />
      <Analysis audioData={audioData} />
      <MoodTrends />
    </div>
  );
}

export default App;
