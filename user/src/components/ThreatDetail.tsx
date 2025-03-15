import React from 'react';
import { X, AlertTriangle, Server, Clock, Shield } from 'lucide-react';
import { Threat } from '../types';
import { format } from 'date-fns';

interface ThreatDetailProps {
  threat: Threat;
  onClose: () => void;
  onResolve: (threatId: string) => void;
}

export const ThreatDetail: React.FC<ThreatDetailProps> = ({ threat, onClose, onResolve }) => {
  const getSeverityColor = (severity: Threat['severity']) => {
    switch (severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-gray-800 rounded-lg w-full max-w-2xl">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <h2 className="text-xl font-semibold text-white">Threat Details</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6">
          <div className="flex items-start space-x-4 mb-6">
            <AlertTriangle className={`w-6 h-6 ${
              getSeverityColor(threat.severity).replace('bg-', 'text-')
            }`} />
            <div>
              <h3 className="text-lg font-medium text-white">{threat.title}</h3>
              <p className="text-gray-400">{threat.description}</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-gray-900 p-4 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <Shield className="w-5 h-5 text-gray-400" />
                <span className="text-gray-300">Severity</span>
              </div>
              <span className={`px-2 py-1 rounded text-sm ${getSeverityColor(threat.severity)} text-white`}>
                {threat.severity.toUpperCase()}
              </span>
            </div>

            <div className="bg-gray-900 p-4 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <Clock className="w-5 h-5 text-gray-400" />
                <span className="text-gray-300">Detected</span>
              </div>
              <span className="text-white">
                {format(new Date(threat.timestamp), 'MMM d, HH:mm:ss')}
              </span>
            </div>

            <div className="bg-gray-900 p-4 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <Server className="w-5 h-5 text-gray-400" />
                <span className="text-gray-300">Source IP</span>
              </div>
              <span className="text-white">{threat.sourceIp}</span>
            </div>

            <div className="bg-gray-900 p-4 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <Server className="w-5 h-5 text-gray-400" />
                <span className="text-gray-300">Target System</span>
              </div>
              <span className="text-white">{threat.targetSystem}</span>
            </div>
          </div>

          <div className="mb-6">
            <h4 className="text-white font-medium mb-2">Event Logs</h4>
            <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm">
              {threat.logs?.map((log, index) => (
                <div key={index} className="text-gray-300">{log}</div>
              ))}
            </div>
          </div>

          {threat.status === 'active' && (
            <div className="flex justify-end">
              <button
                onClick={() => onResolve(threat.id)}
                className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
              >
                Mark as Resolved
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};