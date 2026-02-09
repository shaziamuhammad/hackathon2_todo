/**
 * ChatWidget Component
 * AI-powered chat interface for natural language todo management
 */
'use client';

import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

interface ChatWidgetProps {
  userId?: string;
}

export default function ChatWidget({ userId }: ChatWidgetProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api/v1';

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    try {
      // Get auth token from localStorage
      const token = localStorage.getItem('token');

      if (!token) {
        throw new Error('Not authenticated. Please log in.');
      }

      // Send message to /chat endpoint
      const response = await axios.post(
        `${API_BASE_URL}/chat`,
        {
          message: inputMessage,
          conversation_id: conversationId
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      // Extract response data
      const { response: aiResponse, conversation_id: newConversationId } = response.data;

      // Update conversation ID if new
      if (newConversationId && !conversationId) {
        setConversationId(newConversationId);
      }

      // Add AI response to chat
      const assistantMessage: Message = {
        role: 'assistant',
        content: aiResponse,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (err: any) {
      console.error('Error sending message:', err);

      let errorMessage = 'Failed to send message. Please try again.';

      if (err.response?.status === 401) {
        errorMessage = 'Session expired. Please log in again.';
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }

      setError(errorMessage);

      // Add error message to chat
      const errorMsg: Message = {
        role: 'assistant',
        content: `❌ ${errorMessage}`,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMsg]);

    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setConversationId(null);
    setError(null);
  };

  return (
    <div className="chat-widget flex flex-col h-full bg-white rounded-lg shadow-lg">
      {/* Chat Header */}
      <div className="chat-header bg-purple-600 text-white p-3 md:p-4 rounded-t-lg flex justify-between items-center">
        <div>
          <h3 className="text-base md:text-lg font-semibold">AI Todo Assistant</h3>
          <p className="text-xs md:text-sm text-purple-200">Ask me to manage your tasks</p>
        </div>
        <button
          onClick={clearChat}
          className="text-white hover:text-purple-200 text-xs md:text-sm px-2 py-1 rounded hover:bg-purple-700 transition-colors"
          title="Clear chat"
        >
          Clear
        </button>
      </div>

      {/* Messages Container */}
      <div className="messages-container flex-1 overflow-y-auto p-3 md:p-4 space-y-3 md:space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-4 md:mt-8 px-2">
            <p className="mb-2 text-sm md:text-base">👋 Hi! I'm your AI todo assistant.</p>
            <p className="text-xs md:text-sm">Try saying:</p>
            <ul className="text-xs md:text-sm mt-2 space-y-1">
              <li>"Add buy groceries with high priority"</li>
              <li>"Show me all my tasks"</li>
              <li>"Mark the meeting task as complete"</li>
            </ul>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`message flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`message-bubble max-w-[85%] md:max-w-[80%] p-2.5 md:p-3 rounded-lg text-sm md:text-base ${
                message.role === 'user'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p className="whitespace-pre-wrap break-words">{message.content}</p>
              {message.timestamp && (
                <p className="text-xs mt-1 opacity-70">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </p>
              )}
            </div>
          </div>
        ))}

        {/* Typing Indicator */}
        {isLoading && (
          <div className="message flex justify-start">
            <div className="message-bubble bg-gray-100 p-2.5 md:p-3 rounded-lg">
              <div className="typing-indicator flex space-x-1">
                <div className="dot w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="dot w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div className="dot w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Error Display */}
      {error && (
        <div className="error-banner bg-red-100 border border-red-400 text-red-700 px-3 md:px-4 py-2 text-xs md:text-sm">
          {error}
        </div>
      )}

      {/* Input Area */}
      <div className="input-area p-3 md:p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1 px-3 md:px-4 py-2 md:py-2.5 text-sm md:text-base border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600 disabled:bg-gray-100"
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !inputMessage.trim()}
            className="px-4 md:px-6 py-2 md:py-2.5 text-sm md:text-base bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors touch-manipulation"
          >
            {isLoading ? (
              <span className="hidden sm:inline">Sending...</span>
            ) : (
              <span className="hidden sm:inline">Send</span>
            )}
            {/* Mobile: Show icon only */}
            <span className="sm:hidden">
              {isLoading ? '...' : '➤'}
            </span>
          </button>
        </div>
      </div>

      <style jsx>{`
        .delay-100 {
          animation-delay: 0.1s;
        }
        .delay-200 {
          animation-delay: 0.2s;
        }
      `}</style>
    </div>
  );
}
