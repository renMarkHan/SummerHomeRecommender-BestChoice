/**
 * Chat Module
 * Responsible for handling chat logic, message management and communication with LLM API
 */

/**
 * Format timestamp for display
 */
function formatTimestamp(date) {
    return date.toLocaleTimeString();
}

// Chat State Management
const CHAT_STATE = {
    // Chat history
    messageHistory: [],
    
    // Current session ID
    sessionId: null,
    
    // Whether waiting for response
    isWaitingForResponse: false,
    
    // Message counter
    messageCount: 0,
    
    // Error retry count
    retryCount: 0,
    
    // Maximum retry attempts
    maxRetries: 3
};

/**
 * Chat Configuration
 */
const CHAT_CONFIG = {
    // Maximum message history length
    maxHistoryLength: 50,
    
    // Message types
    messageTypes: {
        USER: 'user',
        BOT: 'bot',
        SYSTEM: 'system',
        ERROR: 'error'
    },
    
    // Default system prompt
    defaultSystemPrompt: 'You are a professional vacation property recommendation assistant who can help users find ideal vacation properties. Please answer user questions in a friendly and professional tone.',
    
    // Error message templates
    errorMessages: {
        network: 'Network connection failed, please check network settings',
        timeout: 'Request timeout, please try again later',
        server: 'Server error, please try again later',
        unknown: 'Unknown error occurred, please try again later'
    }
};

/**
 * Initialize chat module
 */
function initChat() {
    console.log('Initializing chat module...');
    
    // Load chat history
    loadChatHistory();
    
    // Listen for send message events
    document.addEventListener('sendMessage', handleSendMessage);
    
    // Listen for profile save events
    document.addEventListener('saveProfile', handleSaveProfile);
    
    console.log('Chat module initialization complete');
}

/**
 * Generate session ID
 */
function generateSessionId() {
    CHAT_STATE.sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    console.log('Generated session ID:', CHAT_STATE.sessionId);
}

/**
 * Bind chat event listeners
 */
function bindChatEventListeners() {
    // Listen for send message events
    document.addEventListener('sendMessage', handleSendMessage);
    
    // Listen for keyboard shortcuts
    document.addEventListener('keydown', handleGlobalKeydown);
    
    // Listen for page visibility changes
    document.addEventListener('visibilitychange', handleVisibilityChange);
}

/**
 * Handle send message events
 */
async function handleSendMessage(event) {
    const { message } = event.detail;
    
    if (!message || message.trim().length === 0) {
        return;
    }
    
    try {
        // Add user message to chat interface
        addUserMessage(message);
        
        // Save message to history
        saveMessageToHistory(message, CHAT_CONFIG.messageTypes.USER);
        
        // Show loading state
        showChatLoading();
        
        // Send message to LLM API
        const response = await sendMessageToLLM(message);
        
        // Hide loading state
        hideChatLoading();
        
        // Add AI response to chat interface
        addBotMessage(response.reply);
        
        // Save AI response to history
        saveMessageToHistory(response.reply, CHAT_CONFIG.messageTypes.BOT);
        
        // Reset retry count
        CHAT_STATE.retryCount = 0;
        
        // Process possible property recommendations
        processPropertyRecommendations(response.reply);
        
    } catch (error) {
        console.error('Failed to handle send message:', error);
        
        // Hide loading state
        hideChatLoading();
        
        // Show error message
        showErrorMessage(error.message);
        
        // Increment retry count
        CHAT_STATE.retryCount++;
        
        // If retry count hasn't exceeded limit, provide retry options
        if (CHAT_STATE.retryCount < CHAT_STATE.maxRetries) {
            showRetryOption(message);
        }
    }
}

/**
 * Send message to LLM API
 */
async function sendMessageToLLM(message) {
    try {
        // Check if API is available
        const isAvailable = await window.API.isServiceAvailable();
        if (!isAvailable) {
            throw new Error('Backend service unavailable, please check service status');
        }
        
        // Send message
        const response = await window.API.sendChatMessage(message);
        
        // Validate response format
        if (!response || !response.reply) {
            throw new Error('Invalid API response format');
        }
        
        return response;
        
    } catch (error) {
        console.error('Failed to send message to LLM:', error);
        
        // Provide specific error information based on error type
        if (error.message.includes('Network connection failed')) {
            throw new Error(CHAT_CONFIG.errorMessages.network);
        } else if (error.message.includes('Request timeout')) {
            throw new Error(CHAT_CONFIG.errorMessages.timeout);
        } else if (error.message.includes('HTTP error')) {
            throw new Error(CHAT_CONFIG.errorMessages.server);
        } else {
            throw new Error(error.message || CHAT_CONFIG.errorMessages.unknown);
        }
    }
}

