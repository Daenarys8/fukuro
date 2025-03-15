from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, JSON
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base  # Import Base from your database setup file
from enum import Enum

# Enum for threat severity
class ThreatSeverity(Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"

# Enum for threat status
class ThreatStatus(Enum):
    active = "active"
    resolved = "resolved"
    false_positive = "false_positive"
    under_investigation = "under_investigation"

# Constants for threat severity values
THREAT_SEVERITY_CRITICAL = "critical"
THREAT_SEVERITY_HIGH = "high"
THREAT_SEVERITY_MEDIUM = "medium"
THREAT_SEVERITY_LOW = "low"

# Constants for threat status values
THREAT_STATUS_ACTIVE = "active"
THREAT_STATUS_RESOLVED = "resolved"
THREAT_STATUS_FALSE_POSITIVE = "false_positive"
THREAT_STATUS_UNDER_INVESTIGATION = "under_investigation"

class SecurityLog(Base):
    __tablename__ = "security_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    log_type = Column(String, nullable=False)
    source = Column(String)
    message = Column(Text, nullable=False)
    additional_info = Column(JSON)  # Renamed 'metadata' to 'additional_info'
    threat_id = Column(String, ForeignKey('threats.id', ondelete='CASCADE'))
    threat = relationship("Threat", back_populates="logs")

class AnomalyDetection(Base):
    __tablename__ = "anomaly_detections"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    detection_type = Column(String, nullable=False)
    confidence_score = Column(Integer)
    description = Column(Text)
    source_data = Column(JSON)
    impact_severity = Column(String)
    affected_systems = Column(JSON)
    false_positive = Column(Integer, default=0)
    additional_info = Column(JSON)  # Renamed 'metadata' to 'additional_info'

class ResponseActionLog(Base):
    __tablename__ = "response_action_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    action_type = Column(String, nullable=False)
    target_system = Column(String)
    action_details = Column(JSON)
    success = Column(Integer, default=1)
    error_message = Column(Text)
    additional_info = Column(JSON)  # Renamed 'metadata' to 'additional_info'

class Threat(Base):
    __tablename__ = "threats"

    id = Column(String, primary_key=True)
    threat_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    severity = Column(String, nullable=False, default=THREAT_SEVERITY_LOW)
    status = Column(String, nullable=False, default=THREAT_STATUS_ACTIVE)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String)
    target_system = Column(String)
    
    # Relationships
    logs = relationship(
        "SecurityLog",
        back_populates="threat",
        lazy="select",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Threat(id={self.id}, type={self.threat_type}, severity={self.severity})>"
