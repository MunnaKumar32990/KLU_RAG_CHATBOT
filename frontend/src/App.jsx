import { useState, useEffect, useRef } from 'react';
import api from './services/api';
import './App.css';

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [health, setHealth] = useState(null);
    const [stats, setStats] = useState(null);
    const [showSidebar, setShowSidebar] = useState(false);
    const messagesEndRef = useRef(null);

    // Scroll to bottom when new messages arrive
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Fetch health and stats on component mount
    useEffect(() => {
        fetchHealth();
        fetchStats();
    }, []);

    const fetchHealth = async () => {
        const result = await api.getHealth();
        if (result.success) {
            setHealth(result.data);
        }
    };

    const fetchStats = async () => {
        const result = await api.getStats();
        if (result.success) {
            setStats(result.data);
        }
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = {
            role: 'user',
            content: input,
            timestamp: new Date().toLocaleTimeString()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        const result = await api.sendMessage(input);

        if (result.success) {
            const botMessage = {
                role: 'assistant',
                content: result.data.answer,
                sources: result.data.sources || [],
                timestamp: new Date().toLocaleTimeString()
            };
            setMessages(prev => [...prev, botMessage]);
        } else {
            const errorMessage = {
                role: 'error',
                content: result.error,
                timestamp: new Date().toLocaleTimeString()
            };
            setMessages(prev => [...prev, errorMessage]);
        }

        setLoading(false);
    };

    const suggestedQuestions = [
        "What are the B.Tech admission requirements?",
        "What is the highest placement package?",
        "Tell me about the hostel fees",
        "Who is the HOD of Computer Science?",
        "What are the placement statistics for 2024?"
    ];

    return (
        <div className="app">
            {/* Header */}
            <header className="header">
                <div className="header-content">
                    <div className="header-left">
                        <div className="logo">🎓</div>
                        <div className="header-text">
                            <h1>College AI Assistant</h1>
                            <p>Ask me anything about the college</p>
                        </div>
                    </div>
                    <button
                        className="sidebar-toggle"
                        onClick={() => setShowSidebar(!showSidebar)}
                    >
                        {showSidebar ? '✕' : '☰'}
                    </button>
                </div>
            </header>

            <div className="main-container">
                {/* Sidebar */}
                <aside className={`sidebar ${showSidebar ? 'show' : ''}`}>
                    <div className="sidebar-section">
                        <h3>📊 System Status</h3>
                        {health && (
                            <div className="status-card">
                                <div className={`status-indicator ${health.status === 'healthy' ? 'healthy' : 'degraded'}`}>
                                    {health.status === 'healthy' ? '✓' : '⚠'}
                                </div>
                                <div className="status-details">
                                    <p><strong>Status:</strong> {health.status}</p>
                                    <p><strong>Vector DB:</strong> {health.vector_db_initialized ? '✓ Ready' : '✗ Not Ready'}</p>
                                    <p><strong>Ollama:</strong> {health.ollama_available ? '✓ Available' : '✗ Unavailable'}</p>
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="sidebar-section">
                        <h3>📚 Document Stats</h3>
                        {stats && (
                            <div className="stats-card">
                                <p><strong>Total Chunks:</strong> {stats.total_chunks}</p>
                                <p><strong>Status:</strong> {stats.status}</p>
                            </div>
                        )}
                    </div>

                    <div className="sidebar-section">
                        <h3>💡 Suggested Questions</h3>
                        <div className="suggested-questions">
                            {suggestedQuestions.map((question, index) => (
                                <button
                                    key={index}
                                    className="suggested-question"
                                    onClick={() => setInput(question)}
                                >
                                    {question}
                                </button>
                            ))}
                        </div>
                    </div>
                </aside>

                {/* Chat Container */}
                <main className="chat-container">
                    <div className="messages">
                        {messages.length === 0 && (
                            <div className="welcome-message">
                                <div className="welcome-icon">🤖</div>
                                <h2>Welcome to College AI Assistant!</h2>
                                <p>I can help you with information about admissions, fees, placements, academics, faculty, and more.</p>
                                <p>Try asking a question or select from the suggested questions.</p>
                            </div>
                        )}

                        {messages.map((message, index) => (
                            <div key={index} className={`message ${message.role}`}>
                                <div className="message-avatar">
                                    {message.role === 'user' ? '👤' : message.role === 'error' ? '⚠️' : '🤖'}
                                </div>
                                <div className="message-content">
                                    <div className="message-text">{message.content}</div>
                                    {message.sources && message.sources.length > 0 && (
                                        <div className="sources">
                                            <p className="sources-title">📄 Sources:</p>
                                            {message.sources.map((source, idx) => (
                                                <div key={idx} className="source-card">
                                                    <div className="source-header">
                                                        <span className="source-file">{source.source}</span>
                                                        <span className="source-score">
                                                            {(source.relevance_score * 100).toFixed(0)}% match
                                                        </span>
                                                    </div>
                                                    <p className="source-content">{source.content}</p>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                    <span className="message-time">{message.timestamp}</span>
                                </div>
                            </div>
                        ))}

                        {loading && (
                            <div className="message assistant">
                                <div className="message-avatar">🤖</div>
                                <div className="message-content">
                                    <div className="typing-indicator">
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                    </div>
                                </div>
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Form */}
                    <form className="input-form" onSubmit={handleSendMessage}>
                        <input
                            type="text"
                            className="message-input"
                            placeholder="Ask a question about the college..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            disabled={loading}
                        />
                        <button
                            type="submit"
                            className="send-button"
                            disabled={loading || !input.trim()}
                        >
                            {loading ? '⏳' : '➤'}
                        </button>
                    </form>
                </main>
            </div>
        </div>
    );
}

export default App;
