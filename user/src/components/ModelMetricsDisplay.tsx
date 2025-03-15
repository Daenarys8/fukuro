import React from 'react';
import { ModelMetrics } from '../api/types';

interface ModelMetricsDisplayProps {
  metrics: ModelMetrics;
}

export const ModelMetricsDisplay: React.FC<ModelMetricsDisplayProps> = ({ metrics }) => {
  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-lg font-medium text-white mb-4">Model Metrics</h3>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-700 p-4 rounded-lg">
          <div className="text-sm text-gray-400">Accuracy</div>
          <div className="text-lg text-white">{(metrics.accuracy * 100).toFixed(2)}%</div>
        </div>
        <div className="bg-gray-700 p-4 rounded-lg">
          <div className="text-sm text-gray-400">Precision</div>
          <div className="text-lg text-white">{(metrics.precision * 100).toFixed(2)}%</div>
        </div>
        <div className="bg-gray-700 p-4 rounded-lg">
          <div className="text-sm text-gray-400">Recall</div>
          <div className="text-lg text-white">{(metrics.recall * 100).toFixed(2)}%</div>
        </div>
        <div className="bg-gray-700 p-4 rounded-lg">
          <div className="text-sm text-gray-400">F1 Score</div>
          <div className="text-lg text-white">{(metrics.f1_score * 100).toFixed(2)}%</div>
        </div>
      </div>
      {metrics.training_date && (
        <div className="mt-4 text-sm text-gray-400">
          Last trained: {new Date(metrics.training_date).toLocaleString()}
        </div>
      )}
    </div>
  );
};