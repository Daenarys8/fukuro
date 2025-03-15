from typing import List, Dict, Any
import numpy as np
from datetime import datetime, timedelta
import ipaddress
from collections import defaultdict

class FeatureExtractor:
    def __init__(self):
        self.feature_names = []
        self._initialize_features()

    def _initialize_features(self):
        """Initialize feature names for different log types."""
        self.zeek_features = [
            'bytes_per_second',
            'packets_per_second',
            'unique_ips',
            'connection_duration',
            'bytes_ratio',
            'local_network_ratio',
            'error_ratio'
        ]
        
        self.suricata_features = [
            'alert_severity_avg',
            'unique_signatures',
            'event_frequency',
            'high_severity_ratio',
            'source_ip_diversity',
            'protocol_entropy'
        ]
        
        self.osquery_features = [
            'process_events_frequency',
            'file_events_frequency',
            'network_events_frequency',
            'user_events_frequency',
            'system_events_frequency'
        ]

    def _calculate_entropy(self, values: List[Any]) -> float:
        """Calculate Shannon entropy for a list of values."""
        if not values:
            return 0.0
        
        value_counts = defaultdict(int)
        for value in values:
            value_counts[value] += 1
        
        total = len(values)
        entropy = 0.0
        
        for count in value_counts.values():
            probability = count / total
            entropy -= probability * np.log2(probability)
        
        return entropy

    def extract_zeek_features(self, logs: List[Dict[str, Any]], window_minutes: int = 5) -> List[float]:
        """Extract features from Zeek logs within a time window."""
        if not logs:
            return [0.0] * len(self.zeek_features)

        # Group logs by time window
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=window_minutes)
        window_logs = [log for log in logs if start_time <= log['timestamp'] <= end_time]

        if not window_logs:
            return [0.0] * len(self.zeek_features)

        # Calculate features
        total_bytes = sum(log.get('orig_bytes', 0) + log.get('resp_bytes', 0) for log in window_logs)
        total_packets = sum(log.get('orig_pkts', 0) + log.get('resp_pkts', 0) for log in window_logs)
        unique_ips = len(set(log['source_ip'] for log in window_logs) | set(log['dest_ip'] for log in window_logs))
        avg_duration = np.mean([log.get('duration', 0) for log in window_logs])
        
        bytes_ratio = np.mean([
            log.get('orig_bytes', 0) / (log.get('resp_bytes', 1) or 1)
            for log in window_logs if log.get('resp_bytes', 0) > 0
        ])

        local_connections = sum(1 for log in window_logs if log.get('local_orig', False))
        local_ratio = local_connections / len(window_logs)

        error_states = ['S0', 'REJ', 'RSTO', 'RSTOS0', 'RSTRH', 'SH', 'SHR']
        error_ratio = sum(1 for log in window_logs if log.get('conn_state', '') in error_states) / len(window_logs)

        return [
            total_bytes / (window_minutes * 60),  # bytes per second
            total_packets / (window_minutes * 60),  # packets per second
            unique_ips,
            avg_duration,
            bytes_ratio,
            local_ratio,
            error_ratio
        ]

    def extract_suricata_features(self, logs: List[Dict[str, Any]], window_minutes: int = 5) -> List[float]:
        """Extract features from Suricata logs within a time window."""
        if not logs:
            return [0.0] * len(self.suricata_features)

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=window_minutes)
        window_logs = [log for log in logs if start_time <= log['timestamp'] <= end_time]

        if not window_logs:
            return [0.0] * len(self.suricata_features)

        # Calculate features
        severity_scores = [log.get('severity', 0) for log in window_logs if log.get('severity') is not None]
        avg_severity = np.mean(severity_scores) if severity_scores else 0

        unique_sigs = len(set(log.get('signature', '') for log in window_logs))
        event_freq = len(window_logs) / (window_minutes * 60)
        
        high_severity = sum(1 for score in severity_scores if score >= 3)
        high_sev_ratio = high_severity / len(window_logs) if window_logs else 0

        source_ips = [log['src_ip'] for log in window_logs]
        ip_diversity = len(set(source_ips)) / len(window_logs)

        protocols = [log['proto'] for log in window_logs]
        protocol_entropy = self._calculate_entropy(protocols)

        return [
            avg_severity,
            unique_sigs,
            event_freq,
            high_sev_ratio,
            ip_diversity,
            protocol_entropy
        ]

    def extract_osquery_features(self, logs: List[Dict[str, Any]], window_minutes: int = 5) -> List[float]:
        """Extract features from OSQuery logs within a time window."""
        if not logs:
            return [0.0] * len(self.osquery_features)

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=window_minutes)
        window_logs = [log for log in logs if start_time <= log['timestamp'] <= end_time]

        if not window_logs:
            return [0.0] * len(self.osquery_features)

        # Calculate frequencies for different event types
        event_counts = defaultdict(int)
        for log in window_logs:
            name = log['name'].lower()
            if 'process' in name:
                event_counts['process'] += 1
            elif 'file' in name:
                event_counts['file'] += 1
            elif 'network' in name:
                event_counts['network'] += 1
            elif 'user' in name:
                event_counts['user'] += 1
            else:
                event_counts['system'] += 1

        total_time = window_minutes * 60  # convert to seconds
        return [
            event_counts['process'] / total_time,
            event_counts['file'] / total_time,
            event_counts['network'] / total_time,
            event_counts['user'] / total_time,
            event_counts['system'] / total_time
        ]

    def extract_features(self, source: str, logs: List[Dict[str, Any]], window_minutes: int = 5) -> List[float]:
        """Extract features based on the log source."""
        extractors = {
            'zeek': self.extract_zeek_features,
            'suricata': self.extract_suricata_features,
            'osquery': self.extract_osquery_features
        }
        
        if source not in extractors:
            raise ValueError(f"Unsupported log source: {source}")
        
        return extractors[source](logs, window_minutes)