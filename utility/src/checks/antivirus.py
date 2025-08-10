import platform
import subprocess
import os
import re

def check_antivirus():
    """Check antivirus presence and status on the system."""
    try:
        system = platform.system()
        
        if system == "Windows":
            antivirus_list = []
            
            # Check Windows Defender
            try:
                result = subprocess.run(
                    ["sc", "query", "WinDefend"], 
                    capture_output=True, 
                    text=True
                )
                if result.returncode == 0 and "RUNNING" in result.stdout:
                    antivirus_list.append({
                        "name": "Windows Defender",
                        "status": "running",
                        "type": "built-in"
                    })
                elif result.returncode == 0:
                    antivirus_list.append({
                        "name": "Windows Defender",
                        "status": "stopped",
                        "type": "built-in"
                    })
            except:
                pass
            
            # Check for other common antivirus software
            common_av = [
                ("McAfee", "mcafee"),
                ("Norton", "norton"),
                ("Kaspersky", "kaspersky"),
                ("Avast", "avast"),
                ("AVG", "avg"),
                ("Bitdefender", "bitdefender"),
                ("Malwarebytes", "malwarebytes")
            ]
            
            for av_name, process_name in common_av:
                try:
                    result = subprocess.run(
                        ["tasklist", "/FI", f"IMAGENAME eq {process_name}*"], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode == 0 and process_name in result.stdout.lower():
                        antivirus_list.append({
                            "name": av_name,
                            "status": "running",
                            "type": "third_party"
                        })
                except:
                    pass
            
            if antivirus_list:
                return {
                    "status": "protected",
                    "details": {
                        "antivirus_software": antivirus_list,
                        "count": len(antivirus_list)
                    }
                }
            else:
                return {
                    "status": "unprotected",
                    "details": {"warning": "No antivirus software detected"}
                }
                
        elif system == "Darwin":  # macOS
            antivirus_list = []
            
            # macOS has built-in XProtect
            antivirus_list.append({
                "name": "XProtect",
                "status": "enabled",
                "type": "built-in"
            })
            
            # Check for common macOS antivirus software
            common_av = [
                ("Malwarebytes", "Malwarebytes"),
                ("Avast", "Avast"),
                ("AVG", "AVG"),
                ("Bitdefender", "Bitdefender"),
                ("Sophos", "Sophos")
            ]
            
            for av_name, app_name in common_av:
                try:
                    result = subprocess.run(
                        ["pgrep", "-f", app_name], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        antivirus_list.append({
                            "name": av_name,
                            "status": "running",
                            "type": "third_party"
                        })
                except:
                    pass
            
            return {
                "status": "protected",
                "details": {
                    "antivirus_software": antivirus_list,
                    "count": len(antivirus_list)
                }
            }
                
        elif system == "Linux":
            antivirus_list = []
            
            # Check for common Linux antivirus software
            common_av = [
                ("ClamAV", "clamscan"),
                ("Sophos", "sav"),
                ("Comodo", "comodo"),
                ("F-Prot", "f-prot"),
                ("Avast", "avast")
            ]
            
            for av_name, command in common_av:
                try:
                    result = subprocess.run(
                        ["which", command], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        # Check if it's running
                        try:
                            running_check = subprocess.run(
                                ["pgrep", "-f", command], 
                                capture_output=True, 
                                text=True
                            )
                            status = "running" if running_check.returncode == 0 else "installed"
                        except:
                            status = "installed"
                        
                        antivirus_list.append({
                            "name": av_name,
                            "status": status,
                            "type": "third_party"
                        })
                except:
                    pass
            
            if antivirus_list:
                return {
                    "status": "protected",
                    "details": {
                        "antivirus_software": antivirus_list,
                        "count": len(antivirus_list)
                    }
                }
            else:
                return {
                    "status": "unprotected",
                    "details": {"warning": "No antivirus software detected"}
                }
        
        else:
            return {"status": "unknown", "details": {"error": f"Unsupported OS: {system}"}}
            
    except Exception as e:
        return {"status": "error", "details": {"error": str(e)}}
