import React from 'react';
import { Activity, Server, HardDrive } from 'lucide-react';
import { SystemHealth } from '../types/security';

interface SystemMetricsProps {
  health: SystemHealth;
}

export const SystemMetrics: React.FC<SystemMetricsProps> = ({ health }) => {
  const getUsageColor = (usage: number) => {
    if (usage >= 90) return 'text-red-400';
    if (usage >= 70) return 'text-yellow-400';
    return 'text-green-400';
  };

  const metrics = [
    {
      icon: Activity,
      label: 'CPU Usage',
      value: health.cpuUsage,
      color: getUsageColor(health.cpuUsage)
    },
    {
      icon: Server,
      label: 'Memory Usage',
      value: health.memoryUsage,
      color: getUsageColor(health.memoryUsage)
    },
    {
      icon: HardDrive,
      label: 'Disk Usage',
      value: health.diskUsage,
      color: getUsageColor(health.diskUsage)
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {metrics.map((metric, index) => (
        <div key={index} className="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <metric.icon className={`w-5 h-5 ${metric.color}`} />
            <span className="text-gray-400 text-sm">{metric.label}</span>
          </div>
          <div className="mt-2">
            <div className="flex items-center justify-between">
              <span className={`text-2xl font-bold ${metric.color}`}>
                {metric.value}%
              </span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
              <div
                className={`h-2 rounded-full ${metric.color.replace('text', 'bg')}`}
                style={{ width: `${metric.value}%` }}
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};