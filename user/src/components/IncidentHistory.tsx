import React, { useState } from 'react';
import { Calendar, Filter, Download, Search } from 'lucide-react';

export const IncidentHistory: React.FC = () => {
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Mock data for demonstration
  const mockIncidents = [
    {
      id: '1',
      title: 'Brute Force Attack',
      description: 'Multiple failed login attempts detected from IP 192.168.1.100',
      severity: 'high',
      status: 'resolved',
      timestamp: '2024-03-10T10:15:23Z',
      resolvedAt: '2024-03-10T10:30:00Z',
      resolvedBy: 'John Doe'
    },
    {
      id: '2',
      title: 'Suspicious File Access',
      description: 'Unauthorized access attempt to sensitive files',
      severity: 'medium',
      status: 'resolved',
      timestamp: '2024-03-09T15:20:00Z',
      resolvedAt: '2024-03-09T15:45:00Z',
      resolvedBy: 'Jane Smith'
    },
    {
      id: '3',
      title: 'Port Scan Detected',
      description: 'Sequential port scan from external IP address',
      severity: 'low',
      status: 'resolved',
      timestamp: '2024-03-08T08:00:00Z',
      resolvedAt: '2024-03-08T08:30:00Z',
      resolvedBy: 'Mike Johnson'
    }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'text-red-400';
      case 'medium': return 'text-yellow-400';
      case 'low': return 'text-blue-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-lg border border-gray-700">
        <div className="p-4 border-b border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-white">Incident History</h2>
            <div className="flex items-center space-x-4">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search incidents..."
                  className="bg-gray-700 text-white rounded-md pl-8 pr-4 py-1 text-sm w-64"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Search className="w-4 h-4 text-gray-400 absolute left-2 top-2" />
              </div>
              <div className="flex items-center space-x-2">
                <Filter className="w-4 h-4 text-gray-400" />
                <select
                  className="bg-gray-700 text-white rounded-md px-2 py-1 text-sm"
                  value={filter}
                  onChange={(e) => setFilter(e.target.value)}
                >
                  <option value="all">All Severities</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>
              <button className="flex items-center space-x-1 text-gray-400 hover:text-white">
                <Download className="w-4 h-4" />
                <span className="text-sm">Export</span>
              </button>
            </div>
          </div>
        </div>
        <div className="divide-y divide-gray-700">
          {mockIncidents.map((incident) => (
            <div key={incident.id} className="p-4 hover:bg-gray-700 transition-colors">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-lg font-medium text-white">{incident.title}</h3>
                  <p className="text-gray-400 mt-1">{incident.description}</p>
                  <div className="flex items-center space-x-4 mt-2">
                    <span className={`${getSeverityColor(incident.severity)} text-sm`}>
                      {incident.severity.toUpperCase()}
                    </span>
                    <span className="text-gray-500 text-sm flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {new Date(incident.timestamp).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-400">
                    Resolved by: {incident.resolvedBy}
                  </div>
                  <div className="text-sm text-gray-500">
                    {new Date(incident.resolvedAt).toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};