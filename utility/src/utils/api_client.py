import requests
import json
import time
from typing import Dict, Any
from .config import API_BASE_URL, API_ENDPOINT, API_TIMEOUT, MAX_RETRIES, RETRY_DELAY
from .logger import logger

def send_report(data: Dict[str, Any]) -> bool:
    """
    Send system health report to the backend API.
    
    Args:
        data: Dictionary containing system health data
        
    Returns:
        bool: True if successful, False otherwise
    """
    url = f"{API_BASE_URL}{API_ENDPOINT}"
    
    # Prepare the payload according to the backend schema
    payload = {
        "machine_id": data.get("machine_id"),
        "hostname": data.get("system_info", {}).get("hostname"),
        "os_name": data.get("system_info", {}).get("os_name"),
        "os_version": data.get("system_info", {}).get("os_version"),
        "metadata": {
            "architecture": data.get("system_info", {}).get("architecture"),
            "processor": data.get("system_info", {}).get("processor"),
            "overall_status": data.get("overall_status"),
            "issues": data.get("issues", [])
        },
        "checks": []
    }
    
    # Convert checks to the expected format
    for check in data.get("checks", []):
        payload["checks"].append({
            "name": check.get("name"),
            "status": check.get("status"),
            "details": check.get("details")
        })
    
    # Add timestamp if not present
    if "timestamp" not in payload["metadata"]:
        payload["metadata"]["timestamp"] = data.get("timestamp")
    
    logger.logger.info(f"Sending report to {url}")
    logger.logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=API_TIMEOUT,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                logger.logger.info(f"Report sent successfully (attempt {attempt + 1})")
                logger.logger.debug(f"Response: {response.text}")
                return True
            else:
                logger.logger.warning(
                    f"API request failed with status {response.status_code} (attempt {attempt + 1})"
                )
                logger.logger.debug(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            logger.logger.error(f"Request failed (attempt {attempt + 1}): {str(e)}")
        
        # Wait before retry (except on last attempt)
        if attempt < MAX_RETRIES - 1:
            logger.logger.info(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
    
    logger.logger.error(f"Failed to send report after {MAX_RETRIES} attempts")
    return False

def test_connection() -> bool:
    """
    Test the connection to the backend API.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    url = f"{API_BASE_URL}/"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logger.logger.info("Backend connection test successful")
            return True
        else:
            logger.logger.warning(f"Backend connection test failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.logger.error(f"Backend connection test failed: {str(e)}")
        return False
