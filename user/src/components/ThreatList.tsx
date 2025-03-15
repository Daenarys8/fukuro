import React from 'react';
import { AlertTriangle, CheckCircle } from 'lucide-react';
import { Threat } from '../types';
import { format } from 'date-fns';

interface ThreatListProps {
  threats: Threat[];
  onSelectThreat: (threat: Threat) => void;
}

export const ThreatList: React.FC<ThreatListProps> = ({ threats, onSelectThreat }) => {
  const getSeverityColor = (severity: Threat['severity']) => {
    switch (severity) {
      case 'critical': return 'text-red-500';
      case 'high': return 'text-orange-500';
      case 'medium': return 'text-yellow-500';
      case 'low': return 'text-blue-500';
      default: return 'text-gray-500';
    }
  };

  // Function to validate timestamp
  const isValidTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return !isNaN(date.getTime()); // Check if valid date
  };

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-xl font-semibold text-white">Recent Threats</h2>
      </div>
      <div className="divide-y divide-gray-700">
        {Array.isArray(threats) && threats.length > 0 ? (
          threats.map((threat) => {
            const validTimestamp = isValidTimestamp(threat.timestamp);
            return (
              <div
                key={threat.id}
                className="p-4 hover:bg-gray-700 cursor-pointer transition-colors"
                onClick={() => onSelectThreat(threat)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3">
                    {threat.status === 'active' ? (
                      <AlertTriangle className={`w-5 h-5 mt-1 ${getSeverityColor(threat.severity)}`} />
                    ) : (
                      <CheckCircle className="w-5 h-5 mt-1 text-green-500" />
                    )}
                    <div>
                      <h3 className="font-medium text-white">{threat.title}</h3>
                      <p className="text-sm text-gray-400">{threat.description}</p>
                      <div className="mt-2 flex items-center space-x-4 text-sm">
                        <span className="text-gray-500">
                          {validTimestamp
                            ? format(new Date(threat.timestamp), 'MMM d, HH:mm')
                            : 'Invalid timestamp'}
                        </span>
                        <span className={`font-medium ${getSeverityColor(threat.severity)}`}>
                          {threat.severity.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })
        ) : (
          <div className="text-white p-4">No threats available.</div>
        )}
      </div>
    </div>
  );
};
