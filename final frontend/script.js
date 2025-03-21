// Sidebar Toggle
const sidebar = document.getElementById("sidebar");
const burgerMenu = document.getElementById("burger-menu");
const closeBtn = document.getElementById("close-btn");

burgerMenu.addEventListener("click", () => {
    sidebar.classList.add("active");
});

closeBtn.addEventListener("click", () => {
    sidebar.classList.remove("active");
});

// Handle Sidebar Links
const sidebarLinks = document.querySelectorAll(".sidebar-menu a");
sidebarLinks.forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        alert(`Navigating to: ${link.textContent}`);
        sidebar.classList.remove("active");
    });
});

// Profile Icon Click
const profileIcon = document.getElementById("profile-icon");
profileIcon.addEventListener("click", () => {
    alert("Profile Page");
});

// Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = "en-US";

const chatWindow = document.getElementById("chat-window");
const micButton = document.getElementById("mic-button");

// Add Messages to Chat
function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.innerText = text;
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to latest message
}

// AI Response (Simulated Emotion Detection)
function getBotResponse(userText) {
    const lowerText = userText.toLowerCase();
    
    if (lowerText.includes("happy") || lowerText.includes("won") || lowerText.includes("excited")) {
        return "Wow, congrats! 🎉 That’s amazing!";
    } else if (lowerText.includes("sad") || lowerText.includes("upset") || lowerText.includes("lonely")) {
        return "I'm here for you. Want to talk about it? 💙";
    } else if (lowerText.includes("angry") || lowerText.includes("frustrated")) {
        return "Take a deep breath! Want some calming music? 🌿";
    } else {
        return "That's interesting! Tell me more. 🤔";
    }
}

// Start Listening on Button Click
micButton.addEventListener("click", () => {
    recognition.start();
    micButton.style.transform = "scale(1.1)";
    setTimeout(() => {
        micButton.style.transform = "scale(1)";
    }, 200);
});

// Handle Speech Recognition Result
recognition.onresult = (event) => {
    const userText = event.results[0][0].transcript;
    addMessage(userText, "user");

    // Get Bot Response
    const botResponse = getBotResponse(userText);
    setTimeout(() => {
        addMessage(botResponse, "bot");
    }, 1000);
};

// Handle Errors
recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
};