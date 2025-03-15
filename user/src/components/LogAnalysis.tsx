import React, { useState } from 'react';
import { analyzeLogs } from '../api/mockApi';
import type { AnalysisRequest } from '../api/types';

export const LogAnalysis: React.FC = () => {
  const [logData, setLogData] = useState('');
  const [analysisType, setAnalysisType] = useState<'gpt4' | 'mistral'>('gpt4');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsAnalyzing(true);
    setError('');
    setResult(null);

    try {
      const request: AnalysisRequest = {
        log_data: logData,
        analysis_type: analysisType
      };
      const analysisResult = await analyzeLogs(request);
      setResult(analysisResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze logs');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-xl font-semibold text-white mb-4">Log Analysis</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Log Data
          </label>
          <textarea
            value={logData}
            onChange={(e) => setLogData(e.target.value)}
            className="w-full bg-gray-700 text-white rounded-md px-3 py-2 h-32"
            placeholder="Enter log data to analyze"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Analysis Type
          </label>
          <select
            value={analysisType}
            onChange={(e) => setAnalysisType(e.target.value as 'gpt4' | 'mistral')}
            className="w-full bg-gray-700 text-white rounded-md px-3 py-2"
          >
            <option value="gpt4">GPT-4</option>
            <option value="mistral">Mistral</option>
          </select>
        </div>

        {error && (
          <div className="text-red-500 text-sm">{error}</div>
        )}

        {result && (
          <div className="bg-gray-900 rounded-lg p-4 mt-4">
            <h3 className="text-white font-medium mb-2">Analysis Result</h3>
            <pre className="text-gray-300 text-sm overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}

        <button
          type="submit"
          disabled={isAnalyzing}
          className={`w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors ${
            isAnalyzing ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyze Logs'}
        </button>
      </form>
    </div>
  );
};