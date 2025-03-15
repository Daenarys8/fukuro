import React, { useState } from 'react';
import { 
  Home, 
  Shield, 
  Activity, 
  FileText, 
  ChevronLeft, 
  ChevronRight,
  Settings,
  Bell,
  Users,
  Network,
  Database
} from 'lucide-react';

interface MenuItem {
  id: string;
  label: string;
  icon: React.ElementType;
  badge?: number;
  subItems?: MenuItem[];
}

interface SidebarProps {
  onNavigate: (page: string) => void;
  currentPage: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ onNavigate, currentPage }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [expandedGroup, setExpandedGroup] = useState<string | null>(null);

  const menuItems: MenuItem[] = [
    { 
      id: 'dashboard', 
      label: 'Dashboard', 
      icon: Home 
    },
    { 
      id: 'security', 
      label: 'Security', 
      icon: Shield,
      subItems: [
        { id: 'threats', label: 'Active Threats', icon: Bell, badge: 3 },
        { id: 'incidents', label: 'Incident History', icon: FileText },
        { id: 'policies', label: 'Security Policies', icon: Database }
      ]
    },
    { 
      id: 'network', 
      label: 'Network', 
      icon: Network,
      subItems: [
        { id: 'monitoring', label: 'Monitoring', icon: Activity },
        { id: 'connections', label: 'Connections', icon: Users },
        { id: 'logs', label: 'Network Logs', icon: FileText }
      ]
    },
    { 
      id: 'settings', 
      label: 'Settings', 
      icon: Settings 
    }
  ];

  const handleMenuClick = (item: MenuItem) => {
    if (item.subItems) {
      setExpandedGroup(expandedGroup === item.id ? null : item.id);
    } else {
      onNavigate(item.id);
      if (isCollapsed) {
        setExpandedGroup(null);
      }
    }
  };

  const renderMenuItem = (item: MenuItem, isSubItem = false) => (
    <button
      key={item.id}
      onClick={() => handleMenuClick(item)}
      className={`
        w-full flex items-center px-4 py-3 text-gray-300 hover:bg-gray-700 
        hover:text-white transition-colors relative group
        ${currentPage === item.id ? 'bg-gray-700 text-white' : ''}
        ${isSubItem ? 'pl-12' : ''}
      `}
    >
      <item.icon className="w-5 h-5 min-w-[1.25rem]" />
      {!isCollapsed && (
        <>
          <span className="ml-3 truncate">{item.label}</span>
          {item.badge && (
            <span className="ml-auto bg-red-500 text-white text-xs px-2 py-1 rounded-full">
              {item.badge}
            </span>
          )}
        </>
      )}
      {isCollapsed && (
        <div className="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white rounded-md opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50">
          {item.label}
          {item.badge && (
            <span className="ml-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
              {item.badge}
            </span>
          )}
        </div>
      )}
    </button>
  );

  return (
    <div 
      className={`
        bg-gray-800 h-screen fixed left-0 top-16 transition-all duration-300 
        border-r border-gray-700 overflow-hidden
        ${isCollapsed ? 'w-16' : 'w-64'}
      `}
    >
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-3 top-4 bg-gray-700 rounded-full p-1 text-gray-300 hover:text-white hover:bg-gray-600 transition-colors"
      >
        {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>

      <div className="py-4">
        <div className="space-y-1">
          {menuItems.map(item => (
            <React.Fragment key={item.id}>
              {renderMenuItem(item)}
              {!isCollapsed && item.subItems && expandedGroup === item.id && (
                <div className="bg-gray-900 bg-opacity-50">
                  {item.subItems.map(subItem => renderMenuItem(subItem, true))}
                </div>
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {!isCollapsed && (
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-700">
          <div className="flex items-center space-x-3 text-gray-400">
            <div className="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center">
              <Users size={18} />
            </div>
            <div className="flex-1">
              <div className="text-sm font-medium text-gray-300">Security Team</div>
              <div className="text-xs">5 members online</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};