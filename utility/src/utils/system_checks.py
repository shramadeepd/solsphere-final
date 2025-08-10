import platform
import subprocess
import os
import uuid
import socket
from datetime import datetime
from checks.disk_encryption import check_disk_encryption
from checks.os_update import check_os_updates
from checks.antivirus import check_antivirus
from checks.sleep_settings import check_inactivity_settings

def get_machine_id():
    """Generate or retrieve a unique machine identifier."""
    try:
        # Try to get existing machine ID from file
        id_file = os.path.join(os.path.dirname(__file__), '..', 'machine_id.txt')
        if os.path.exists(id_file):
            with open(id_file, 'r') as f:
                return f.read().strip()
        
        # Generate new machine ID
        machine_id = str(uuid.uuid4())
        
        # Save to file
        with open(id_file, 'w') as f:
            f.write(machine_id)
        
        return machine_id
    except Exception:
        # Fallback to hostname-based ID
        return f"machine-{socket.gethostname()}-{uuid.uuid4().hex[:8]}"

def get_system_info():
    """Get basic system information."""
    try:
        system = platform.system()
        release = platform.release()
        version = platform.version()
        machine = platform.machine()
        processor = platform.processor()
        hostname = socket.gethostname()
        
        return {
            "os_name": system,
            "os_version": f"{release} {version}",
            "architecture": machine,
            "processor": processor,
            "hostname": hostname
        }
    except Exception as e:
        return {
            "os_name": "unknown",
            "os_version": "unknown",
            "architecture": "unknown",
            "processor": "unknown",
            "hostname": "unknown",
            "error": str(e)
        }

def collect_system_info():
    """Collect all system checks and information."""
    try:
        # Get basic system info
        system_info = get_system_info()
        machine_id = get_machine_id()
        
        # Perform all checks
        disk_encryption_result = check_disk_encryption()
        os_updates_result = check_os_updates()
        antivirus_result = check_antivirus()
        inactivity_result = check_inactivity_settings()
        
        # Compile results
        checks = [
            {
                "name": "disk_encryption",
                "status": disk_encryption_result["status"],
                "details": disk_encryption_result["details"]
            },
            {
                "name": "os_updates",
                "status": os_updates_result["status"],
                "details": os_updates_result["details"]
            },
            {
                "name": "antivirus",
                "status": antivirus_result["status"],
                "details": antivirus_result["details"]
            },
            {
                "name": "inactivity_settings",
                "status": inactivity_result["status"],
                "details": inactivity_result["details"]
            }
        ]
        
        # Determine overall system health
        overall_status = "healthy"
        issues = []
        
        for check in checks:
            if check["status"] in ["error", "unknown"]:
                overall_status = "unknown"
            elif check["status"] in ["non_compliant", "unprotected", "outdated"]:
                overall_status = "unhealthy"
                if "warning" in check["details"]:
                    issues.append(f"{check['name']}: {check['details']['warning']}")
                elif "issues" in check["details"]:
                    issues.append(f"{check['name']}: {', '.join(check['details']['issues'])}")
        
        return {
            "machine_id": machine_id,
            "timestamp": datetime.utcnow().isoformat(),
            "system_info": system_info,
            "overall_status": overall_status,
            "issues": issues,
            "checks": checks
        }
        
    except Exception as e:
        return {
            "machine_id": get_machine_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "error": f"Failed to collect system info: {str(e)}",
            "overall_status": "error"
        }
