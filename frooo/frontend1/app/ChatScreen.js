import { useState, useEffect } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { Audio } from "expo-av";
import Voice from "@react-native-voice/voice"; // Install using `npm install @react-native-voice/voice`
import axios from "axios"; // Install using `npm install axios`
import { useNavigation } from "@react-navigation/native";

export default function ChatScreen() {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const navigation = useNavigation();

  useEffect(() => {
    Voice.onSpeechResults = (event) => setTranscript(event.value[0]);
    return () => Voice.destroy().then(Voice.removeAllListeners);
  }, []);

  const startRecording = async () => {
    setRecording(true);
    await Voice.start("en-US");
  };

  const stopRecording = async () => {
    setRecording(false);
    await Voice.stop();
    analyzeEmotion(transcript);
  };

  const analyzeEmotion = async (text) => {
    try {
      const { data } = await axios.post("http://your-backend-url/analyze", { text });
      setResponse(data.response);
    } catch (error) {
      setResponse("Error detecting emotion.");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Talk About Your Day</Text>
      <TouchableOpacity
        style={recording ? styles.buttonRecording : styles.button}
        onPress={recording ? stopRecording : startRecording}
      >
        <Text style={styles.buttonText}>{recording ? "Stop Recording" : "Start Talking"}</Text>
      </TouchableOpacity>
      <Text style={styles.transcript}>🗣 {transcript}</Text>
      <Text style={styles.response}>🤖 {response}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#222" },
  title: { fontSize: 22, color: "white", marginBottom: 20 },
  button: { backgroundColor: "#1DB954", padding: 15, borderRadius: 10 },
  buttonRecording: { backgroundColor: "#FF3D00", padding: 15, borderRadius: 10 },
  buttonText: { color: "white", fontSize: 18 },
  transcript: { color: "white", fontSize: 16, marginTop: 20 },
  response: { color: "#1DB954", fontSize: 18, marginTop: 10 }
});
