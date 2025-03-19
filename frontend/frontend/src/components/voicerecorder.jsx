// src/components/VoiceRecorder.jsx
import React, { useState } from "react";
import { ReactMic } from "react-mic";
import axios from "axios";

const VoiceRecorder = ({ onAnalysis }) => {
  const [recording, setRecording] = useState(false);

  const startRecording = () => setRecording(true);
  const stopRecording = () => setRecording(false);

  const onData = (recordedData) => {
    console.log("Recording in progress:", recordedData);
  };

  const onStop = async (recordedData) => {
    console.log("Recording stopped:", recordedData);
    const audioBlob = recordedData.blob;

    // Send audio to the backend
    const formData = new FormData();
    formData.append("file", audioBlob);

    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze_voice/", formData);
      onAnalysis(response.data.emotion); // Send result to parent component
    } catch (error) {
      console.error("Error uploading audio:", error);
    }
  };

  return (
    <div>
      <h2>🎤 Record Your Voice Diary</h2>
      <ReactMic
        record={recording}
        onStop={onStop}
        onData={onData}
        mimeType="audio/wav"
        strokeColor="#000000"
        backgroundColor="#FFDDC1"
      />
      <button onClick={startRecording}>Start Recording</button>
      <button onClick={stopRecording}>Stop Recording</button>
    </div>
  );
};

export default VoiceRecorder;

