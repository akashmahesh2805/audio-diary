import React from "react";
import { View, TouchableOpacity, Text, StyleSheet } from "react-native";

export default function VoiceInput({ onRecord, isRecording }) {
  return (
    <TouchableOpacity style={styles.button} onPress={onRecord}>
      <Text style={styles.text}>{isRecording ? "Stop Recording" : "Start Recording"}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: { padding: 15, backgroundColor: "blue", borderRadius: 8 },
  text: { color: "#fff", fontSize: 16 },
});
