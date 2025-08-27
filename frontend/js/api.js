/**
 * API Module
 * Responsible for communicating with the FastAPI backend service
 */

// API Configuration
const API_CONFIG = {
    // Base URL for backend service
    BASE_URL: 'http://127.0.0.1:8000',
    
    // API endpoints
    ENDPOINTS: {
        CHAT: '/chat',
        HEALTH: '/health',
        ROOT: '/'
    },
    
    // Request timeout (milliseconds)
    TIMEOUT: 30000,
    
    // Maximum retry attempts
    MAX_RETRIES: 3
};

/**
 * Generic HTTP request function
 * @param {string} url - Request URL
 * @param {Object} options - Request options
 * @returns {Promise} - Returns Promise object
 */
async function makeRequest(url, options = {}) {
    const {
        method = 'GET',
        headers = {},
        body = null,
        timeout = API_CONFIG.TIMEOUT,
        retries = 0
    } = options;

    try {
        // Create AbortController for timeout control
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        // Prepare request configuration
        const requestOptions = {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...headers
            },
            signal: controller.signal
        };

        // Add request body if present
        if (body && method !== 'GET') {
            requestOptions.body = JSON.stringify(body);
        }

        // Send request
        const response = await fetch(url, requestOptions);
        
        // Clear timeout timer
        clearTimeout(timeoutId);

        // Check response status
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse response data
        const data = await response.json();
        return { success: true, data, status: response.status };

    } catch (error) {
        // Handle timeout errors
        if (error.name === 'AbortError') {
            throw new Error('Request timeout, please check your network connection');
        }

        // Handle network errors
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Network connection failed, please check if backend service is running');
        }

        // Handle other errors
        throw new Error(`Request failed: ${error.message}`);
    }
}

/**
 * Request function with retry mechanism
 * @param {string} url - Request URL
 * @param {Object} options - Request options
 * @returns {Promise} - Returns Promise object
 */
async function makeRequestWithRetry(url, options = {}) {
    let lastError;
    
    for (let attempt = 0; attempt <= API_CONFIG.MAX_RETRIES; attempt++) {
        try {
            return await makeRequest(url, options);
        } catch (error) {
            lastError = error;
            
            // If not the last attempt, wait before retrying
            if (attempt < API_CONFIG.MAX_RETRIES) {
                const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
                await new Promise(resolve => setTimeout(resolve, delay));
                console.log(`Request failed, retrying in ${delay}ms (${attempt + 1}/${API_CONFIG.MAX_RETRIES})`);
            }
        }
    }
    
    throw lastError;
}

/**
 * Send chat message to backend
 * @param {string} message - User message
 * @returns {Promise} - Returns Promise with AI response
 */
async function sendChatMessage(message) {
    try {
        console.log('Sending chat message:', message);
        
        const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CHAT}`;
        const response = await makeRequestWithRetry(url, {
            method: 'POST',
            body: { message },
            timeout: 60000 // Chat requests can wait longer
        });
        
        console.log('Received AI response:', response.data);
        return response.data;
        
    } catch (error) {
        console.error('Failed to send chat message:', error);
        throw error;
    }
}

/**
 * Check backend service health status
 * @returns {Promise} - Returns Promise with health status
 */
async function checkHealth() {
    try {
        const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HEALTH}`;
        const response = await makeRequest(url, { timeout: 5000 });
        
        console.log('Health check result:', response.data);
        return response.data;
        
    } catch (error) {
        console.error('Health check failed:', error);
        throw error;
    }
}

/**
 * Check if backend service is available
 * @returns {Promise<boolean>} - Returns boolean indicating service availability
 */
async function isServiceAvailable() {
    try {
        await checkHealth();
        return true;
    } catch (error) {
        return false;
    }
}

/**
 * Get API status information
 * @returns {Object} - Returns API status object
 */
function getApiStatus() {
    return {
        baseUrl: API_CONFIG.BASE_URL,
        endpoints: API_CONFIG.ENDPOINTS,
        timeout: API_CONFIG.TIMEOUT,
        maxRetries: API_CONFIG.MAX_RETRIES
    };
}

/**
 * Update API configuration
 * @param {Object} newConfig - New configuration object
 */
function updateApiConfig(newConfig) {
    Object.assign(API_CONFIG, newConfig);
    console.log('API configuration updated:', API_CONFIG);
}

// Export all functions
window.API = {
    sendChatMessage,
    checkHealth,
    isServiceAvailable,
    getApiStatus,
    updateApiConfig,
    makeRequest,
    makeRequestWithRetry
};

// Log API module information to console
console.log('API module loaded:', window.API);
console.log('API configuration:', API_CONFIG);
