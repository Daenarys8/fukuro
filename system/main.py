import os
import datetime
import logging
import traceback
from typing import Dict, Any, List, Optional
from sqlalchemy import create_engine, text
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Internal imports
from .database import get_db, init_db
from .routers import threat_management
from .models import (
    Threat, SecurityLog, AnomalyDetection,
    ResponseActionLog as DBResponseAction
)
from .schemas_consolidated import (
    NetworkStatsResponse, ThreatResponse, LogData,
    AnalysisRequest, AnomalyData, ResponseAction
)
from .config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API for system threat detection and management",
    version=settings.VERSION
)

# Register routers early
app.include_router(threat_management.router)

import os

# Configure CORS settings
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
allowed_origins = [
    frontend_url,
    "http://localhost:5173",  # Dev server
    "http://localhost:3000",  # Alt dev port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://localhost:8000",  # API server
    "http://127.0.0.1:8000"
]

# Add CORS middleware early in the chain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)

# Initialize database
logger.info("Initializing database...")
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Database initialization error: {str(e)}")
    logger.error("Will attempt to initialize during startup")

# Database configuration
DATABASE_RETRY_INTERVAL = 2  # seconds between retries
DATABASE_MAX_RETRIES = 3    # maximum number of retry attempts
DATABASE_TIMEOUT = 30       # database connection timeout in seconds
DATABASE_TABLES = [
    'threats',
    'security_logs',
    'anomaly_detections',
    'response_action_logs'
]

# Engine configuration
ENGINE_CONFIG = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "connect_args": {
        "connect_timeout": DATABASE_TIMEOUT
    }
}

def verify_database_connection():
    """Test database connection"""
    from sqlalchemy import create_engine, text
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, **ENGINE_CONFIG)
    try:
        with engine.connect() as conn:
            conn.execution_options(timeout=10)
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return False

# API Server Configuration
import socket

# Initialize the application
def initialize_database():
    """Initialize database and verify connection"""
    try:
        # Initialize database schema
        logger.info("Initializing database schema...")
        init_db()
        logger.info("Database schema initialized")

        # Test database connection
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, **ENGINE_CONFIG)
        try:
            with engine.connect() as conn:
                conn.execution_options(timeout=10)
                conn.execute(text("SELECT 1"))
                for table in DATABASE_TABLES:
                    try:
                        conn.execute(text(f"SELECT 1 FROM {table} LIMIT 1"))
                    except Exception as e:
                        logger.error(f"Error checking table {table}: {str(e)}")
                        raise
        except Exception as e:
            logger.error(f"Database verification failed: {str(e)}")
            raise
    #                 logger.warning(f"Table {table} not found - will be created on first use")
    #     logger.info("Database connection verified")
    #     return True
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        logger.error(traceback.format_exc())
        return False

# Initialize database on first load
try:
    initialize_database()
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    logger.info("Will retry database initialization during startup")

@app.on_event("startup")
def startup():
    """Initialize application and server"""
    try:
        logger.info("Starting server initialization...")
        import atexit
        atexit.register(lambda: logger.info("Server shutting down..."))

        # Clean migration state first
        logger.info("Cleaning database and migration state...")

        
        # Run migrations on clean state
        logger.info("Running database migrations...")
        from .apply_migrations import apply_migrations, reset_migration_state
        reset_migration_state()
        apply_migrations()

        # Log loaded routes
        logger.info("Checking routes are loaded correctly...")

        # Ensure data directory exists
        from pathlib import Path
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        data_dir.chmod(0o777)
        
        # Populate demo data if in development mode
        if os.getenv('ENVIRONMENT', 'development') == 'development':
            logger.info("Populating database with demo data...")
            from .generate_demo_data import populate_demo_data
            populate_demo_data()
            logger.info("Demo data population complete")
        
        # Log server configuration
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', '8000'))
        
        logger.info("Server configuration:")
        logger.info(f"  Host: {host}")
        logger.info(f"  Port: {port}")
        logger.info(f"  Environment: {os.getenv('ENVIRONMENT', 'development')}")
        logger.info(f"  Database: {os.getenv('SQLALCHEMY_DATABASE_URL', 'default')}")
        
        logger.info("\nAvailable endpoints:")
        logger.info("  - GET  /threats         - Get current threats")
        logger.info("  - POST /threats/resolve - Resolve a threat")
        logger.info("  - GET  /health         - System health check")
        logger.info("  - GET  /stats/network  - Network statistics")
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise RuntimeError("Failed to start server")

