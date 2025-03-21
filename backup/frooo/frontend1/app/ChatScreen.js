import React, { useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { Audio } from "expo-av";
import * as Speech from "expo-speech";

export default function ChatScreen() {
  const [recording, setRecording] = useState(null);

  const startRecording = async () => {
    try {
      const { granted } = await Audio.requestPermissionsAsync();
      if (!granted) return;
      const newRecording = new Audio.Recording();
      await newRecording.prepareToRecordAsync(Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY);
      await newRecording.startAsync();
      setRecording(newRecording);
    } catch (error) {
      console.error("Error starting recording", error);
    }
  };

  const stopRecording = async () => {
    if (!recording) return;
    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();
    console.log("Recording saved at", uri);
    setRecording(null);
    Speech.speak("Wow, congrats!", { rate: 1.0 });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Chat with Your AI</Text>
      <TouchableOpacity style={styles.button} onPress={recording ? stopRecording : startRecording}>
        <Text style={styles.buttonText}>{recording ? "Stop Recording" : "Start Talking"}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  title: { fontSize: 20, fontWeight: "bold" },
  button: { backgroundColor: "#007AFF", padding: 15, borderRadius: 10, marginTop: 20 },
  buttonText: { color: "#fff", fontSize: 16 },
});
