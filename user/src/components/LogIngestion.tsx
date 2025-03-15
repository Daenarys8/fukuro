import React, { useState } from 'react';
import { ingestLog } from '../api/mockApi';

export const LogIngestion: React.FC = () => {
  const [source, setSource] = useState('');
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      let parsedContent;
      try {
        parsedContent = JSON.parse(content);
      } catch (jsonError) {
        throw new Error('Invalid JSON format');
      }

      // Log the parsed content to verify the structure
      console.log('Parsed Content:', parsedContent);

      // Ensure the required fields for 'suricata' are present
      if (source === 'suricata') {
        const requiredFields = ['timestamp', 'event_type', 'data'];
        for (const field of requiredFields) {
          if (!parsedContent[field]) {
            throw new Error(`Missing required field: ${field}`);
          }
        }

        // Ensure 'data' object is present and correctly structured
        if (parsedContent.data && parsedContent.data.flow) {
          const flow = parsedContent.data.flow;

          // Ensure 'start' and 'end' are in correct ISO format
          if (flow.start && flow.end) {
            flow.start = new Date(flow.start).toISOString(); // Convert to ISO format
            flow.end = new Date(flow.end).toISOString(); // Convert to ISO format
          } else {
            throw new Error('Missing or incorrect date format for flow start or end');
          }
        } else {
          throw new Error('Missing flow data in "data" field');
        }
      }

      // Log the final data structure before sending it
      console.log('Final Data to Send:', { source, parsedContent });

      // Send the log to the API
      await ingestLog(source, parsedContent);
      setSuccess('Log ingested successfully');
      setSource('');
      setContent('');
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-xl font-semibold text-white mb-4">Log Ingestion</h2>
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
            Content (JSON)
          </label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full bg-gray-700 text-white rounded-md px-3 py-2 h-32"
            placeholder="Enter JSON content"
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
          disabled={isLoading}
          className={`w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition-colors ${
            isLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {isLoading ? 'Ingesting...' : 'Ingest Log'}
        </button>
      </form>
    </div>
  );
};
