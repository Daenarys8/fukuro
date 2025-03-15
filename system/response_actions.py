import logging
from typing import Dict, Any, List
import aiohttp
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityResponder:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.alert_endpoints = self.config.get("alert_endpoints", [])
        self.firewall_api = self.config.get("firewall_api", "")
        self.quarantine_api = self.config.get("quarantine_api", "")

    async def quarantine_system(self, target: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Quarantine a compromised system."""
        try:
            logger.info(f"Quarantining system: {target}")
            
            if not self.quarantine_api:
                raise ValueError("Quarantine API endpoint not configured")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.quarantine_api,
                    json={
                        "target": target,
                        "parameters": parameters
                    }
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Quarantine failed: {await response.text()}")
                    
                    return {
                        "status": "success",
                        "action": "quarantine",
                        "target": target,
                        "details": await response.json()
                    }
        except Exception as e:
            logger.error(f"Error quarantining system: {str(e)}")
            raise

    async def send_alert(self, alert_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Send security alerts to configured endpoints."""
        try:
            logger.info("Sending security alerts")
            
            if not self.alert_endpoints:
                raise ValueError("No alert endpoints configured")
            
            results = []
            async with aiohttp.ClientSession() as session:
                for endpoint in self.alert_endpoints:
                    try:
                        async with session.post(endpoint, json=alert_data) as response:
                            results.append({
                                "endpoint": endpoint,
                                "status": "success" if response.status == 200 else "failed",
                                "details": await response.text()
                            })
                    except Exception as e:
                        results.append({
                            "endpoint": endpoint,
                            "status": "failed",
                            "error": str(e)
                        })
            
            return results
        except Exception as e:
            logger.error(f"Error sending alerts: {str(e)}")
            raise

    async def update_firewall(self, rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update firewall rules."""
        try:
            logger.info("Updating firewall rules")
            
            if not self.firewall_api:
                raise ValueError("Firewall API endpoint not configured")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.firewall_api,
                    json={"rules": rules}
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Firewall update failed: {await response.text()}")
                    
                    return {
                        "status": "success",
                        "action": "firewall_update",
                        "rules_applied": len(rules),
                        "details": await response.json()
                    }
        except Exception as e:
            logger.error(f"Error updating firewall: {str(e)}")
            raise

    async def execute_response(self, action_type: str, target: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a security response action."""
        try:
            if action_type == "quarantine":
                return await self.quarantine_system(target, parameters)
            elif action_type == "alert":
                return {"alerts": await self.send_alert(parameters)}
            elif action_type == "firewall":
                return await self.update_firewall(parameters.get("rules", []))
            else:
                raise ValueError(f"Unsupported action type: {action_type}")
        except Exception as e:
            logger.error(f"Error executing response action: {str(e)}")
            raise