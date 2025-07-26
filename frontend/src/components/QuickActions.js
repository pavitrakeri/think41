import React from 'react';
import { Package, ShoppingCart, TrendingUp, HelpCircle } from 'lucide-react';

const QuickActions = ({ onAction }) => {
  const actions = [
    {
      id: 'top-products',
      text: 'Top Products',
      icon: TrendingUp,
      message: 'What are the top 5 most sold products?'
    },
    {
      id: 'order-status',
      text: 'Order Status',
      icon: ShoppingCart,
      message: 'Show me the status of order ID 12345'
    },
    {
      id: 'stock-check',
      text: 'Stock Check',
      icon: Package,
      message: 'How many Classic T-Shirts are left in stock?'
    },
    {
      id: 'help',
      text: 'Help',
      icon: HelpCircle,
      message: 'What can you help me with?'
    }
  ];

  return (
    <div className="space-y-3">
      <div className="text-sm font-medium text-gray-700">Quick Actions:</div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        {actions.map((action) => {
          const Icon = action.icon;
          return (
            <button
              key={action.id}
              onClick={() => onAction(action.message)}
              className="flex items-center space-x-2 p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200 text-sm"
            >
              <Icon className="h-4 w-4 text-gray-600" />
              <span className="text-gray-700">{action.text}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default QuickActions; 