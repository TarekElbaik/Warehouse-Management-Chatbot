const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

// Enhanced scroll to bottom function - FIXES SCROLL ISSUE
function scrollToBottom() {
  setTimeout(() => {
    chatBox.scrollTop = chatBox.scrollHeight;
  }, 100);
}

// Add message with avatar, timestamp, and type
function appendMessage(sender, text, type = "") {
  const wrapper = document.createElement("div");
  wrapper.classList.add("message-wrapper", sender);

  const avatar = document.createElement("div");
  avatar.classList.add("avatar", sender);
  
  if (sender === "user") {
    avatar.innerHTML = '<i class="fas fa-user"></i>';
  } else {
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
  }

  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  if (type) msg.classList.add(type);
  msg.textContent = text;

  const time = document.createElement("div");
  time.classList.add("timestamp");
  time.textContent = new Date().toLocaleTimeString([], {
    hour: '2-digit', 
    minute: '2-digit'
  });

  msg.appendChild(time);

  if (sender === "user") {
    wrapper.appendChild(msg);
    wrapper.appendChild(avatar);
  } else {
    wrapper.appendChild(avatar);
    wrapper.appendChild(msg);
  }

  chatBox.appendChild(wrapper);
  scrollToBottom(); // Ensures proper scrolling
}

// Enhanced typing indicator
function showTyping() {
  const wrapper = document.createElement("div");
  wrapper.classList.add("message-wrapper", "bot");
  
  const avatar = document.createElement("div");
  avatar.classList.add("avatar", "bot");
  avatar.innerHTML = '<i class="fas fa-robot"></i>';
  
  const typing = document.createElement("div");
  typing.classList.add("typing");
  typing.innerHTML = '<div class="dot3"></div>Typing...';
  
  wrapper.appendChild(avatar);
  wrapper.appendChild(typing);
  chatBox.appendChild(wrapper);
  scrollToBottom(); // Ensures typing indicator is visible
  
  return wrapper;
}

// Enhanced submit handler with better error handling
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  // Add loading state
  form.classList.add("loading");
  
  appendMessage("user", message);
  input.value = "";

  const typingDiv = showTyping();

  try {
    const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender: "user", message }),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();

    // Remove typing indicator
    if (typingDiv && typingDiv.parentNode) {
      chatBox.removeChild(typingDiv);
    }

    // Add bot responses with staggered timing for better UX
    if (data && data.length > 0) {
      data.forEach((msg, index) => {
        setTimeout(() => {
          const type = msg.intent || "fallback";
          appendMessage("bot", msg.text, type);
        }, index * 500); // Stagger messages
      });
    } else {
      appendMessage("bot", "I didn't receive a response. Please try again.", "fallback");
    }
  } catch (err) {
    console.error("Error:", err);
    
    // Remove typing indicator
    if (typingDiv && typingDiv.parentNode) {
      chatBox.removeChild(typingDiv);
    }
    
    appendMessage("bot", "Sorry, I'm having trouble connecting. Please check if the server is running and try again.", "fallback");
  } finally {
    // Remove loading state
    form.classList.remove("loading");
  }
});

// Enhanced input handling with Enter key support
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    form.dispatchEvent(new Event("submit"));
  }
});

// Auto-focus input for better UX
input.focus();

// Welcome message with delay for better presentation
setTimeout(() => {
  appendMessage("bot", "👋 Welcome to the Warehouse Assistant! I can help you check order status, manage inventory, and reschedule deliveries. How can I assist you today?", "greet");
}, 500);
