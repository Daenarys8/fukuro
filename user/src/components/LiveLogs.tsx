import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { Terminal } from 'lucide-react';

interface Log {
  timestamp: string;
  message: string;
  type: 'info' | 'warning' | 'error';
}

interface LiveLogsProps {
  logs: Log[];
}

export const LiveLogs: React.FC<LiveLogsProps> = ({ logs }) => {
  const [currentTime, setCurrentTime] = useState(format(new Date(), 'HH:mm:ss'));

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentTime(format(new Date(), 'HH:mm:ss'));
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  const getLogColor = (type: Log['type']) => {
    switch (type) {
      case 'error': return 'text-red-400';
      case 'warning': return 'text-yellow-400';
      default: return 'text-blue-400';
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="p-4 border-b border-gray-700 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Terminal className="w-5 h-5 text-gray-400" />
          <h2 className="text-lg font-semibold text-white">Live System Logs</h2>
        </div>
        <span className="text-sm text-gray-400">
          Last updated: {currentTime}
        </span>
      </div>
      <div className="p-4 max-h-96 overflow-y-auto font-mono text-sm">
        {Array.isArray(logs) && logs.length > 0 ? (
          logs.map((log, index) => {
            const logTimestamp = new Date(log.timestamp);
            const isValidTimestamp = !isNaN(logTimestamp.getTime());
            return (
              <div key={index} className="py-1">
                <span className="text-gray-500">
                  [{isValidTimestamp ? format(logTimestamp, 'HH:mm:ss') : 'Invalid Timestamp'}]
                </span>
                <span className={`ml-2 ${getLogColor(log.type)}`}>{log.message}</span>
              </div>
            );
          })
        ) : (
          <div>No logs available</div>
        )}
      </div>
    </div>
  );
};
