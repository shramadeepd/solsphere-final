#!/usr/bin/env python3
"""
Build script for SolSphere Utility
Creates distributable packages for different platforms
"""

import os
import sys
import shutil
import zipfile
import tarfile
from pathlib import Path
from datetime import datetime

def create_windows_package():
    """Create Windows executable package"""
    print("Creating Windows package...")
    
    # Create dist directory
    dist_dir = Path("dist/windows")
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy files
    files_to_copy = [
        "src/",
        "requirements.txt",
        "config.template",
        "install_service.py",
        "install_windows.bat",
        "README.md"
    ]
    
    for item in files_to_copy:
        src = Path(item)
        dst = dist_dir / item
        
        if src.is_file():
            shutil.copy2(src, dst)
        elif src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
    
    # Create zip file
    zip_name = f"solsphere-utility-windows-{datetime.now().strftime('%Y%m%d')}.zip"
    zip_path = Path("dist") / zip_name
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = Path(root) / file
                arc_name = file_path.relative_to(dist_dir)
                zipf.write(file_path, arc_name)
    
    print(f"Windows package created: {zip_path}")
    return zip_path

def create_linux_package():
    """Create Linux package"""
    print("Creating Linux package...")
    
    # Create dist directory
    dist_dir = Path("dist/linux")
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy files
    files_to_copy = [
        "src/",
        "requirements.txt",
        "config.template",
        "install_daemon.sh",
        "README.md"
    ]
    
    for item in files_to_copy:
        src = Path(item)
        dst = dist_dir / item
        
        if src.is_file():
            shutil.copy2(src, dst)
        elif src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
    
    # Make install script executable
    install_script = dist_dir / "install_daemon.sh"
    install_script.chmod(0o755)
    
    # Create tar.gz file
    tar_name = f"solsphere-utility-linux-{datetime.now().strftime('%Y%m%d')}.tar.gz"
    tar_path = Path("dist") / tar_name
    
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(dist_dir, arcname="solsphere-utility")
    
    print(f"Linux package created: {tar_path}")
    return tar_path

def create_macos_package():
    """Create macOS package"""
    print("Creating macOS package...")
    
    # Create dist directory
    dist_dir = Path("dist/macos")
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy files
    files_to_copy = [
        "src/",
        "requirements.txt",
        "config.template",
        "install_daemon.sh",
        "README.md"
    ]
    
    for item in files_to_copy:
        src = Path(item)
        dst = dist_dir / item
        
        if src.is_file():
            shutil.copy2(src, dst)
        elif src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
    
    # Make install script executable
    install_script = dist_dir / "install_daemon.sh"
    install_script.chmod(0o755)
    
    # Create tar.gz file
    tar_name = f"solsphere-utility-macos-{datetime.now().strftime('%Y%m%d')}.tar.gz"
    tar_path = Path("dist") / tar_name
    
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(dist_dir, arcname="solsphere-utility")
    
    print(f"macOS package created: {tar_path}")
    return tar_path

def create_source_package():
    """Create source distribution package"""
    print("Creating source package...")
    
    try:
        # Clean previous builds
        for path in ["build", "dist", "*.egg-info"]:
            if Path(path).exists():
                shutil.rmtree(path)
        
        # Build source distribution
        os.system(f"{sys.executable} setup.py sdist bdist_wheel")
        
        print("Source package created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating source package: {e}")
        return False

def main():
    """Main build function"""
    print("SolSphere Utility Package Builder")
    print("=" * 40)
    
    # Create dist directory
    Path("dist").mkdir(exist_ok=True)
    
    # Build packages
    packages = []
    
    if len(sys.argv) > 1:
        platform = sys.argv[1].lower()
        
        if platform == "windows":
            packages.append(create_windows_package())
        elif platform == "linux":
            packages.append(create_linux_package())
        elif platform == "macos":
            packages.append(create_macos_package())
        elif platform == "source":
            create_source_package()
        elif platform == "all":
            packages.extend([
                create_windows_package(),
                create_linux_package(),
                create_macos_package()
            ])
            create_source_package()
        else:
            print(f"Unknown platform: {platform}")
            print("Supported platforms: windows, linux, macos, source, all")
            return
    else:
        # Default: build all packages
        packages.extend([
            create_windows_package(),
            create_linux_package(),
            create_macos_package()
        ])
        create_source_package()
    
    print("\n" + "=" * 40)
    print("Build completed successfully!")
    
    if packages:
        print("\nCreated packages:")
        for package in packages:
            if package:
                print(f"  - {package.name}")
    
    print(f"\nAll packages saved to: {Path('dist').absolute()}")

if __name__ == "__main__":
    main() 