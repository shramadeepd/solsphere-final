import platform
import subprocess
import os
import re

def check_disk_encryption():
    """Check if disk encryption is enabled on the system."""
    try:
        system = platform.system()
        
        if system == "Windows":
            # Check BitLocker status
            result = subprocess.run(
                ["manage-bde", "-status", "C:"], 
                capture_output=True, 
                text=True, 
                shell=True
            )
            if result.returncode == 0:
                # Look for encryption percentage
                if "Percentage Encrypted" in result.stdout:
                    match = re.search(r"Percentage Encrypted:\s*(\d+)%", result.stdout)
                    if match:
                        percentage = int(match.group(1))
                        return {
                            "status": "encrypted" if percentage > 0 else "not_encrypted",
                            "details": {"encryption_type": "BitLocker", "percentage": percentage}
                        }
                return {"status": "not_encrypted", "details": {"encryption_type": "BitLocker"}}
            else:
                return {"status": "unknown", "details": {"error": "Unable to check BitLocker status"}}
                
        elif system == "Darwin":  # macOS
            # Check FileVault status
            result = subprocess.run(
                ["fdesetup", "status"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                if "FileVault is On" in result.stdout:
                    return {"status": "encrypted", "details": {"encryption_type": "FileVault"}}
                else:
                    return {"status": "not_encrypted", "details": {"encryption_type": "FileVault"}}
            else:
                return {"status": "unknown", "details": {"error": "Unable to check FileVault status"}}
                
        elif system == "Linux":
            # Check for LUKS/dm-crypt
            result = subprocess.run(
                ["lsblk", "-o", "NAME,TYPE,FSTYPE,MOUNTPOINT"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                # Look for crypt devices
                lines = result.stdout.strip().split('\n')
                encrypted_devices = []
                for line in lines[1:]:  # Skip header
                    if 'crypt' in line or 'LUKS' in line:
                        encrypted_devices.append(line.strip())
                
                if encrypted_devices:
                    return {
                        "status": "encrypted", 
                        "details": {
                            "encryption_type": "LUKS/dm-crypt",
                            "devices": encrypted_devices
                        }
                    }
                else:
                    return {"status": "not_encrypted", "details": {"encryption_type": "LUKS/dm-crypt"}}
            else:
                return {"status": "unknown", "details": {"error": "Unable to check disk status"}}
        
        else:
            return {"status": "unknown", "details": {"error": f"Unsupported OS: {system}"}}
            
    except Exception as e:
        return {"status": "error", "details": {"error": str(e)}}
