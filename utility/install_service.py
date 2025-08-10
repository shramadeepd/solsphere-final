#!/usr/bin/env python3
"""
Windows Service Installer for System Utility
Installs the utility as a Windows service that runs in the background
"""

import os
import sys
import winreg
import subprocess
from pathlib import Path

def install_windows_service():
    """Install the utility as a Windows service using NSSM"""
    try:
        # Check if NSSM is available
        nssm_path = find_nssm()
        if not nssm_path:
            print("NSSM not found. Installing NSSM...")
            install_nssm()
            nssm_path = find_nssm()
        
        # Get the current directory
        current_dir = Path(__file__).parent.absolute()
        python_exe = sys.executable
        script_path = current_dir / "src" / "main.py"
        
        # Service configuration
        service_name = "SolSphereUtility"
        service_display_name = "SolSphere System Utility"
        service_description = "System health monitoring utility for SolSphere"
        
        # Install the service
        print(f"Installing service: {service_name}")
        
        # Set the application path
        subprocess.run([
            nssm_path, "set", service_name, "Application", 
            python_exe, str(script_path)
        ], check=True)
        
        # Set the working directory
        subprocess.run([
            nssm_path, "set", service_name, "AppDirectory", 
            str(current_dir)
        ], check=True)
        
        # Set the display name
        subprocess.run([
            nssm_path, "set", service_name, "DisplayName", 
            service_display_name
        ], check=True)
        
        # Set the description
        subprocess.run([
            nssm_path, "set", service_name, "Description", 
            service_description
        ], check=True)
        
        # Set startup type to automatic
        subprocess.run([
            nssm_path, "set", service_name, "Start", "SERVICE_AUTO_START"
        ], check=True)
        
        # Set the service to restart on failure
        subprocess.run([
            nssm_path, "set", service_name, "AppRestartDelay", "10000"
        ], check=True)
        
        # Start the service
        print("Starting service...")
        subprocess.run([
            nssm_path, "start", service_name
        ], check=True)
        
        print(f"Service '{service_name}' installed and started successfully!")
        print(f"Service will run automatically on system startup.")
        print(f"To manage the service, use: nssm {service_name}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error installing service: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    return True

def find_nssm():
    """Find NSSM in common locations"""
    # Check if NSSM is in PATH
    try:
        result = subprocess.run(["nssm", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return "nssm"
    except FileNotFoundError:
        pass
    
    # Check common installation paths
    nssm_paths = [
        r"C:\Program Files\nssm\nssm.exe",
        r"C:\Program Files (x86)\nssm\nssm.exe",
        r"C:\nssm\nssm.exe"
    ]
    
    for path in nssm_paths:
        if os.path.exists(path):
            return path
    
    return None

def install_nssm():
    """Download and install NSSM"""
    import urllib.request
    import zipfile
    
    nssm_url = "https://nssm.cc/release/nssm-2.24.zip"
    nssm_dir = Path("C:/nssm")
    
    print("Downloading NSSM...")
    
    # Create directory
    nssm_dir.mkdir(exist_ok=True)
    
    # Download NSSM
    zip_path = nssm_dir / "nssm.zip"
    urllib.request.urlretrieve(nssm_url, zip_path)
    
    # Extract
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(nssm_dir)
    
    # Clean up
    zip_path.unlink()
    
    # Add to PATH
    add_to_path(str(nssm_dir))
    
    print("NSSM installed successfully!")

def add_to_path(path):
    """Add a path to the system PATH environment variable"""
    try:
        # Get current PATH
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 
                            0, winreg.KEY_READ | winreg.KEY_WRITE)
        
        current_path, _ = winreg.QueryValueEx(key, "Path")
        
        if path not in current_path:
            new_path = current_path + ";" + path
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        
        winreg.CloseKey(key)
        
    except Exception as e:
        print(f"Warning: Could not add to PATH automatically: {e}")
        print(f"Please add '{path}' to your system PATH manually")

def uninstall_service():
    """Uninstall the Windows service"""
    service_name = "SolSphereUtility"
    
    try:
        nssm_path = find_nssm()
        if nssm_path:
            # Stop the service first
            subprocess.run([nssm_path, "stop", service_name], 
                         capture_output=True)
            
            # Remove the service
            subprocess.run([nssm_path, "remove", service_name, "confirm"], 
                         check=True)
            
            print(f"Service '{service_name}' uninstalled successfully!")
        else:
            print("NSSM not found. Cannot uninstall service.")
            
    except subprocess.CalledProcessError as e:
        print(f"Error uninstalling service: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall_service()
    else:
        install_windows_service() 