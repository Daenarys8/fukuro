import React, { useState, useEffect } from 'react';
import { ThreatList } from './ThreatList';
import { ThreatDetail } from './ThreatDetail';
import { ResponseAction } from './ResponseAction';
import { fetchThreats, resolveThreat } from '../api/mockApi';
import { Threat } from '../types';

export const ThreatManagement: React.FC = () => {
  const [threats, setThreats] = useState<Threat[]>([]);
  const [selectedThreat, setSelectedThreat] = useState<Threat | null>(null);
  const [error, setError] = useState('');

  const loadThreats = async () => {
    try {
      const fetchedThreats = await fetchThreats();
      setThreats(fetchedThreats);
    } catch (err) {
      setError('Failed to fetch threats');
    }
  };

  useEffect(() => {
    loadThreats();
  }, []);

  const handleResolveThreat = async (threatId: string) => {
    try {
      await resolveThreat(threatId);
      await loadThreats(); // Reload the list
      setSelectedThreat(null); // Close the detail view
    } catch (err) {
      setError('Failed to resolve threat');
    }
  };

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-500 text-white p-4 rounded-lg">{error}</div>
      )}
      
      <ThreatList
        threats={threats}
        onSelectThreat={setSelectedThreat}
      />

      {selectedThreat && (
        <ThreatDetail
          threat={selectedThreat}
          onClose={() => setSelectedThreat(null)}
          onResolve={handleResolveThreat}
        />
      )}

      <ResponseAction
        anomalyId={selectedThreat?.id ? parseInt(selectedThreat.id) : undefined}
      />
    </div>
  );
};