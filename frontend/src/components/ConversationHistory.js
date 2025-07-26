import React from 'react';
import { MessageSquare, Clock, Trash2 } from 'lucide-react';
import { useChat } from '../context/ChatContext';

const ConversationHistory = () => {
  const { state, actions } = useChat();

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = (now - date) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } else if (diffInHours < 48) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString();
    }
  };

  const getConversationPreview = (conversation) => {
    const userMessages = conversation.messages.filter(msg => msg.type === 'user');
    if (userMessages.length > 0) {
      const lastUserMessage = userMessages[userMessages.length - 1];
      return lastUserMessage.content.length > 50 
        ? lastUserMessage.content.substring(0, 50) + '...'
        : lastUserMessage.content;
    }
    return 'No messages';
  };

  const handleConversationClick = (conversationId) => {
    actions.loadConversation(conversationId);
  };

  const handleDeleteConversation = (e, conversationId) => {
    e.stopPropagation();
    const updatedConversations = state.conversations.filter(c => c.id !== conversationId);
    actions.setConversations(updatedConversations);
    
    // If we're deleting the currently selected conversation, clear the messages
    if (state.selectedConversationId === conversationId) {
      actions.clearMessages();
      actions.setSelectedConversation(null);
      actions.setCurrentConversation(null);
    }
  };

  const startNewConversation = () => {
    actions.clearMessages();
    actions.setSelectedConversation(null);
    actions.setCurrentConversation(null);
  };

  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Conversations</h3>
        <button
          onClick={startNewConversation}
          className="mt-2 w-full bg-primary-500 text-white px-3 py-2 rounded-lg hover:bg-primary-600 transition-colors text-sm font-medium"
        >
          New Conversation
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {state.conversations.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            <MessageSquare className="h-8 w-8 mx-auto mb-2 text-gray-400" />
            <p className="text-sm">No conversations yet</p>
            <p className="text-xs">Start a new conversation to see it here</p>
          </div>
        ) : (
          <div className="p-2">
            {state.conversations.map((conversation) => (
              <div
                key={conversation.id}
                onClick={() => handleConversationClick(conversation.id)}
                className={`p-3 rounded-lg cursor-pointer transition-colors mb-2 ${
                  state.selectedConversationId === conversation.id
                    ? 'bg-primary-50 border border-primary-200'
                    : 'hover:bg-gray-50'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2 mb-1">
                      <MessageSquare className="h-4 w-4 text-gray-400" />
                      <span className="text-sm font-medium text-gray-900 truncate">
                        {conversation.title || 'Conversation'}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500 mb-2 line-clamp-2">
                      {getConversationPreview(conversation)}
                    </p>
                    <div className="flex items-center space-x-1 text-xs text-gray-400">
                      <Clock className="h-3 w-3" />
                      <span>{formatDate(conversation.timestamp)}</span>
                      <span>•</span>
                      <span>{conversation.messages.length} messages</span>
                    </div>
                  </div>
                  <button
                    onClick={(e) => handleDeleteConversation(e, conversation.id)}
                    className="opacity-0 group-hover:opacity-100 hover:bg-red-100 p-1 rounded transition-all"
                    title="Delete conversation"
                  >
                    <Trash2 className="h-3 w-3 text-gray-400 hover:text-red-500" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationHistory; 