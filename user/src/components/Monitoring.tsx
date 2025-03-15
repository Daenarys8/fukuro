import React from 'react';
import { NetworkGraph } from './NetworkGraph';
import { SystemMetrics } from './SystemMetrics';
import { LiveLogs } from './LiveLogs';

export const Monitoring: React.FC = () => {
  // Mock data for demonstration
  const mockHealth = {
    status: 'healthy',
    activeThreats: 2,
    resolvedThreats: 5,
    lastUpdated: new Date().toISOString(),
    cpuUsage: 45,
    memoryUsage: 60,
    diskUsage: 75
  };

  const mockNetworkStats = [{
    timestamp: new Date().toISOString(),
    connections: 150,
    bandwidth: 75,
    anomalies: 2,
    inboundTraffic: 1024,
    outboundTraffic: 512,
    blockedAttempts: 23
  }];

  const mockLogs = [
    { timestamp: new Date().toISOString(), message: 'System check completed', type: 'info' },
    { timestamp: new Date().toISOString(), message: 'Network scan initiated', type: 'info' },
    { timestamp: new Date().toISOString(), message: 'Unusual traffic detected', type: 'warning' }
  ];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-6">System Monitoring</h2>
      
      <SystemMetrics health={mockHealth} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <NetworkGraph data={mockNetworkStats} />
        <LiveLogs logs={mockLogs} />
      </div>
    </div>
  );
};