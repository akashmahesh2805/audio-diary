import { useState } from "react";
import { Audio } from "expo-av";

export default function useAudioRecording() {
  const [recording, setRecording] = useState(null);

  const startRecording = async () => {
    const { recording } = await Audio.Recording.createAsync(Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY);
    setRecording(recording);
  };

  const stopRecording = async () => {
    await recording.stopAndUnloadAsync();
    return recording.getURI();
  };

  return { startRecording, stopRecording };
}
