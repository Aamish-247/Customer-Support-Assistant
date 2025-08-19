

const chatMessages = document.getElementById('chat-message'); // Your chat messages container
const userInput = document.getElementById('user_message');
const sendButton = document.getElementById('send_button');
const exitButton = document.getElementById('exit_button'); // Assuming you have an Exit button


// Typing animation is rendered as a standalone placeholder (not a message bubble)


const PROCESSING_ANIMATION_URL = "/static/robot process automation.json";

const STORAGE_KEY = "chatHistory";

// --- Backend API Endpoint ---
// Use relative path so it works both locally (when proxied) and on Railway
const API_URL = "/chat"; // FastAPI chat endpoint on the same host
// If hosting backend on a different domain, replace with full URL

// --- User ID (for session management with backend) ---
let currentUserId = localStorage.getItem('chatbot_user_id');
if (!currentUserId) {
    currentUserId = ""; // Backend will generate if null/empty
    // We will set it in localStorage once the first response with a user_id comes back
}
console.log("Current User ID (initial):", currentUserId);

function loadChatFromStorage() {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
}
  
  // localStorage me messages save karna
function saveChatToStorage(messages) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
}

let messages = loadChatFromStorage(); // purane messages load ho gaye

function addMessage(role, content) {
  messages.push({ role, content });   
  saveChatToStorage(messages);        
  renderMessages();                   
}

function renderMessages() {
    const messagesList = document.getElementById("chat-message");
    messagesList.innerHTML = ""; 

    for (const m of messages) {
        // 1. Create the wrapper div
        const messageWrapper = document.createElement("div");
        messageWrapper.classList.add("message-wrapper");

        // Add sender-specific class for alignment
        if (m.role === "user") {
            messageWrapper.classList.add("user-message");
        } else if (m.role === "bot") {
            messageWrapper.classList.add("bot-message");
        }

        // 2. Create the actual message bubble div
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message");

        const paragraph = document.createElement("p");
        paragraph.textContent = m.content;

        messageDiv.appendChild(paragraph);
        messageWrapper.appendChild(messageDiv);

        messagesList.appendChild(messageWrapper);
    }

    // Scroll to the bottom after rendering
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

window.addEventListener("load", () => {
    renderMessages();  // reload ke time purane messages dikh jaenge
});

// --- Helper Function to Display Messages ---
function displayMessage(message, sender, animate = false) {

    messages.push({ role: sender, content: message });
    saveChatToStorage(messages);
    
    // 1. Create the wrapper div
    const messageWrapper = document.createElement('div');
    messageWrapper.classList.add('message-wrapper'); // Add the wrapper class

    // Add sender-specific class to the wrapper for alignment
    if (sender === 'user') {
        messageWrapper.classList.add('user-message');
    } else if (sender === 'bot') {
        messageWrapper.classList.add('bot-message');
    }

    // 2. Create the actual message bubble div
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message'); // Always add 'message' class for the bubble

    const paragraph = document.createElement('p');
    paragraph.textContent = message;

    messageDiv.appendChild(paragraph);
    messageWrapper.appendChild(messageDiv); // Append the message bubble inside the wrapper

    chatMessages.appendChild(messageWrapper); // Append the wrapper to the chat container

    // Scroll to the latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Optional: Add simple animation for new messages
    if (animate) {
        // Apply animation to the wrapper for a cleaner effect
        messageWrapper.style.opacity = 0;
        messageWrapper.style.transform = 'translateY(20px)';
        setTimeout(() => {
            messageWrapper.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            messageWrapper.style.opacity = 1;
            messageWrapper.style.transform = 'translateY(0)';
        }, 50); // Small delay for effect
    }

    // Debug: Log the classes to console
    console.log('Message wrapper classes:', messageWrapper.classList.toString());
    console.log('Sender:', sender);
}


function showTypingPlaceholder() {
    const placeholder = document.createElement('div');
    placeholder.classList.add('reply-placeholder');

    const player = document.createElement('lottie-player');
    player.classList.add('reply-anim');
    player.setAttribute('src', PROCESSING_ANIMATION_URL);
    player.setAttribute('background', 'transparent');
    player.setAttribute('speed', '1');
    player.setAttribute('loop', 'true');
    player.setAttribute('autoplay', 'true');

    placeholder.appendChild(player);
    chatMessages.appendChild(placeholder);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return placeholder;
}

function removeTypingPlaceholder(node) {
    if (node && node.parentNode) {
        node.parentNode.removeChild(node);
    }
}



// --- Main Send Message Function ---
async function sendMessage() {
    let typingNode = null;
    try {
        const message = userInput.value.trim();
        if (message === '') return;

        displayMessage(message, 'user', true);
        userInput.value = '';

        // Show bot typing animation exactly where the reply will appear (not a bubble)
        typingNode = showTypingPlaceholder();

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_input: message,
                user_id: currentUserId
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('API Error:', errorData);
            throw new Error(`Server error: ${errorData.detail.message || response.statusText}`);
        }

        const data = await response.json();
        console.log("Backend Response:", data);

        if (data.user_id && data.user_id !== currentUserId) {
            currentUserId = data.user_id;
            localStorage.setItem('chatbot_user_id', currentUserId);
            console.log("Updated User ID:", currentUserId);
        }

        // Replace typing placeholder with actual bot message
        removeTypingPlaceholder(typingNode);
        typingNode = null;
        displayMessage(data.response, 'bot', true);
    }
    catch (error) 
    {
        console.error('Error sending message:', error);
        removeTypingPlaceholder(typingNode);
        displayMessage("Sorry, something went wrong. Please try again.", 'bot', true);
    } 
    finally 
    {
        // nothing here; typing bubble is handled above
    }
}


// --- Event Listeners ---
sendButton.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (event) => { // <-- YEH HAI AAPKA KEYPRESS EVENT LISTENER
    if (event.key === 'Enter') { //
        event.preventDefault(); // <-- YEH LINE YAHAN ADD KAREIN!
        sendMessage(); //
    }
});

exitButton.addEventListener('click', () => {
    if (confirm("Are you sure you want to exit the chat?")) {

        localStorage.removeItem(STORAGE_KEY);
        // Redirect to home page
        window.location.href = '/'; 
    }
});