@app.on_event("shutdown")
def shutdown_event():
    """Cleanup when shutting down the API server"""
    logger.info("API server shutting down...")

# API endpoints

@app.get("/stats/network", response_model=NetworkStatsResponse)
def get_network_stats(db: Session = Depends(get_db)):
    """
    Get network statistics with fallback for database issues
    """
    try:
        try:
            total_logs = db.query(SecurityLog).count()
            recent_anomalies = db.query(AnomalyDetection).filter(
                AnomalyDetection.timestamp >= datetime.datetime.utcnow() - datetime.timedelta(hours=24)
            ).count()
        except Exception as db_error:
            logger.warning(f"Database query failed: {str(db_error)}")
            return {
                "total_connections": 0,
                "unique_ips": 0,
                "last_hour_connections": 0,
                "timestamp": datetime.datetime.utcnow(),
                "status": "degraded",
                "message": "Database currently unavailable"
            }

        return {
            "total_connections": total_logs,
            "unique_ips": 0,
            "last_hour_connections": recent_anomalies,
            "timestamp": datetime.datetime.utcnow(),
            "status": "healthy"
        }
    except Exception as e:
        logger.error(f"Error in network stats endpoint: {str(e)}")
        return {
            "status": "error",
            "message": "Internal server error",
            "timestamp": datetime.datetime.utcnow()
        }

@app.post("/ingest")
def ingest_log(log_data: LogData, db: Session = Depends(get_db)):
    """
    Ingest a log entry into the system
    """
    try:
        log_entry = SecurityLog(
            timestamp=log_data.timestamp,
            source=log_data.source,
            event_type=log_data.event_type,
            raw_data=str(log_data.data)
        )
        db.add(log_entry)
        db.commit()
        
        return {"status": "success", "message": "Log ingested successfully"}
    except Exception as e:
        logger.error(f"Error ingesting log: {str(e)}")
        raise HTTPException(status_code=500, detail="Error ingesting log")

@app.post("/analyze")
def analyze_log(analysis_request: AnalysisRequest):
    """
    Analyze log data with specified analysis type
    """
    try:
        # Add log analysis logic here
        return {"status": "success", "results": f"Analysis of type {analysis_request.analysis_type} completed"}
    except Exception as e:
        logger.error(f"Error in log analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing log")

@app.post("/detect")
def detect_anomaly(anomaly_data: AnomalyData, db: Session = Depends(get_db)):
    """
    Process potential anomaly detection
    """
    try:
        anomaly = AnomalyDetection(
            timestamp=anomaly_data.timestamp,
            source=anomaly_data.source,
            metrics=str(anomaly_data.metrics),
            alert_level=anomaly_data.alert_level
        )
        db.add(anomaly)
        db.commit()
        
        return {"status": "success", "alert_level": anomaly_data.alert_level}
    except Exception as e:
        logger.error(f"Error in anomaly detection: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing anomaly")

@app.post("/respond")
def trigger_response(response: ResponseAction, db: Session = Depends(get_db)):
    """
    Trigger a response action
    """
    try:
        action_log = DBResponseAction(
            action_type=response.action_type,
            target=response.target,
            parameters=str(response.parameters) if response.parameters else None,
            timestamp=datetime.datetime.utcnow()
        )
        db.add(action_log)
        db.commit()
        
        return {"status": "success", "action": "Response action triggered"}
    except Exception as e:
        logger.error(f"Error triggering response: {str(e)}")
        raise HTTPException(status_code=500, detail="Error triggering response")

@app.get("/")
def root():
    """
    Root endpoint
    """
    return {"status": "online", "system": "Security Monitoring System"}

@app.get("/health")
def system_health():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow(),
        "version": settings.VERSION,
        "system_metrics": {
            "cpu_usage": 0.0,  # Placeholder for actual metrics
            "memory_usage": 0.0,
            "disk_usage": 0.0
        }
    }

# Removed duplicate /stats/network endpoint

@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    """
    Get recent security logs
    """
    try:
        logs = db.query(SecurityLog).order_by(SecurityLog.timestamp.desc()).limit(100).all()
        return {"logs": logs}
    except Exception as e:
        logger.error(f"Error fetching logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving logs")

# Removed duplicate /threats endpoint - now handled by threat_management router


# Include routers
# Ensure routers are registered before the first request
from .routers import threat_management
app.include_router(threat_management.router, prefix="")