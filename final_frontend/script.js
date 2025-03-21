const chatBox = document.getElementById("chat-box");
const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const burgerIcon = document.getElementById("burger-icon");
const sidebar = document.getElementById("sidebar");
const mainContent = document.getElementById("main-content");
const profileIcon = document.getElementById("profile-icon");
const profileDropdown = document.getElementById("profile-dropdown");

let mediaRecorder;
let websocket;

// Display a default message from the bot
displayMessage("Hey, tell me about your day!", "bot");

// Toggle Sidebar
burgerIcon.addEventListener("click", () => {
    sidebar.classList.toggle("active");
    mainContent.classList.toggle("active");
});

// Toggle Profile Dropdown
profileIcon.addEventListener("click", () => {
    profileDropdown.classList.toggle("active");
});

// Close Dropdown when clicking outside
document.addEventListener("click", (event) => {
    if (!profileIcon.contains(event.target) && !profileDropdown.contains(event.target)) {
        profileDropdown.classList.remove("active");
    }
});

// WebSocket connection
function connectWebSocket() {
    websocket = new WebSocket("ws://localhost:8000/audio-stream/");

    websocket.onopen = () => {
        console.log("WebSocket connection established");
    };

    websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        displayMessage(data.transcription, "user"); // Display user's transcribed message
        displayMessage(data.response, "bot"); // Display bot's response

        // Play the bot's audio response
        const audio = new Audio(`data:audio/wav;base64,${data.audio_response}`);
        audio.play();
    };

    websocket.onclose = () => {
        console.log("WebSocket connection closed");
    };
}

// Display messages in the chat box
function displayMessage(message, sender) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", `${sender}-message`);
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Start recording audio
startBtn.addEventListener("click", async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });

        mediaRecorder.ondataavailable = async (event) => {
            if (event.data.size > 0) {
                const arrayBuffer = await event.data.arrayBuffer();
                websocket.send(arrayBuffer); // Send audio chunk to the backend
            }
        };

        mediaRecorder.start(1000); // Send chunks every 1 second
        startBtn.disabled = true;
        stopBtn.disabled = false;
    } catch (error) {
        console.error("Error accessing microphone:", error);
        displayMessage("Unable to access microphone. Please allow permissions.", "bot");
    }
});

// Stop recording audio
stopBtn.addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
});

// Initialize WebSocket connection when the page loads
connectWebSocket();

// Handle navigation links
document.getElementById("home-link").addEventListener("click", (e) => {
    e.preventDefault();
    alert("Home page will be implemented soon!");
});

document.getElementById("diary-link").addEventListener("click", (e) => {
    e.preventDefault();
    alert("Diary Entries page will be implemented soon!");
});

document.getElementById("stats-link").addEventListener("click", (e) => {
    e.preventDefault();
    alert("Emotion Stats page will be implemented soon!");
});

document.getElementById("settings-link").addEventListener("click", (e) => {
    e.preventDefault();
    alert("Settings page will be implemented soon!");
});