/**
 * Add user message to chat interface
 */
function addUserMessage(message) {
    // Use UI module to add message
    window.UI.addMessageToChat(message, true);
    
    // Update message count
    CHAT_STATE.messageCount++;
    
    console.log('Added user message:', message);
}

/**
 * Add AI response to chat interface
 */
function addBotMessage(message) {
    // Use UI module to add message
    window.UI.addMessageToChat(message, false);
    
    // Update message count
    CHAT_STATE.messageCount++;
    
    console.log('Added AI response:', message);
}

/**
 * Show chat loading state
 */
function showChatLoading() {
    CHAT_STATE.isWaitingForResponse = true;
    window.UI.showLoading();
    
    // Update send button state during loading
    updateSendButtonDuringLoading(true);
}

/**
 * Hide chat loading state
 */
function hideChatLoading() {
    CHAT_STATE.isWaitingForResponse = false;
    window.UI.hideLoading();
    
    // Restore send button state
    updateSendButtonDuringLoading(false);
}

/**
 * Update send button state during loading
 */
function updateSendButtonDuringLoading(isLoading) {
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.disabled = isLoading;
        if (isLoading) {
            sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        } else {
            sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        }
    }
}

/**
 * Show error message
 */
function showErrorMessage(errorMessage) {
    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message bot-message error-message';
    errorDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-exclamation-triangle"></i>
        </div>
        <div class="message-content">
            <div class="message-text error-text">
                <i class="fas fa-exclamation-circle"></i>
                ${errorMessage}
            </div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    // Add to chat area
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.appendChild(errorDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Show notification
    window.UI.showNotification(errorMessage, 'error');
}

/**
 * Show retry options
 */
function showRetryOption(originalMessage) {
    const retryDiv = document.createElement('div');
    retryDiv.className = 'message bot-message retry-message';
    retryDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-redo"></i>
        </div>
        <div class="message-content">
            <div class="message-text">
                Message sending failed. You can:
                <div class="retry-options">
                    <button class="retry-btn" onclick="retryMessage('${originalMessage}')">
                        <i class="fas fa-redo"></i> Retry
                    </button>
                    <button class="retry-btn" onclick="editMessage()">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                </div>
            </div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    // Add to chat area
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.appendChild(retryDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

/**
 * Retry sending message
 */
function retryMessage(message) {
    // Remove retry options
    const retryMessages = document.querySelectorAll('.retry-message');
    retryMessages.forEach(msg => msg.remove());
    
    // Resend message
    const event = new CustomEvent('sendMessage', { detail: { message } });
    document.dispatchEvent(event);
}

/**
 * Edit message
 */
function editMessage() {
    // Remove retry options
    const retryMessages = document.querySelectorAll('.retry-message');
    retryMessages.forEach(msg => msg.remove());
    
    // Focus on input field
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.focus();
    }
    
    // Show notification
    window.UI.showNotification('Please edit your message in the input field', 'info');
}

/**
 * Save message to history
 */
function saveMessageToHistory(message, type) {
    const messageObj = {
        id: Date.now(),
        content: message,
        type: type,
        timestamp: new Date().toISOString(),
        sessionId: CHAT_STATE.sessionId
    };
    
    // Add to history
    CHAT_STATE.messageHistory.push(messageObj);
    
    // Limit history length
    if (CHAT_STATE.messageHistory.length > CHAT_CONFIG.maxHistoryLength) {
        CHAT_STATE.messageHistory.shift();
    }
    
    // Save to local storage
    saveChatHistoryToStorage();
    
    console.log('Saved message to history:', messageObj);
}

/**
 * Load chat history
 */
function loadChatHistory() {
    try {
        const savedHistory = localStorage.getItem('chatHistory');
        if (savedHistory) {
            const history = JSON.parse(savedHistory);
            // Only load history for current session
            CHAT_STATE.messageHistory = history.filter(msg => 
                msg.sessionId === CHAT_STATE.sessionId
            );
            console.log('Loaded chat history:', CHAT_STATE.messageHistory.length, 'messages');
        }
    } catch (error) {
        console.error('Failed to load chat history:', error);
    }
}

/**
 * Save chat history to local storage
 */
function saveChatHistoryToStorage() {
    try {
        localStorage.setItem('chatHistory', JSON.stringify(CHAT_STATE.messageHistory));
    } catch (error) {
        console.error('Failed to save chat history:', error);
    }
}

/**
 * Add welcome message
 */
function addWelcomeMessage() {
    // If this is a new session, add welcome message
    if (CHAT_STATE.messageHistory.length === 0) {
        const welcomeMessage = `Welcome to Vacation Rentals AI Assistant! 👋

I can help you:
🏠 Find ideal vacation properties
🗺️ Recommend popular travel destinations
📅 Plan perfect travel itineraries
💰 Provide budget recommendations

Please tell me your needs and I'll provide professional advice!`;
        
        // Save welcome message to history
        saveMessageToHistory(welcomeMessage, CHAT_CONFIG.messageTypes.SYSTEM);
    }
}

/**
 * Process property recommendations from AI response
 */
function processPropertyRecommendations(response) {
    // This function can be expanded to parse AI responses for property recommendations
    // and display them in the properties section
    console.log('Processing property recommendations:', response);
}

/**
 * Handle profile save event
 */
function handleSaveProfile(event) {
    const profileData = event.detail;
    console.log('Saving profile for Team18:', profileData);
    
    // Ensure the name is always Team18
    profileData.name = 'Team18';
    
    // Save profile to backend
    saveUserProfile(profileData);
}

/**
 * Save user profile to backend
 */
async function saveUserProfile(profileData) {
    try {
        // Show loading indicator
        window.UI.showLoading();
        
        // Create user profile via API
        const response = await fetch('/create_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: profileData.name,
                weighed_location: profileData.locationWeight,
                weighed_type: profileData.typeWeight,
                weighed_features: profileData.featuresWeight,
                weighed_price: profileData.priceWeight
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Profile saved successfully:', result);
            
            // Show success message
            window.UI.showNotification('Profile saved successfully! User ID: ' + result.user_id, 'success');
        } else {
            throw new Error('Failed to save profile');
        }
        
    } catch (error) {
        console.error('Error saving profile:', error);
        window.UI.showNotification('Failed to save profile. Please try again.', 'error');
    } finally {
        // Hide loading indicator
        window.UI.hideLoading();
    }
}

/**
 * Handle global keyboard events
 */
function handleGlobalKeydown(event) {
    // Ctrl/Cmd + Enter to quickly send message
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        const chatInput = document.getElementById('chatInput');
        if (chatInput && chatInput.value.trim()) {
            event.preventDefault();
            handleSendClick();
        }
    }
    
    // Esc key to clear input field
    if (event.key === 'Escape') {
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.value = '';
            chatInput.style.height = 'auto';
            updateSendButtonState();
        }
    }
}

