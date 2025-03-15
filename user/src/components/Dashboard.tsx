import React from 'react';
import { AlertTriangle, CheckCircle, Activity } from 'lucide-react';
import { SystemHealth } from '../types/security';
import { format } from 'date-fns';

interface DashboardProps {
  health: SystemHealth;
}

// Function to validate timestamp
const isValidTimestamp = (timestamp: string) => {
  const date = new Date(timestamp);
  return !isNaN(date.getTime()); // Check if valid date
};

export const Dashboard: React.FC<DashboardProps> = ({ health }) => {
  const validTimestamp = isValidTimestamp(health.lastUpdated);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-300">System Status</h3>
          <Activity className={`w-6 h-6 ${
            health.status === 'healthy' ? 'text-green-400' :
            health.status === 'warning' ? 'text-yellow-400' :
            'text-red-400'
          }`} />
        </div>
        <p className="mt-2 text-2xl font-bold text-white capitalize">{health.status}</p>
        <p className="text-sm text-gray-400">
          Last updated: {validTimestamp ? format(new Date(health.lastUpdated), 'HH:mm:ss') : 'Invalid time'}
        </p>
      </div>

      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-300">Active Threats</h3>
          <AlertTriangle className="w-6 h-6 text-red-400" />
        </div>
        <p className="mt-2 text-2xl font-bold text-white">{health.activeThreats}</p>
        <p className="text-sm text-gray-400">Requiring immediate attention</p>
      </div>

      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-300">Resolved Threats</h3>
          <CheckCircle className="w-6 h-6 text-green-400" />
        </div>
        <p className="mt-2 text-2xl font-bold text-white">{health.resolvedThreats}</p>
        <p className="text-sm text-gray-400">In the last 24 hours</p>
      </div>
    </div>
  );
};
