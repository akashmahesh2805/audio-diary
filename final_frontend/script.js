document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    const burgerIcon = document.getElementById("burger-icon");
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");
    const profileIcon = document.getElementById("profile-icon");
    const profileDropdown = document.getElementById("profile-dropdown");

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
        websocket = new WebSocket("https://fastapi-production-6871.up.railway.app/");

        websocket.onopen = () => console.log("WebSocket connected");
        websocket.onmessage = (event) => handleWebSocketMessage(event);
        websocket.onclose = () => console.log("WebSocket closed, reconnecting...");
    }

    function handleWebSocketMessage(event) {
        try {
            const data = JSON.parse(event.data);
            displayMessage(data.response, "bot");
    
            // Play bot's audio response if available
            if (data.audio_response) {
                playBase64Audio(data.audio_response);
            }
        } catch (error) {
            console.error("Error processing WebSocket message:", error);
        }
    }
    
    // Function to decode Base64 and play audio
    function playBase64Audio(base64Audio) {
        const audio = new Audio(`data:audio/wav;base64,${base64Audio}`);
        audio.play();
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
            sendAudioWithText(transcript);  // Send transcript along with the audio
        };
    
        recognitionInstance.onerror = (event) => console.error("Speech recognition error:", event.error);
        return recognitionInstance;
    }
    

    // Start Recording
    startBtn.addEventListener("click", async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
                const arrayBuffer = await audioBlob.arrayBuffer();
                const base64Audio = await blobToBase64(audioBlob); // Convert to base64
            
                websocket.send(JSON.stringify({ 
                    audio: base64Audio, 
                    text: lastTranscript || ""  // Send last transcript if available
                }));
            
                audioChunks = [];
            };
            

            mediaRecorder.start();
            startBtn.disabled = true;
            stopBtn.disabled = false;

            // Start Speech Recognition
            recognition = initializeSpeechRecognition();
            if (recognition) recognition.start();

        } catch (error) {
            console.error("Microphone access error:", error);
            displayMessage("Please allow microphone access.", "bot");
        }
    });

    // Stop Recording
    stopBtn.addEventListener("click", () => {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
            if (recognition) recognition.stop();  // Stop speech recognition
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
    function blobToBase64(blob) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = () => resolve(reader.result.split(",")[1]); // Extract Base64 part
        });
    }
    
});
