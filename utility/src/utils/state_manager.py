import json
import os
from typing import Dict, Any, Optional
from .config import STATE_FILE
from .logger import logger

def save_state(data: Dict[str, Any]) -> bool:
    """
    Save the current system state to a file.
    
    Args:
        data: Dictionary containing system health data
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        state_file_path = os.path.join(script_dir, '..', STATE_FILE)
        
        # Create a simplified state for comparison (exclude timestamp and other volatile data)
        state_to_save = {
            "machine_id": data.get("machine_id"),
            "overall_status": data.get("overall_status"),
            "checks": []
        }
        
        # Save only the essential check information
        for check in data.get("checks", []):
            state_to_save["checks"].append({
                "name": check.get("name"),
                "status": check.get("status")
            })
        
        with open(state_file_path, 'w') as f:
            json.dump(state_to_save, f, indent=2)
        
        logger.logger.debug(f"State saved to {state_file_path}")
        return True
        
    except Exception as e:
        logger.logger.error(f"Failed to save state: {str(e)}")
        return False

def load_last_state() -> Optional[Dict[str, Any]]:
    """
    Load the last saved system state from file.
    
    Returns:
        Optional[Dict]: The last state or None if not found/error
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        state_file_path = os.path.join(script_dir, '..', STATE_FILE)
        
        if not os.path.exists(state_file_path):
            logger.logger.debug("No previous state file found")
            return None
        
        with open(state_file_path, 'r') as f:
            state = json.load(f)
        
        logger.logger.debug(f"State loaded from {state_file_path}")
        return state
        
    except Exception as e:
        logger.logger.error(f"Failed to load state: {str(e)}")
        return None

def has_state_changed(current_state: Dict[str, Any], last_state: Optional[Dict[str, Any]]) -> bool:
    """
    Compare current state with last state to determine if there are meaningful changes.
    
    Args:
        current_state: Current system state
        last_state: Previous system state
        
    Returns:
        bool: True if state has changed, False otherwise
    """
    if last_state is None:
        logger.logger.debug("No previous state to compare with")
        return True
    
    try:
        # Compare overall status
        if current_state.get("overall_status") != last_state.get("overall_status"):
            logger.logger.debug("Overall status changed")
            return True
        
        # Compare individual checks
        current_checks = {check["name"]: check["status"] for check in current_state.get("checks", [])}
        last_checks = {check["name"]: check["status"] for check in last_state.get("checks", [])}
        
        # Check if any check statuses have changed
        for check_name, current_status in current_checks.items():
            if check_name not in last_checks:
                logger.logger.debug(f"New check found: {check_name}")
                return True
            if last_checks[check_name] != current_status:
                logger.logger.debug(f"Check status changed for {check_name}: {last_checks[check_name]} -> {current_status}")
                return True
        
        # Check if any checks were removed
        for check_name in last_checks:
            if check_name not in current_checks:
                logger.logger.debug(f"Check removed: {check_name}")
                return True
        
        logger.logger.debug("No meaningful changes detected")
        return False
        
    except Exception as e:
        logger.logger.error(f"Error comparing states: {str(e)}")
        # If we can't compare, assume there's a change to be safe
        return True
