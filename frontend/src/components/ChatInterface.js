import React, { useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Bot, User, Loader, Menu, X } from 'lucide-react';
import ChatMessage from './ChatMessage';
import QuickActions from './QuickActions';
import ConversationHistory from './ConversationHistory';
import { useChat } from '../context/ChatContext';

const ChatInterface = () => {
  const { state, actions } = useChat();
  const messagesEndRef = useRef(null);
  const [showSidebar, setShowSidebar] = React.useState(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [state.messages]);

  // Add welcome message on component mount if no messages exist
  useEffect(() => {
    if (state.messages.length === 0 && !state.selectedConversationId) {
      const welcomeMessage = {
        id: Date.now(),
        type: 'bot',
        content: "Hello! I'm your AI customer support assistant. I can help you with:\n\n• Product information and availability\n• Order status and tracking\n• Stock levels\n• General customer service questions\n\nHow can I assist you today?",
        timestamp: new Date()
      };
      actions.setMessages([welcomeMessage]);
    }
  }, [state.messages.length, state.selectedConversationId, actions]);

  const sendMessage = async (message) => {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    actions.addMessage(userMessage);
    actions.setUserInput('');
    actions.setLoading(true);

    try {
      const response = await axios.post('/api/chat', {
        message: message,
        conversation_id: state.currentConversationId
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.response,
        timestamp: new Date()
      };

      actions.addMessage(botMessage);
      actions.setCurrentConversation(response.data.conversation_id);

      // Save conversation if it's new
      if (!state.currentConversationId) {
        const conversation = {
          id: response.data.conversation_id,
          title: message.length > 30 ? message.substring(0, 30) + '...' : message,
          messages: [...state.messages, userMessage, botMessage],
          timestamp: new Date()
        };
        actions.addConversation(conversation);
      } else {
        // Update existing conversation
        const updatedConversations = state.conversations.map(conv => {
          if (conv.id === state.currentConversationId) {
            return {
              ...conv,
              messages: [...conv.messages, userMessage, botMessage]
            };
          }
          return conv;
        });
        actions.setConversations(updatedConversations);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: "I'm sorry, I'm having trouble connecting to the server right now. Please try again in a moment.",
        timestamp: new Date()
      };
      actions.addMessage(errorMessage);
    } finally {
      actions.setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(state.userInput);
  };

  const handleQuickAction = (action) => {
    sendMessage(action);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="card">
        <div className="flex h-[600px]">
          {/* Sidebar Toggle for Mobile */}
          <div className="lg:hidden absolute top-4 left-4 z-10">
            <button
              onClick={() => setShowSidebar(!showSidebar)}
              className="p-2 bg-white rounded-lg shadow-md hover:bg-gray-50"
            >
              {showSidebar ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>

          {/* Conversation History Sidebar */}
          <div className={`
            ${showSidebar ? 'block' : 'hidden'} 
            lg:block lg:relative lg:translate-x-0
            absolute left-0 top-0 h-full z-20
            transform transition-transform duration-300 ease-in-out
          `}>
            <ConversationHistory />
          </div>

          {/* Main Chat Area */}
          <div className="flex-1 flex flex-col">
            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {state.messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              
              {state.isLoading && (
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <Bot className="h-4 w-4 text-primary-600" />
                  </div>
                  <div className="flex-1">
                    <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
                      <div className="loading-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Quick Actions */}
            <div className="border-t border-gray-200 p-4">
              <QuickActions onAction={handleQuickAction} />
            </div>

            {/* Input Form */}
            <div className="border-t border-gray-200 p-4">
              <form onSubmit={handleSubmit} className="flex space-x-3">
                <div className="flex-1">
                  <textarea
                    value={state.userInput}
                    onChange={(e) => actions.setUserInput(e.target.value)}
                    placeholder="Type your message here..."
                    className="chat-input"
                    rows="2"
                    disabled={state.isLoading}
                  />
                </div>
                <button
                  type="submit"
                  disabled={state.isLoading || !state.userInput.trim()}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                >
                  {state.isLoading ? (
                    <Loader className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                  <span>Send</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 