from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from dateutil.parser import isoparse

class ZeekLog(BaseModel):
    timestamp: datetime
    uid: str
    source_ip: str
    source_port: int
    dest_ip: str
    dest_port: int
    protocol: str
    service: Optional[str]
    duration: Optional[float]
    orig_bytes: Optional[int]
    resp_bytes: Optional[int]
    conn_state: Optional[str]
    local_orig: Optional[bool]
    local_resp: Optional[bool]
    missed_bytes: Optional[int]
    history: Optional[str]
    orig_pkts: Optional[int]
    orig_ip_bytes: Optional[int]
    resp_pkts: Optional[int]
    resp_ip_bytes: Optional[int]

class SuricataLog(BaseModel):
    timestamp: datetime
    event_type: str
    src_ip: str
    src_port: Optional[int] = 0
    dest_ip: str
    dest_port: Optional[int] = 0
    proto: str
    alert: Optional[Dict[str, Any]] = None 
    flow_id: Optional[int] = None
    in_iface: Optional[str] = None
    event_category: Optional[str] = None
    severity: Optional[int] = None 
    signature: Optional[str] = None
    signature_id: Optional[int] = None
    flow: Optional[Dict[str, Any]] = None
    tcp: Optional[Dict[str, Any]] = None
    app_proto: Optional[str] = None

class OSQueryLog(BaseModel):
    timestamp: datetime
    name: str
    action: str
    columns: Dict[str, Any]
    counter: Optional[int]
    decorations: Optional[Dict[str, Any]]
    hostIdentifier: str
    calendarTime: str
    unixTime: int

class LogParser:
    @staticmethod
    def parse_zeek(content: Dict[str, Any]) -> ZeekLog:
        """Parse and validate Zeek log content."""
        try:
            # Convert Unix timestamp to datetime if needed
            if isinstance(content.get('timestamp'), (int, float)):
                content['timestamp'] = datetime.fromtimestamp(content['timestamp'])
            return ZeekLog(**content)
        except Exception as e:
            raise ValueError(f"Invalid Zeek log format: {str(e)}")

    @staticmethod
    def parse_suricata(content: Dict[str, Any]) -> SuricataLog:
        """Parse and validate Suricata log content."""
        try:
            # Convert timestamp string to datetime if needed
            if isinstance(content.get('timestamp'), str):
                try:
                    content['timestamp'] = isoparse(content['timestamp'])  # Use isoparse for better timezone handling
                except ValueError as e:
                    raise ValueError(f"Invalid timestamp format: {str(e)}")
            
            # Handle flow timestamps if present
            if 'flow' in content and isinstance(content['flow'], dict):
                flow = content['flow']
                for time_field in ['start', 'end']:
                    if time_field in flow and isinstance(flow[time_field], str):
                        flow[time_field] = isoparse(flow[time_field])

            return SuricataLog(**content)
        except Exception as e:
            raise ValueError(f"Invalid Suricata log format: {str(e)}")

    @staticmethod
    def parse_osquery(content: Dict[str, Any]) -> OSQueryLog:
        """Parse and validate OSQuery log content."""
        try:
            # Convert calendarTime to timestamp
            if 'calendarTime' in content:
                content['timestamp'] = isoparse(content['calendarTime'])  # Use isoparse for better format handling
            return OSQueryLog(**content)
        except Exception as e:
            raise ValueError(f"Invalid OSQuery log format: {str(e)}")

    @classmethod
    def parse_log(cls, source: str, content: Dict[str, Any]) -> BaseModel:
        """Parse logs based on their source."""
        parsers = {
            'zeek': cls.parse_zeek,
            'suricata': cls.parse_suricata,
            'osquery': cls.parse_osquery
        }
        
        if source not in parsers:
            raise ValueError(f"Unsupported log source: {source}")
        
        return parsers[source](content)
