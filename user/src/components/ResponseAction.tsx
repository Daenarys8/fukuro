import React, { useState } from 'react';
import { executeAction } from '../api/mockApi';

interface ResponseActionProps {
  anomalyId?: number;
}

export const ResponseAction: React.FC<ResponseActionProps> = ({ anomalyId }) => {
  const [actionType, setActionType] = useState('');
  const [target, setTarget] = useState('');
  const [parameters, setParameters] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsExecuting(true);
    setError('');
    setSuccess('');

    try {
      let parsedParams;
      try {
        parsedParams = JSON.parse(parameters);
      } catch {
        throw new Error('Invalid JSON in parameters');
      }

      await executeAction(actionType, target, parsedParams, anomalyId);
      setSuccess('Response action executed successfully');
      setActionType('');
      setTarget('');
      setParameters('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to execute action');
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-xl font-semibold text-white mb-4">Execute Response Action</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Action Type
          </label>
          <select
            value={actionType}
            onChange={(e) => setActionType(e.target.value)}
            className="w-full bg-gray-700 text-white rounded-md px-3 py-2"
            required
          >
            <option value="">Select action type</option>
            <option value="quarantine">Quarantine</option>
            <option value="alert">Alert</option>
            <option value="firewall">Firewall Rule</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Target
          </label>
          <input
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            className="w-full bg-gray-700 text-white rounded-md px-3 py-2"
            placeholder="IP address, hostname, or identifier"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Parameters (JSON)
          </label>
          <textarea
            value={parameters}
            onChange={(e) => setParameters(e.target.value)}
            className="w-full bg-gray-700 text-white rounded-md px-3 py-2 h-32"
            placeholder="Enter parameters as JSON"
            required
          />
        </div>

        {error && (
          <div className="text-red-500 text-sm">{error}</div>
        )}

        {success && (
          <div className="text-green-500 text-sm">{success}</div>
        )}

        <button
          type="submit"
          disabled={isExecuting}
          className={`w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors ${
            isExecuting ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {isExecuting ? 'Executing...' : 'Execute Action'}
        </button>
      </form>
    </div>
  );
};