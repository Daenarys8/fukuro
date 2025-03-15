import React from 'react';
import { ConnectionsList } from './ConnectionsList';

export const Connections: React.FC = () => {
  // Mock data for demonstration
  const mockConnections = [
    {
      id: '1',
      sourceIp: '192.168.1.100',
      destinationIp: '192.168.1.1',
      protocol: 'TCP',
      port: 443,
      status: 'active',
      startTime: new Date().toISOString(),
      lastActivity: new Date().toISOString(),
      bytesTransferred: 1024
    },
    {
      id: '2',
      sourceIp: '192.168.1.101',
      destinationIp: '192.168.1.2',
      protocol: 'UDP',
      port: 53,
      status: 'active',
      startTime: new Date().toISOString(),
      lastActivity: new Date().toISOString(),
      bytesTransferred: 512
    }
  ] as const;

  const handleBlockIp = (ip: string) => {
    console.log('Blocking IP:', ip);
  };

  const handleQuarantine = (systemId: string) => {
    console.log('Quarantining system:', systemId);
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-6">Network Connections</h2>
      <ConnectionsList
        connections={mockConnections}
        onBlockIp={handleBlockIp}
        onQuarantine={handleQuarantine}
      />
    </div>
  );
};