from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# Models from schemas.py
class ThreatResolutionRequest(BaseModel):
    threat_id: str
    resolution_notes: Optional[str] = None

class ThreatResponse(BaseModel):
    id: str
    threat_type: str
    title: str
    description: Optional[str] = None
    severity: str  # Will be serialized from enum
    status: str  # Will be serialized from enum
    timestamp: Optional[datetime] = None
    source_ip: Optional[str] = None
    target_system: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class ThreatListResponse(BaseModel):
    threats: List[ThreatResponse]
    threat_level: str
    anomaly_count: int

class NetworkStatsResponse(BaseModel):
    total_connections: int
    unique_ips: int
    last_hour_connections: int

# Models from main.py
class LogData(BaseModel):
    timestamp: datetime
    source: str
    event_type: str
    data: Dict[str, Any]

class AnalysisRequest(BaseModel):
    data: Dict[str, Any]
    analysis_type: str

class AnomalyData(BaseModel):
    timestamp: datetime
    source: str
    metrics: Dict[str, Any]
    alert_level: Optional[str] = "low"

class ResponseAction(BaseModel):
    action_type: str
    target: str
    parameters: Optional[Dict[str, Any]] = None  # Added based on usage in main.py

# Models from models.py
class AnomalyResult(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    raw_score: float
    timestamp: datetime
    source: str
    features: List[float]
    feature_names: List[str]
    window_minutes: int
    logs_analyzed: int
    metadata: Optional[Dict[str, Any]] = None

class ModelMetrics(BaseModel):
    threshold: float
    contamination: float
    n_estimators: int
    feature_importances: Optional[Dict[str, float]] = None
    last_training_date: Optional[datetime] = None
    total_samples_trained: Optional[int] = None