/**
 * Handle page visibility changes
 */
function handleVisibilityChange() {
    if (document.hidden) {
        // Handle when page is hidden
        console.log('Page hidden');
    } else {
        // Handle when page is visible
        console.log('Page visible');
        // Can add logic here to restore chat state
    }
}

/**
 * Get current time string
 */
function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

/**
 * Clear chat history
 */
function clearChatHistory() {
    CHAT_STATE.messageHistory = [];
    localStorage.removeItem('chatHistory');
    
    // Clear chat interface
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.innerHTML = '';
    }
    
    // Re-add welcome message
    addWelcomeMessage();
    
    console.log('Chat history cleared');
}

/**
 * Export chat history
 */
function exportChatHistory() {
    try {
        const historyData = {
            sessionId: CHAT_STATE.sessionId,
            exportTime: new Date().toISOString(),
            messages: CHAT_STATE.messageHistory
        };
        
        const dataStr = JSON.stringify(historyData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `chat_history_${CHAT_STATE.sessionId}.json`;
        link.click();
        
        console.log('Chat history exported');
        
    } catch (error) {
        console.error('Failed to export chat history:', error);
        window.UI.showNotification('Export failed, please try again', 'error');
    }
}

/**
 * Get chat statistics
 */
function getChatStats() {
    return {
        totalMessages: CHAT_STATE.messageCount,
        userMessages: CHAT_STATE.messageHistory.filter(msg => 
            msg.type === CHAT_CONFIG.messageTypes.USER
        ).length,
        botMessages: CHAT_STATE.messageHistory.filter(msg => 
            msg.type === CHAT_CONFIG.messageTypes.BOT
        ).length,
        sessionId: CHAT_STATE.sessionId,
        isWaiting: CHAT_STATE.isWaitingForResponse
    };
}

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', initChat);

// Export chat functions
window.Chat = {
    clearChatHistory,
    exportChatHistory,
    getChatStats,
    retryMessage,
    editMessage
};

/**
 * Bind floating chat event listeners
 */
function bindFloatingChatEventListeners() {
    console.log('💬 Binding floating chat event listeners...');
    
    // Floating chat input
    const floatingChatInput = document.getElementById('floatingChatInput');
    const floatingSendButton = document.getElementById('floatingSendButton');
    
    if (floatingChatInput) {
        // Auto resize textarea
        floatingChatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
            
            // Enable/disable send button
            if (floatingSendButton) {
                floatingSendButton.disabled = !this.value.trim();
            }
        });
        
        // Enter key to send (Shift+Enter for new line)
        floatingChatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleFloatingChatSend();
            }
        });
    }
    
    // Floating send button
    if (floatingSendButton) {
        floatingSendButton.addEventListener('click', handleFloatingChatSend);
    }
    
    // Floating quick action buttons
    const floatingQuickActionBtns = document.querySelectorAll('.floating-chat-input-container .quick-action-btn');
    floatingQuickActionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const prompt = this.getAttribute('data-prompt');
            if (prompt && floatingChatInput) {
                floatingChatInput.value = prompt;
                floatingChatInput.focus();
                if (floatingSendButton) {
                    floatingSendButton.disabled = false;
                }
            }
        });
    });
}

