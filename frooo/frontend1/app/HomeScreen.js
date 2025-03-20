import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { useNavigation } from "@react-navigation/native";

export default function HomeScreen() {
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>AI Audio Diary</Text>
      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate("Chat")}>
        <Text style={styles.buttonText}>Start Talking</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#121212" },
  title: { fontSize: 28, fontWeight: "bold", color: "white", marginBottom: 20 },
  button: { backgroundColor: "#1DB954", padding: 15, borderRadius: 10 },
  buttonText: { color: "white", fontSize: 18 }
});
