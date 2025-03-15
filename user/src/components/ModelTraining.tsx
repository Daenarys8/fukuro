import React, { useState } from 'react';
import { trainModel } from '../api/mockApi';
import { ModelMetricsDisplay } from './ModelMetricsDisplay';
import { ModelMetrics } from '../api/types';

export const ModelTraining: React.FC = () => {
  const [source, setSource] = useState('');
  const [windowMinutes, setWindowMinutes] = useState(5);
  const [isTraining, setIsTraining] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsTraining(true);
    setError('');
    setSuccess('');

    try {
      const result = await trainModel(source, [], windowMinutes);
      setSuccess('Model training completed successfully');
      setMetrics(result.metrics);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to train model');
    } finally {
      setIsTraining(false);
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-xl font-semibold text-white mb-4">Model Training</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Source
          </label>
          <select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            className="w-full bg-gray-700 text-white rounded-md px-3 py-2"
            required
          >
            <option value="">Select source</option>
            <option value="zeek">Zeek</option>
            <option value="suricata">Suricata</option>
            <option value="osquery">OSQuery</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Window Minutes
          </label>
          <input
            type="number"
            value={windowMinutes}
            onChange={(e) => setWindowMinutes(Number(e.target.value))}
            min="1"
            max="60"
            className="w-full bg-gray-700 text-white rounded-md px-3 py-2"
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
          disabled={isTraining}
          className={`w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors ${
            isTraining ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {isTraining ? 'Training...' : 'Train Model'}
        </button>
      </form>

      {metrics && (
        <div className="mt-6">
          <ModelMetricsDisplay metrics={metrics} />
        </div>
      )}
    </div>
  );
};