/**
 * Handle floating chat send
 */
function handleFloatingChatSend() {
    const floatingChatInput = document.getElementById('floatingChatInput');
    if (!floatingChatInput || !floatingChatInput.value.trim()) {
        return;
    }
    
    const message = floatingChatInput.value.trim();
    console.log('💬 Sending floating chat message:', message);
    
    // Clear input
    floatingChatInput.value = '';
    floatingChatInput.style.height = 'auto';
    
    // Disable send button
    const floatingSendButton = document.getElementById('floatingSendButton');
    if (floatingSendButton) {
        floatingSendButton.disabled = true;
    }
    
    // Add user message to floating chat
    addFloatingMessage(message, 'user');
    
    // Send to API
    sendChatMessageToAPI(message, true); // true indicates floating chat
}

/**
 * Add message to floating chat
 */
function addFloatingMessage(message, type, timestamp = null) {
    const floatingChatMessages = document.getElementById('floatingChatMessages');
    if (!floatingChatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.innerHTML = type === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = message;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = timestamp || new Date().toLocaleTimeString();
    
    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timeDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    floatingChatMessages.appendChild(messageDiv);
    floatingChatMessages.scrollTop = floatingChatMessages.scrollHeight;
}

/**
 * Send chat message to API (updated to support floating chat)
 */
async function sendChatMessageToAPI(message, isFloatingChat = false) {
    try {
        console.log('💬 Sending message to API:', message);
        
        // Show typing indicator
        if (isFloatingChat) {
            showFloatingTypingIndicator();
        } else {
            showFloatingTypingIndicator(); // Using floating typing indicator for now
        }
        
        // Call API
        const response = await window.API.sendChatMessage(message);
        
        // Hide typing indicator
        if (isFloatingChat) {
            hideFloatingTypingIndicator();
        } else {
            hideTypingIndicator();
        }
        
        // Add bot response
        if (response && response.response) {
            if (isFloatingChat) {
                addFloatingMessage(response.response, 'bot');
            } else {
                addFloatingMessage(response.response, 'bot'); // Using floating message for now
            }
            
            // Update message history
            CHAT_STATE.messageHistory.push(
                { type: 'user', content: message, timestamp: new Date() },
                { type: 'bot', content: response.response, timestamp: new Date() }
            );
            
            // Trim history if too long
            if (CHAT_STATE.messageHistory.length > CHAT_CONFIG.maxHistoryLength) {
                CHAT_STATE.messageHistory = CHAT_STATE.messageHistory.slice(-CHAT_CONFIG.maxHistoryLength);
            }
        }
        
    } catch (error) {
        console.error('💬 Error sending message:', error);
        
        // Hide typing indicator
        if (isFloatingChat) {
            hideFloatingTypingIndicator();
        } else {
            hideTypingIndicator();
        }
        
        // Show error message
        const errorMessage = 'Sorry, I encountered an error. Please try again.';
        if (isFloatingChat) {
            addFloatingMessage(errorMessage, 'bot');
        } else {
            addFloatingMessage(errorMessage, 'bot'); // Using floating message for now
        }
    }
}

/**
 * Show typing indicator in floating chat
 */
function showFloatingTypingIndicator() {
    const floatingChatMessages = document.getElementById('floatingChatMessages');
    if (!floatingChatMessages) return;
    
    const typingDiv = document.createElement('div');
    typingDiv.id = 'floatingTypingIndicator';
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-text">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    
    floatingChatMessages.appendChild(typingDiv);
    floatingChatMessages.scrollTop = floatingChatMessages.scrollHeight;
}

/**
 * Hide typing indicator in floating chat
 */
function hideFloatingTypingIndicator() {
    const typingIndicator = document.getElementById('floatingTypingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Initialize floating chat when page loads
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(bindFloatingChatEventListeners, 100); // Small delay to ensure DOM is ready
});

console.log('Chat module loaded:', window.Chat);
