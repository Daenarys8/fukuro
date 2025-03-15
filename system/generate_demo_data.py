import random
import datetime
import json  # Ensure JSON serialization
from typing import List
from uuid import uuid4
from sqlalchemy.orm import Session

from .database import init_db, get_db
from .models import SecurityLog, AnomalyDetection, ResponseActionLog, Threat, ThreatSeverity, ThreatStatus

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_random_timestamp(days_back: int = 30):
    now = datetime.datetime.now()
    random_days = random.randint(0, days_back)
    random_seconds = random.randint(0, 86400)
    return now - datetime.timedelta(days=random_days, seconds=random_seconds)

def generate_security_logs(db: Session, count: int = 100) -> List[SecurityLog]:
    logs = []
    event_types = ["login_attempt", "file_access", "network_connection", "system_change", "policy_violation"]
    
    for _ in range(count):
        log = SecurityLog(
            timestamp=generate_random_timestamp(),
            source=generate_random_ip(),
            event_type=random.choice(event_types),
            raw_data=json.dumps({"details": "Sample raw data"})  # Serialize dict to JSON string
        )
        db.add(log)
        logs.append(log)
    
    return logs

def generate_threats(db: Session, count: int = 20) -> List[Threat]:
    threats = []
    threat_types = ["malware", "intrusion_attempt", "data_breach", "suspicious_activity", "policy_violation"]
    
    for _ in range(count):
        severity = random.choice(list(ThreatSeverity))
        status = random.choice(list(ThreatStatus))
        
        threat = Threat(
            id=str(uuid4()),
            threat_type=random.choice(threat_types),
            title=f"{random.choice(threat_types).replace('_', ' ').title()} Threat",
            severity=severity,
            status=status,
            source_ip=generate_random_ip(),
            timestamp=generate_random_timestamp(),
            description=f"Detected {severity} severity threat from {generate_random_ip()}"
        )
        db.add(threat)
        threats.append(threat)
    
    return threats

def generate_anomalies(db: Session, threats: List[Threat], count: int = 40) -> List[AnomalyDetection]:
    anomalies = []
    
    for _ in range(count):
        threat = random.choice(threats) if threats else None
        
        anomaly = AnomalyDetection(
            timestamp=generate_random_timestamp(),
            source_ip=generate_random_ip(),
            severity=random.randint(1, 10),
            description="Unusual network behavior detected",
            anomaly_score=str(random.uniform(0.7, 1.0)),
            features=json.dumps({"network_stats": {"bytes": random.randint(1000, 100000), "packets": random.randint(10, 1000)}}),  # Serialize dict
            is_anomaly=1,
            threat_id=threat.id if threat else None
        )
        db.add(anomaly)
        anomalies.append(anomaly)
    
    return anomalies

def generate_response_actions(db: Session, threats: List[Threat], count: int = 30) -> List[ResponseActionLog]:
    actions = []
    action_types = ["block_ip", "alert_admin", "isolate_system", "update_firewall", "incident_report"]
    
    for _ in range(count):
        threat = random.choice(threats) if threats else None
        
        action = ResponseActionLog(
            timestamp=generate_random_timestamp(),
            action_type=random.choice(action_types),
            parameters=json.dumps({"action_result": "successfully executed"}),  # Serialize dict
            anomaly_id=None
        )
        db.add(action)
        actions.append(action)
    
    return actions

def populate_demo_data():
    """Main function to populate the database with demo data"""
    init_db()
    db = next(get_db())
    
    try:
        # Generate and commit threats first since other tables reference them
        threats = generate_threats(db)
        db.commit()
        
        # Generate dependent data
        security_logs = generate_security_logs(db)
        anomalies = generate_anomalies(db, threats)
        response_actions = generate_response_actions(db, threats)
        
        # Commit remaining changes
        db.commit()
        
        print(f"""Demo data generated successfully:
        - {len(security_logs)} security logs
        - {len(threats)} threats
        - {len(anomalies)} anomalies
        - {len(response_actions)} response actions""")
        
    except Exception as e:
        db.rollback()
        print(f"Error generating demo data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_demo_data()
