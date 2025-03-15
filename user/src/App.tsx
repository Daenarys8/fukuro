import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './components/Dashboard';
import { ThreatList } from './components/ThreatList';
import { ThreatDetail } from './components/ThreatDetail';
import { NetworkGraph } from './components/NetworkGraph';
import { LiveLogs } from './components/LiveLogs';
import { LogIngestion } from './components/LogIngestion';
import { ModelTraining } from './components/ModelTraining';
import { LogAnalysis } from './components/LogAnalysis';
import { ThreatManagement } from './components/ThreatManagement';
import { Settings } from './components/Settings';
import { Monitoring } from './components/Monitoring';
import { Connections } from './components/Connections';
import { HelpSupport } from './components/HelpSupport';
import { IncidentHistory } from './components/IncidentHistory';
import {
  fetchThreats,
  fetchSystemHealth,
  fetchStats,
  resolveThreat
} from './api/mockApi';
import type { Threat, SystemHealth, NetworkStats } from './types';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [threats, setThreats] = useState<Threat[]>([]);
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [networkStats, setNetworkStats] = useState<NetworkStats[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedThreat, setSelectedThreat] = useState<Threat | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [threatsData, healthData, statsData] = await Promise.all([
          fetchThreats(),
          fetchSystemHealth(),
          fetchStats()
        ]);
        setThreats(threatsData);
        setHealth(healthData);
        setNetworkStats([statsData]); // Ensure this is in the correct format
      } catch (err) {
        setError('Failed to fetch security data');
      } finally {
        setLoading(false);
      }
    };

    loadInitialData();

    // Set up polling for real-time updates
    const pollInterval = setInterval(async () => {
      try {
        const [newHealth, newStats] = await Promise.all([
          fetchSystemHealth(),
          fetchStats()
        ]);
        setHealth(newHealth);
        setNetworkStats(prev => [...prev.slice(-19), newStats]);
      } catch (err) {
        console.error('Failed to update real-time data:', err);
      }
    }, 5000);

    return () => clearInterval(pollInterval);
  }, []);

  const handleResolveThreat = async (threatId: string) => {
    try {
      await resolveThreat(threatId);
      setThreats(threats.map(threat =>
        threat.id === threatId
          ? { ...threat, status: 'resolved' as const }
          : threat
      ));
      setSelectedThreat(null);
    } catch (err) {
      setError('Failed to resolve threat');
    }
  };

  const handleSignOut = () => {
    setIsAuthenticated(false);
    setCurrentPage('dashboard');
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="bg-gray-800 p-8 rounded-lg shadow-lg">
          <h1 className="text-2xl font-bold text-white mb-4">Signed Out</h1>
          <p className="text-gray-400 mb-4">You have been successfully signed out.</p>
          <button
            onClick={() => setIsAuthenticated(true)}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Sign In Again
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white">Loading security dashboard...</div>
      </div>
    );
  }

  if (error || !health) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-red-400">{error || 'Failed to load dashboard'}</div>
      </div>
    );
  }

  // Conditionally render pages based on currentPage state
  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return (
          <>
            <Dashboard health={health} />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <NetworkGraph data={networkStats} />
              <LiveLogs logs={logs} />
            </div>
            <ThreatList threats={threats} onSelectThreat={setSelectedThreat} />
          </>
        );
      case 'threats':
        return <ThreatManagement />;
      case 'monitoring':
        return <Monitoring />;
      case 'connections':
        return <Connections />;
      case 'network':
        return <NetworkGraph data={networkStats} />;
        case 'incidents':
        return <IncidentHistory />;
        case 'settings':
          return <Settings />;
        case 'help':
          return <HelpSupport />;  
      case 'logs':
        return (
          <div className="space-y-6">
            <LogIngestion />
            <LogAnalysis />
          </div>
        );
      case 'model':
        return <ModelTraining />;
      default:
        return <Dashboard health={health} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-900">
      <Header onNavigate={setCurrentPage} onSignOut={handleSignOut} />
      <Sidebar onNavigate={setCurrentPage} currentPage={currentPage} />
      
      <main className="ml-64 pt-16">
        <div className="p-8">
          {renderPage()}
        </div>
      </main>

      {selectedThreat && (
        <ThreatDetail
          threat={selectedThreat}
          onClose={() => setSelectedThreat(null)}
          onResolve={handleResolveThreat}
        />
      )}
    </div>
  );
}

export default App;
