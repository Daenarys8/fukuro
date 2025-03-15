from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from ..database import get_db
from ..models import AnomalyDetection, Threat, ThreatStatus, ThreatSeverity
from sqlalchemy.orm import Session
import datetime
import logging
import traceback
from ..schemas_consolidated import ThreatResponse, ThreatListResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/threats", tags=["threats"])

@router.get("", response_model=ThreatListResponse)
async def get_threats(db: Session = Depends(get_db)):
    """Get current threat information, including active threats with full details."""
    logger.debug("Processing get_threats request")
    try:
        # Get recent anomalies for threat level calculation
        recent_anomalies = db.query(AnomalyDetection).filter(
            AnomalyDetection.timestamp >= datetime.datetime.utcnow() - datetime.timedelta(hours=24)
        ).all() or []

        # Calculate threat level
        threat_level = "low"
        if len(recent_anomalies) > 10:
            threat_level = "high"
        elif len(recent_anomalies) > 5:
            threat_level = "medium"
        
        try:
            # Get active threats only
            # Query active threats by string value
            threats = db.query(Threat).filter(Threat.status == 'active').all() or []
            logger.debug(f"Found {len(threats)} active threats")
        except Exception as e:
            logger.error(f"Error querying threats: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )
        
        # Convert threats to response format
        threat_responses = []
        for threat in threats:
            try:
                # Ensure required fields are present and properly formatted
                if not threat.id or not threat.threat_type or not threat.title:
                    logger.error(f"Missing required field for threat {threat.id}")
                    continue

                # Safe enum conversion
                try:
                    # Convert string values to enums for validation, then back to strings
                    severity = ThreatSeverity(threat.severity) if threat.severity else ThreatSeverity.low
                    status = ThreatStatus(threat.status) if threat.status else ThreatStatus.active
                    
                    threat_data = {
                        "id": str(threat.id),
                        "threat_type": str(threat.threat_type),
                        "title": str(threat.title),
                        "description": str(threat.description) if threat.description else None,
                        "severity": severity.value,
                        "status": status.value,
                        "timestamp": threat.timestamp,
                        "source_ip": str(threat.source_ip) if threat.source_ip else None,
                        "target_system": str(threat.target_system) if threat.target_system else None
                    }
                except ValueError as ve:
                    logger.error(f"Invalid enum value for threat {threat.id}: {ve}")
                    continue
                logger.debug(f"Converting threat data: {threat_data}")
                response = ThreatResponse(**threat_data)
                threat_responses.append(response)
            except Exception as e:
                logger.error(f"Error converting threat {threat.id}: {str(e)}")
                logger.error(f"Threat data that failed: {vars(threat)}")
                logger.error(traceback.format_exc())
                continue
        
        response_data = ThreatListResponse(
            threats=threat_responses,
            threat_level=threat_level,
            anomaly_count=len(recent_anomalies)
        )
        
        return response_data

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error retrieving threat information: {error_msg}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        
        logger.error(f"Raw database error: {error_msg}")
        if "no such column" in error_msg.lower():
            # Database schema mismatch
            detail = "Database schema is out of date. Please run migrations."
        elif "operational error" in error_msg.lower():
            # Database connection issues
            detail = "Database connection error. Please try again later."
        else:
            detail = "Internal server error while retrieving threats."
            
        raise HTTPException(
            status_code=500,
            detail=detail
        )

@router.post("/{threat_id}/resolve")
async def resolve_threat(threat_id: str, db: Session = Depends(get_db)):
    """Resolve a threat by its ID."""
    try:
        threat = db.query(Threat).filter(Threat.id == threat_id).first()
        if not threat:
            raise HTTPException(status_code=404, detail="Threat not found")
            
        threat.status = ThreatStatus.resolved.value
        db.commit()
        return {"status": "success", "message": f"Threat {threat_id} resolved"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resolving threat {threat_id}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))