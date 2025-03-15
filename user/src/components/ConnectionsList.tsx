import React from 'react';
import { Network, Shield, AlertCircle } from 'lucide-react';
import { Connection } from '../types/security';

interface ConnectionsListProps {
  connections: Connection[];
  onBlockIp: (ip: string) => void;
  onQuarantine: (systemId: string) => void;
}

export const ConnectionsList: React.FC<ConnectionsListProps> = ({
  connections,
  onBlockIp,
  onQuarantine
}) => {
  const getStatusColor = (status: Connection['status']) => {
    switch (status) {
      case 'active': return 'text-green-400';
      case 'blocked': return 'text-red-400';
      case 'quarantined': return 'text-yellow-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="p-4 border-b border-gray-700 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Network className="w-5 h-5 text-blue-400" />
          <h2 className="text-lg font-semibold text-white">Active Connections</h2>
        </div>
        <span className="text-sm text-gray-400">
          {connections.length} connections
        </span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-left text-gray-400 text-sm">
              <th className="p-4">Source IP</th>
              <th className="p-4">Destination IP</th>
              <th className="p-4">Protocol</th>
              <th className="p-4">Port</th>
              <th className="p-4">Status</th>
              <th className="p-4">Duration</th>
              <th className="p-4">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {connections.map(connection => (
              <tr key={connection.id} className="hover:bg-gray-700">
                <td className="p-4 text-white">{connection.sourceIp}</td>
                <td className="p-4 text-white">{connection.destinationIp}</td>
                <td className="p-4 text-gray-300">{connection.protocol}</td>
                <td className="p-4 text-gray-300">{connection.port}</td>
                <td className="p-4">
                  <span className={`${getStatusColor(connection.status)}`}>
                    {connection.status}
                  </span>
                </td>
                <td className="p-4 text-gray-300">
                  {new Date(connection.startTime).toLocaleTimeString()}
                </td>
                <td className="p-4">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => onBlockIp(connection.sourceIp)}
                      className="p-1 text-red-400 hover:text-red-300 transition-colors"
                      title="Block IP"
                    >
                      <Shield className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => onQuarantine(connection.id)}
                      className="p-1 text-yellow-400 hover:text-yellow-300 transition-colors"
                      title="Quarantine"
                    >
                      <AlertCircle className="w-5 h-5" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};