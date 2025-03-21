// Elements
const micButton = document.getElementById("micButton");
const chatContainer = document.getElementById("chatContainer");
const micCircle = document.getElementById("micCircle");

let mediaRecorder;
let audioContext;
let analyser;
let dataArray;
let ws;
let isRecording = false;
let silenceTimeout;

// Function to start recording
async function startRecording() {
    if (isRecording) return;
    isRecording = true;

    // Clear any previous WebSocket connection
    if (ws) {
        ws.close();
    }

    ws = new WebSocket("ws://localhost:8000/audio-stream/");
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
        console.log("WebSocket connected.");
    };

    ws.onmessage = async (event) => {
        let response = JSON.parse(event.data);
        if (response.type === "text") {
            addChatMessage("bot", response.text);
        } else if (response.type === "audio") {
            playAudio(response.audio_url);
        }
    };

    ws.onerror = (error) => {
        console.error("WebSocket Error:", error);
    };

    ws.onclose = () => {
        console.log("WebSocket closed.");
        stopMicAnimation();
    };

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioContext.createMediaStreamSource(stream);
        
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
        source.connect(analyser);

        mediaRecorder = new MediaRecorder(stream);
        let chunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                ws.send(event.data);
                chunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            ws.send(JSON.stringify({ type: "end" }));
            stream.getTracks().forEach(track => track.stop());
            stopMicAnimation();
        };

        mediaRecorder.start(250);
        startMicAnimation();

        detectSilence(stream);
    } catch (error) {
        console.error("Error accessing microphone:", error);
        isRecording = false;
    }
}

// Function to detect silence
function detectSilence(stream) {
    const threshold = 0.02;
    function checkSilence() {
        analyser.getByteFrequencyData(dataArray);
        let avgVolume = dataArray.reduce((sum, val) => sum + val, 0) / dataArray.length;

        if (avgVolume < threshold * 255) {
            clearTimeout(silenceTimeout);
            silenceTimeout = setTimeout(stopRecording, 2000);
        } else {
            clearTimeout(silenceTimeout);
        }

        if (isRecording) {
            requestAnimationFrame(checkSilence);
        }
    }
    checkSilence();
}

// Function to stop recording
function stopRecording() {
    if (!isRecording) return;
    isRecording = false;

    mediaRecorder.stop();
    if (ws) ws.close();
}

// Function to start mic animation
function startMicAnimation() {
    micCircle.classList.add("listening");
    function animate() {
        if (!isRecording) return;
        analyser.getByteFrequencyData(dataArray);
        let volume = dataArray.reduce((sum, val) => sum + val, 0) / dataArray.length;
        let scale = Math.max(1, 1 + volume / 100);
        micCircle.style.transform = `scale(${scale})`;
        requestAnimationFrame(animate);
    }
    animate();
}

// Function to stop mic animation
function stopMicAnimation() {
    micCircle.classList.remove("listening");
    micCircle.style.transform = "scale(1)";
}

// Function to play audio
function playAudio(url) {
    let audio = new Audio(url);
    audio.play();
}

// Function to add messages to chat
function addChatMessage(sender, message) {
    let msgDiv = document.createElement("div");
    msgDiv.classList.add(sender === "user" ? "user-message" : "bot-message");
    msgDiv.textContent = message;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Event listener for mic button
micButton.addEventListener("click", () => {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
});
