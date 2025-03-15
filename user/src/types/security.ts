export type ThreatSeverity = 'low' | 'medium' | 'high' | 'critical';
export type ThreatStatus = 'active' | 'resolved';

export interface Threat {
  id: string;
  title: string;
  description: string;
  severity: ThreatSeverity;
  status: ThreatStatus;
  timestamp: string;
  sourceIp?: string;
  targetSystem?: string;
  logs?: string[];
}

export interface SystemHealth {
  status: 'healthy' | 'warning' | 'critical';
  activeThreats: number;
  resolvedThreats: number;
  lastUpdated: string;
}

export interface NetworkStats {
  total_connections: number;
  unique_ips: number;
  last_hour_connections: number;
}

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  training_date?: string;
}

export interface AnalysisRequest {
  log_data: string;
  analysis_type: 'gpt4' | 'mistral';
}

export interface ApiResponse {
  message: string;
  timestamp: string;
}

export interface ThreatResolutionRequest {
  threatId: string;
  resolution: {
    action: 'block' | 'quarantine' | 'monitor';
    notes?: string;
    timestamp: string;
  };
}

// Connection types
export interface Connection {
  id: string;
  sourceIp: string;
  destinationIp: string;
  protocol: string;
  port: number;
  status: 'active' | 'blocked' | 'quarantined';
  startTime: string;
  lastActivity: string;
  bytesTransferred: number;
}