import React from "react";
import { View, Text, StyleSheet } from "react-native";

export default function ChatBubble({ text, isUser }) {
  return (
    <View style={[styles.bubble, isUser ? styles.userBubble : styles.aiBubble]}>
      <Text style={styles.text}>{text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  bubble: { padding: 10, borderRadius: 10, marginVertical: 5, maxWidth: "70%" },
  userBubble: { backgroundColor: "#007AFF", alignSelf: "flex-end" },
  aiBubble: { backgroundColor: "#E0E0E0", alignSelf: "flex-start" },
  text: { fontSize: 16 },
});
