import axios from 'axios';
import type { 
  Threat, 
  SystemHealth, 
  NetworkStats,
  ThreatResolutionRequest,
  ModelMetrics,
  AnalysisRequest
} from '../types';

// Get the API URL from environment or default to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Log the API URL in development
if (import.meta.env.DEV) {
    console.log('API URL:', API_BASE_URL);
}

// Fetch threats
export const fetchThreats = async (): Promise<{
  threats: Threat[],
  threat_level: string,
  anomaly_count: number
}> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/threats`);
    return response.data; // Backend returns ThreatListResponse
  } catch (error) {
    console.error('Error fetching threats:', error);
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch threats');
    }
    throw new Error('Failed to fetch threats');
  }
};

// Fetch system health
export const fetchSystemHealth = async (): Promise<SystemHealth> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);  // Updated endpoint
    return response.data;  // Ensure the backend returns this structure
  } catch (error) {
    console.error('Error fetching system health', error);
    throw new Error('Failed to fetch system health');
  }
};

// Fetch system stats (updated network stats endpoint)
export const fetchStats = async (): Promise<NetworkStats> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/stats/network`);  // Updated endpoint
    return response.data;  // Ensure the backend returns this structure
  } catch (error) {
    console.error('Error fetching system stats', error);
    throw new Error('Failed to fetch system stats');
  }
};

// Ingest logs
export const ingestLog = async (source: string, content: any): Promise<void> => {
  try {
    await axios.post(`${API_BASE_URL}/ingest`, {
      source,
      content
    });
  } catch (error) {
    console.error('Error ingesting log', error);
    throw new Error('Failed to ingest log');
  }
};

// Analyze logs
export const analyzeLogs = async (request: AnalysisRequest): Promise<any> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, request);
    return response.data;  // Ensure the backend returns this structure
  } catch (error) {
    console.error('Error analyzing logs', error);
    throw new Error('Failed to analyze logs');
  }
};

// Detect anomalies
export const detectAnomaly = async (source: string, logs: any[], windowMinutes: number = 5): Promise<any> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/detect`, {
      source,
      logs,
      window_minutes: windowMinutes
    });
    return response.data;  // Ensure the backend returns this structure
  } catch (error) {
    console.error('Error detecting anomaly', error);
    throw new Error('Failed to detect anomaly');
  }
};

// Train model
export const trainModel = async (source: string, logs: any[], windowMinutes: number = 5): Promise<any> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/train`, {
      source,
      logs,
      window_minutes: windowMinutes
    });
    return response.data;  // Ensure the backend returns this structure
  } catch (error) {
    console.error('Error training model', error);
    throw new Error('Failed to train model');
  }
};

// Execute response action
export const executeAction = async (actionType: string, target: string, parameters: any, anomalyId?: number): Promise<void> => {
  try {
    await axios.post(`${API_BASE_URL}/respond`, {  // Updated endpoint
      action_type: actionType,
      target,
      parameters,
      anomaly_id: anomalyId
    });
  } catch (error) {
    console.error('Error executing action', error);
    throw new Error('Failed to execute action');
  }
};

// Resolve a threat
export const resolveThreat = async (threatId: string): Promise<void> => {
  try {
    const request: ThreatResolutionRequest = { 
      threatId,
      resolution: {
        action: 'block',
        timestamp: new Date().toISOString()
      }
    };
    await axios.post(`${API_BASE_URL}/resolve-threat`, request);  // Endpoint for threat resolution
  } catch (error) {
    console.error('Error resolving threat', error);
    throw new Error('Failed to resolve threat');
  }
};
