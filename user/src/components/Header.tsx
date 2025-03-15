import React, { useState } from 'react';
import { Shield, Bell, User, Menu, Search, X, Settings, LogOut, HelpCircle } from 'lucide-react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router for navigation

interface HeaderProps {
  onNavigate: (page: string) => void;
  onSignOut: () => void;
}

interface Notification {
  id: string;
  title: string;
  message: string;
  time: string;
  type: 'alert' | 'info' | 'warning';
}

export const Header: React.FC<HeaderProps> = ({ onNavigate, onSignOut }) => {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [notifications] = useState<Notification[]>([
    {
      id: '1',
      title: 'Critical Security Alert',
      message: 'Multiple failed login attempts detected',
      time: '2 min ago',
      type: 'alert'
    },
    {
      id: '2',
      title: 'System Update',
      message: 'Security patches available for installation',
      time: '10 min ago',
      type: 'info'
    },
    {
      id: '3',
      title: 'Network Warning',
      message: 'Unusual traffic pattern detected',
      time: '15 min ago',
      type: 'warning'
    }
  ]);

  const getNotificationColor = (type: Notification['type']) => {
    switch (type) {
      case 'alert': return 'text-red-500';
      case 'warning': return 'text-yellow-500';
      case 'info': return 'text-blue-500';
      default: return 'text-gray-500';
    }
  };

  const handleMenuClick = (action: string) => {
    setShowUserMenu(false);
    if (action === 'signout') {
      onSignOut();
    } else {
      onNavigate(action);
    }
  };

  return (
    <header className="bg-gray-900 border-b border-gray-700">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
        <div className="flex items-center space-x-8">
        <div className="flex items-center">
          <a href="/" className="flex items-center">
            <img src="/assets/logo.png" alt="Logo" width={60} height={60} />
            <span className="ml-[-0.5rem] text-xl font-bold text-white">Fukuro</span>
          </a>
        </div>

          
          <div className="hidden md:flex relative">
              <input
                type="text"
                placeholder="Search..."
                className="bg-gray-800 text-gray-300 pl-10 pr-4 py-2 rounded-lg border border-gray-700 focus:outline-none focus:border-blue-500 w-64"
              />
              <Search className="w-5 h-5 text-gray-500 absolute left-3 top-2.5" />
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="relative">
              <button
                onClick={() => setShowNotifications(!showNotifications)}
                className="text-gray-300 hover:text-white p-2 rounded-lg hover:bg-gray-800 transition-colors relative"
              >
                <Bell className="w-6 h-6" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>

              {showNotifications && (
                <div className="absolute right-0 mt-2 w-80 bg-gray-800 rounded-lg shadow-lg border border-gray-700 py-2">
                  <div className="flex items-center justify-between px-4 pb-2 border-b border-gray-700">
                    <h3 className="text-white font-medium">Notifications</h3>
                    <button 
                      onClick={() => setShowNotifications(false)}
                      className="text-gray-400 hover:text-white"
                    >
                      <X size={16} />
                    </button>
                  </div>
                  {notifications.map(notification => (
                    <div
                      key={notification.id}
                      className="px-4 py-3 hover:bg-gray-700 cursor-pointer"
                    >
                      <div className="flex items-start">
                        <div className="flex-1">
                          <p className={`font-medium ${getNotificationColor(notification.type)}`}>
                            {notification.title}
                          </p>
                          <p className="text-sm text-gray-400">{notification.message}</p>
                          <p className="text-xs text-gray-500 mt-1">{notification.time}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                  <div className="px-4 pt-2 border-t border-gray-700">
                    <button className="text-blue-400 hover:text-blue-300 text-sm">
                      View all notifications
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-3 text-gray-300 hover:text-white p-2 rounded-lg hover:bg-gray-800 transition-colors"
              >
                <div className="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center">
                  <User className="w-5 h-5" />
                </div>
                <span className="hidden md:inline">Admin User</span>
              </button>

              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-48 bg-gray-800 rounded-lg shadow-lg border border-gray-700 py-2">
                  <button
                    onClick={() => handleMenuClick('settings')}
                    className="w-full px-4 py-2 text-left text-gray-300 hover:bg-gray-700 flex items-center"
                  >
                    <Settings className="w-4 h-4 mr-2" />
                    Settings
                  </button>
                  <button
                    onClick={() => handleMenuClick('help')}
                    className="w-full px-4 py-2 text-left text-gray-300 hover:bg-gray-700 flex items-center"
                  >
                    <HelpCircle className="w-4 h-4 mr-2" />
                    Help & Support
                  </button>
                  <div className="border-t border-gray-700 my-1"></div>
                  <button
                    onClick={() => handleMenuClick('signout')}
                    className="w-full px-4 py-2 text-left text-red-400 hover:bg-gray-700 flex items-center"
                  >
                    <LogOut className="w-4 h-4 mr-2" />
                    Sign Out
                  </button>
                </div>
              )}
            </div>

            <button className="md:hidden text-gray-300 hover:text-white">
              <Menu className="w-6 h-6" />
            </button>
          </div>
        </div>
        </div>
    </header>
  );
};
