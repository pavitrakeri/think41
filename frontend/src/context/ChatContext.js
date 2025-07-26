import React, { createContext, useContext, useReducer, useEffect } from 'react';

// Initial state
const initialState = {
  messages: [],
  isLoading: false,
  userInput: '',
  conversations: [],
  currentConversationId: null,
  selectedConversationId: null
};

// Action types
const ACTIONS = {
  SET_MESSAGES: 'SET_MESSAGES',
  ADD_MESSAGE: 'ADD_MESSAGE',
  SET_LOADING: 'SET_LOADING',
  SET_USER_INPUT: 'SET_USER_INPUT',
  SET_CONVERSATIONS: 'SET_CONVERSATIONS',
  ADD_CONVERSATION: 'ADD_CONVERSATION',
  SET_CURRENT_CONVERSATION: 'SET_CURRENT_CONVERSATION',
  SET_SELECTED_CONVERSATION: 'SET_SELECTED_CONVERSATION',
  LOAD_CONVERSATION: 'LOAD_CONVERSATION',
  CLEAR_MESSAGES: 'CLEAR_MESSAGES'
};

// Reducer function
const chatReducer = (state, action) => {
  switch (action.type) {
    case ACTIONS.SET_MESSAGES:
      return { ...state, messages: action.payload };
    
    case ACTIONS.ADD_MESSAGE:
      return { ...state, messages: [...state.messages, action.payload] };
    
    case ACTIONS.SET_LOADING:
      return { ...state, isLoading: action.payload };
    
    case ACTIONS.SET_USER_INPUT:
      return { ...state, userInput: action.payload };
    
    case ACTIONS.SET_CONVERSATIONS:
      return { ...state, conversations: action.payload };
    
    case ACTIONS.ADD_CONVERSATION:
      return { 
        ...state, 
        conversations: [...state.conversations, action.payload]
      };
    
    case ACTIONS.SET_CURRENT_CONVERSATION:
      return { ...state, currentConversationId: action.payload };
    
    case ACTIONS.SET_SELECTED_CONVERSATION:
      return { ...state, selectedConversationId: action.payload };
    
    case ACTIONS.LOAD_CONVERSATION:
      const conversation = state.conversations.find(c => c.id === action.payload);
      return {
        ...state,
        messages: conversation ? conversation.messages : [],
        selectedConversationId: action.payload,
        currentConversationId: action.payload
      };
    
    case ACTIONS.CLEAR_MESSAGES:
      return { ...state, messages: [] };
    
    default:
      return state;
  }
};

// Create context
const ChatContext = createContext();

// Provider component
export const ChatProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Load conversations from localStorage on mount
  useEffect(() => {
    const savedConversations = localStorage.getItem('chatConversations');
    if (savedConversations) {
      try {
        const conversations = JSON.parse(savedConversations);
        dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: conversations });
      } catch (error) {
        console.error('Error loading conversations from localStorage:', error);
      }
    }
  }, []);

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('chatConversations', JSON.stringify(state.conversations));
  }, [state.conversations]);

  // Actions
  const actions = {
    setMessages: (messages) => dispatch({ type: ACTIONS.SET_MESSAGES, payload: messages }),
    addMessage: (message) => dispatch({ type: ACTIONS.ADD_MESSAGE, payload: message }),
    setLoading: (loading) => dispatch({ type: ACTIONS.SET_LOADING, payload: loading }),
    setUserInput: (input) => dispatch({ type: ACTIONS.SET_USER_INPUT, payload: input }),
    setConversations: (conversations) => dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: conversations }),
    addConversation: (conversation) => dispatch({ type: ACTIONS.ADD_CONVERSATION, payload: conversation }),
    setCurrentConversation: (id) => dispatch({ type: ACTIONS.SET_CURRENT_CONVERSATION, payload: id }),
    setSelectedConversation: (id) => dispatch({ type: ACTIONS.SET_SELECTED_CONVERSATION, payload: id }),
    loadConversation: (id) => dispatch({ type: ACTIONS.LOAD_CONVERSATION, payload: id }),
    clearMessages: () => dispatch({ type: ACTIONS.CLEAR_MESSAGES })
  };

  return (
    <ChatContext.Provider value={{ state, actions }}>
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use the chat context
export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}; 