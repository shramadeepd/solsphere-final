import platform
import subprocess
import re
import json
from datetime import datetime

def check_os_updates():
    """Check if the operating system is up to date."""
    try:
        system = platform.system()
        
        if system == "Windows":
            # Check Windows Update status
            result = subprocess.run(
                ["wmic", "qfe", "list", "brief", "/format:csv"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:  # Has header + at least one update
                    # Get the latest update date
                    latest_update = None
                    for line in lines[1:]:
                        if line.strip():
                            parts = line.split(',')
                            if len(parts) >= 3:
                                try:
                                    date_str = parts[3].strip()
                                    if date_str:
                                        update_date = datetime.strptime(date_str, '%Y%m%d')
                                        if latest_update is None or update_date > latest_update:
                                            latest_update = update_date
                                except:
                                    continue
                    
                    if latest_update:
                        days_since_update = (datetime.now() - latest_update).days
                        if days_since_update <= 30:
                            return {
                                "status": "up_to_date",
                                "details": {
                                    "last_update": latest_update.strftime('%Y-%m-%d'),
                                    "days_since_update": days_since_update
                                }
                            }
                        else:
                            return {
                                "status": "outdated",
                                "details": {
                                    "last_update": latest_update.strftime('%Y-%m-%d'),
                                    "days_since_update": days_since_update,
                                    "warning": "System may need updates"
                                }
                            }
                
                return {"status": "unknown", "details": {"error": "Unable to determine update status"}}
            else:
                return {"status": "unknown", "details": {"error": "Unable to check Windows updates"}}
                
        elif system == "Darwin":  # macOS
            # Check macOS software updates
            result = subprocess.run(
                ["softwareupdate", "-l"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                if "No updates available" in result.stdout:
                    return {"status": "up_to_date", "details": {"message": "No updates available"}}
                else:
                    # Parse available updates
                    updates = []
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if line.strip() and not line.startswith('Software Update Tool'):
                            updates.append(line.strip())
                    
                    if updates:
                        return {
                            "status": "updates_available",
                            "details": {
                                "available_updates": updates,
                                "count": len(updates)
                            }
                        }
                    else:
                        return {"status": "up_to_date", "details": {"message": "No updates available"}}
            else:
                return {"status": "unknown", "details": {"error": "Unable to check macOS updates"}}
                
        elif system == "Linux":
            # Check for available package updates
            updates = []
            
            # Try apt (Debian/Ubuntu)
            try:
                result = subprocess.run(
                    ["apt", "list", "--upgradable"], 
                    capture_output=True, 
                    text=True
                )
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:  # Has updates
                        for line in lines[1:]:
                            if line.strip():
                                updates.append(line.strip())
            except:
                pass
            
            # Try yum (RHEL/CentOS)
            if not updates:
                try:
                    result = subprocess.run(
                        ["yum", "check-update", "--quiet"], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode == 100:  # 100 means updates available
                        lines = result.stdout.strip().split('\n')
                        for line in lines:
                            if line.strip():
                                updates.append(line.strip())
                except:
                    pass
            
            # Try pacman (Arch)
            if not updates:
                try:
                    result = subprocess.run(
                        ["pacman", "-Qu"], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        lines = result.stdout.strip().split('\n')
                        for line in lines:
                            if line.strip():
                                updates.append(line.strip())
                except:
                    pass
            
            if not updates:
                return {"status": "up_to_date", "details": {"message": "No updates available"}}
            else:
                return {
                    "status": "updates_available",
                    "details": {
                        "available_updates": updates[:10],  # Limit to first 10
                        "count": len(updates)
                    }
                }
        
        else:
            return {"status": "unknown", "details": {"error": f"Unsupported OS: {system}"}}
            
    except Exception as e:
        return {"status": "error", "details": {"error": str(e)}}
