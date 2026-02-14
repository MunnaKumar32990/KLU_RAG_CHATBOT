import axios from 'axios';

const API_BASE_URL = '/api';

// Configure axios with longer timeout for slow model responses
const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 120000, // 2 minutes timeout for llama3.2:1b model
    headers: {
        'Content-Type': 'application/json'
    }
});

// API service for interacting with FastAPI backend
const api = {
    // POST /chat - Send a question and get response
    async sendMessage(question, conversationId = null) {
        try {
            const response = await axiosInstance.post('/chat', {
                question,
                conversation_id: conversationId
            });
            return { success: true, data: response.data };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.detail || error.message || 'Failed to send message'
            };
        }
    },

    // GET /health - Check system health
    async getHealth() {
        try {
            const response = await axiosInstance.get('/health');
            return { success: true, data: response.data };
        } catch (error) {
            return {
                success: false,
                error: error.message || 'Failed to fetch health status'
            };
        }
    },

    // GET /stats - Get document statistics
    async getStats() {
        try {
            const response = await axiosInstance.get('/stats');
            return { success: true, data: response.data };
        } catch (error) {
            return {
                success: false,
                error: error.message || 'Failed to fetch stats'
            };
        }
    },

    // GET / - Get API info
    async getApiInfo() {
        try {
            const response = await axiosInstance.get('/');
            return { success: true, data: response.data };
        } catch (error) {
            return {
                success: false,
                error: error.message || 'Failed to fetch API info'
            };
        }
    }
};

export default api;
