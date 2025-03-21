document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    const burgerIcon = document.getElementById("burger-icon");
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");
    const profileIcon = document.getElementById("profile-icon");
    const profileDropdown = document.getElementById("profile-dropdown");
    <link rel="icon" href="data:;base64,iVBORw0KGgo="></link>
    let mediaRecorder;
    let audioChunks = [];
    let websocket;
    let recognition;

    // Display default bot message
    displayMessage("Hey, tell me about your day!", "bot");

    // Toggle Sidebar
    burgerIcon.addEventListener("click", () => {
        sidebar.classList.toggle("active");
        mainContent.classList.toggle("active");
    });

    // Toggle Profile Dropdown
    profileIcon.addEventListener("click", (event) => {
        event.stopPropagation();
        profileDropdown.classList.toggle("active");
    });

    // Close Profile Dropdown when clicking outside
    document.addEventListener("click", (event) => {
        if (!profileIcon.contains(event.target) && !profileDropdown.contains(event.target)) {
            profileDropdown.classList.remove("active");
        }
    });

    // Connect WebSocket
    function connectWebSocket() {
        websocket = new WebSocket("ws://localhost:8000/audio-stream/");
    
        websocket.onopen = () => {
            console.log("WebSocket connection established");
        };
    
        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            displayMessage(data.response, "bot"); // Display bot's response
    
            // Play the bot's audio response
            const audio = new Audio(`data:audio/wav;base64,${data.audio_response}`);
            audio.play();
        };
    
        websocket.onclose = () => {
            console.log("WebSocket connection closed");
        };
    }

    function handleWebSocketMessage(event) {
        try {
            const data = JSON.parse(event.data);
            displayMessage(data.response, "bot");

            // Play bot's audio response
            if (data.audio_response) {
                const audio = new Audio(`data:audio/wav;base64,${data.audio_response}`);
                audio.play();
            }
        } catch (error) {
            console.error("Error processing WebSocket message:", error);
        }
    }

    // Display messages in chat box
    function displayMessage(message, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", `${sender}-message`);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Initialize Speech Recognition
    function initializeSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            console.error("Speech Recognition API not supported.");
            return null;
        }

        const recognitionInstance = new SpeechRecognition();
        recognitionInstance.continuous = false;
        recognitionInstance.interimResults = false;
        recognitionInstance.lang = "en-US";

        recognitionInstance.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            displayMessage(transcript, "user");
        };

        recognitionInstance.onerror = (event) => console.error("Speech recognition error:", event.error);
        return recognitionInstance;
    }

    // Start recording audio
startBtn.addEventListener("click", async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm; codecs=opus" });

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/webm; codecs=opus" });
            const arrayBuffer = await audioBlob.arrayBuffer();
            websocket.send(arrayBuffer); // Send audio file to the backend
            audioChunks = []; // Reset audio chunks
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

    // Initialize WebSocket
    connectWebSocket();

    // Handle Navigation Links
    document.querySelectorAll(".sidebar ul li a").forEach(link => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            alert(`${link.textContent} page will be implemented soon!`);
        });
    });
});
