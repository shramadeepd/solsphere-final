import platform
import subprocess
import re
import json

def check_inactivity_settings():
    """Check sleep/inactivity settings to ensure they are ≤ 10 minutes."""
    try:
        system = platform.system()
        
        if system == "Windows":
            # Check Windows power settings
            try:
                # Get current power scheme
                result = subprocess.run(
                    ["powercfg", "/getactivescheme"], 
                    capture_output=True, 
                    text=True
                )
                if result.returncode == 0:
                    # Extract GUID from output
                    match = re.search(r'Power Scheme GUID: ([a-f0-9\-]+)', result.stdout)
                    if match:
                        guid = match.group(1)
                        
                        # Check monitor timeout
                        monitor_result = subprocess.run(
                            ["powercfg", "/q", guid, "7516b95f-f776-4464-8c53-06167f40cc99", "ad9a0e66-8e09-4356-97a3-eb511a9dfa9f"], 
                            capture_output=True, 
                            text=True
                        )
                        
                        # Check disk timeout
                        disk_result = subprocess.run(
                            ["powercfg", "/q", guid, "0012ee47-9041-4b5d-9b77-535fba8b1442", "0b2d69d7-a2a1-449c-9680-f91c70521c60"], 
                            capture_output=True, 
                            text=True
                        )
                        
                        # Check sleep timeout
                        sleep_result = subprocess.run(
                            ["powercfg", "/q", guid, "0012ee47-9041-4b5d-9b77-535fba8b1442", "29f6c1db-86da-48c5-9fdb-f2b67b1f44da"], 
                            capture_output=True, 
                            text=True
                        )
                        
                        # Parse timeouts (convert from seconds to minutes)
                        timeouts = {}
                        
                        if monitor_result.returncode == 0:
                            match = re.search(r'Current AC Power Setting Index: 0x([0-9a-f]+)', monitor_result.stdout)
                            if match:
                                hex_value = int(match.group(1), 16)
                                if hex_value != 0:  # 0 means never
                                    timeouts["monitor"] = hex_value // 60  # Convert seconds to minutes
                        
                        if disk_result.returncode == 0:
                            match = re.search(r'Current AC Power Setting Index: 0x([0-9a-f]+)', disk_result.stdout)
                            if match:
                                hex_value = int(match.group(1), 16)
                                if hex_value != 0:  # 0 means never
                                    timeouts["disk"] = hex_value // 60
                        
                        if sleep_result.returncode == 0:
                            match = re.search(r'Current AC Power Setting Index: 0x([0-9a-f]+)', sleep_result.stdout)
                            if match:
                                hex_value = int(match.group(1), 16)
                                if hex_value != 0:  # 0 means never
                                    timeouts["sleep"] = hex_value // 60
                        
                        # Check if any timeout is > 10 minutes
                        issues = []
                        for timeout_type, minutes in timeouts.items():
                            if minutes > 10:
                                issues.append(f"{timeout_type}: {minutes} minutes")
                        
                        if issues:
                            return {
                                "status": "non_compliant",
                                "details": {
                                    "timeouts": timeouts,
                                    "issues": issues,
                                    "warning": "Some timeouts exceed 10 minutes"
                                }
                            }
                        else:
                            return {
                                "status": "compliant",
                                "details": {
                                    "timeouts": timeouts,
                                    "message": "All timeouts are ≤ 10 minutes"
                                }
                            }
                
                return {"status": "unknown", "details": {"error": "Unable to determine power settings"}}
                
            except Exception as e:
                return {"status": "error", "details": {"error": f"Error checking power settings: {str(e)}"}}
                
        elif system == "Darwin":  # macOS
            try:
                # Check macOS sleep settings
                result = subprocess.run(
                    ["pmset", "-g"], 
                    capture_output=True, 
                    text=True
                )
                
                if result.returncode == 0:
                    timeouts = {}
                    issues = []
                    
                    # Parse pmset output
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if 'sleep' in line.lower():
                            match = re.search(r'sleep\s+(\d+)', line)
                            if match:
                                minutes = int(match.group(1))
                                timeouts["sleep"] = minutes
                                if minutes > 10:
                                    issues.append(f"sleep: {minutes} minutes")
                        
                        elif 'displaysleep' in line.lower():
                            match = re.search(r'displaysleep\s+(\d+)', line)
                            if match:
                                minutes = int(match.group(1))
                                timeouts["display_sleep"] = minutes
                                if minutes > 10:
                                    issues.append(f"display_sleep: {minutes} minutes")
                    
                    if issues:
                        return {
                            "status": "non_compliant",
                            "details": {
                                "timeouts": timeouts,
                                "issues": issues,
                                "warning": "Some timeouts exceed 10 minutes"
                            }
                        }
                    else:
                        return {
                            "status": "compliant",
                            "details": {
                                "timeouts": timeouts,
                                "message": "All timeouts are ≤ 10 minutes"
                            }
                        }
                
                return {"status": "unknown", "details": {"error": "Unable to determine sleep settings"}}
                
            except Exception as e:
                return {"status": "error", "details": {"error": f"Error checking sleep settings: {str(e)}"}}
                
        elif system == "Linux":
            try:
                # Check Linux power management settings
                timeouts = {}
                issues = []
                
                # Check systemd-logind settings
                try:
                    result = subprocess.run(
                        ["systemctl", "show", "systemd-logind"], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode == 0:
                        for line in result.stdout.strip().split('\n'):
                            if 'IdleAction=' in line:
                                match = re.search(r'IdleAction=(\w+)', line)
                                if match:
                                    action = match.group(1)
                                    if action == "suspend":
                                        timeouts["idle_action"] = "suspend"
                                    else:
                                        timeouts["idle_action"] = action
                            
                            elif 'IdleActionSec=' in line:
                                match = re.search(r'IdleActionSec=(\d+)', line)
                                if match:
                                    seconds = int(match.group(1))
                                    minutes = seconds // 60
                                    timeouts["idle_timeout"] = minutes
                                    if minutes > 10:
                                        issues.append(f"idle_timeout: {minutes} minutes")
                except:
                    pass
                
                # Check X11 screen saver settings
                try:
                    result = subprocess.run(
                        ["xset", "q"], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode == 0:
                        for line in result.stdout.strip().split('\n'):
                            if 'timeout:' in line:
                                match = re.search(r'timeout:\s+(\d+)', line)
                                if match:
                                    minutes = int(match.group(1))
                                    timeouts["screen_saver"] = minutes
                                    if minutes > 10:
                                        issues.append(f"screen_saver: {minutes} minutes")
                except:
                    pass
                
                if issues:
                    return {
                        "status": "non_compliant",
                        "details": {
                            "timeouts": timeouts,
                            "issues": issues,
                            "warning": "Some timeouts exceed 10 minutes"
                        }
                    }
                else:
                    return {
                        "status": "compliant",
                        "details": {
                            "timeouts": timeouts,
                            "message": "All timeouts are ≤ 10 minutes"
                        }
                    }
                
            except Exception as e:
                return {"status": "error", "details": {"error": f"Error checking sleep settings: {str(e)}"}}
        
        else:
            return {"status": "unknown", "details": {"error": f"Unsupported OS: {system}"}}
            
    except Exception as e:
        return {"status": "error", "details": {"error": str(e)}}
