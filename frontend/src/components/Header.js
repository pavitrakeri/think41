import React from 'react';
import { MessageCircle, ShoppingBag } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <MessageCircle className="h-8 w-8 text-primary-600" />
              <ShoppingBag className="h-6 w-6 text-primary-500" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">E-commerce Chatbot</h1>
              <p className="text-sm text-gray-600">Customer Support Assistant</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600">
              <span className="w-2 h-2 bg-green-500 rounded-full"></span>
              <span>Online</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <span className="text-primary-600 font-medium text-sm">AI</span>
              </div>
              <span className="text-sm font-medium text-gray-700">AI Assistant</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 