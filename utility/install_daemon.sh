#!/bin/bash
"""
Linux/Mac Daemon Installer for System Utility
Installs the utility as a systemd service (Linux) or launchd daemon (macOS)
"""

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UTILITY_NAME="solsphere-utility"
SERVICE_NAME="solsphere-utility"

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

install_linux_service() {
    print_status "Installing Linux systemd service..."
    
    # Create systemd service file
    SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
    
    sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=SolSphere System Utility
After=network.target
Wants=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$SCRIPT_DIR
ExecStart=$SCRIPT_DIR/.venv/bin/python $SCRIPT_DIR/src/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment=PYTHONPATH=$SCRIPT_DIR/src

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd and enable service
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    sudo systemctl start "$SERVICE_NAME"
    
    print_status "Service installed and started successfully!"
    print_status "To check status: sudo systemctl status $SERVICE_NAME"
    print_status "To stop: sudo systemctl stop $SERVICE_NAME"
    print_status "To restart: sudo systemctl restart $SERVICE_NAME"
}

install_macos_daemon() {
    print_status "Installing macOS launchd daemon..."
    
    # Create launchd plist file
    PLIST_FILE="$HOME/Library/LaunchAgents/com.solsphere.utility.plist"
    
    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.solsphere.utility</string>
    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/.venv/bin/python</string>
        <string>$SCRIPT_DIR/src/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/solsphere-utility.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/solsphere-utility-error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONPATH</key>
        <string>$SCRIPT_DIR/src</string>
    </dict>
</dict>
</plist>
EOF

    # Load the daemon
    launchctl load "$PLIST_FILE"
    
    print_status "Daemon installed and loaded successfully!"
    print_status "To unload: launchctl unload $PLIST_FILE"
    print_status "To check status: launchctl list | grep solsphere"
}

uninstall_service() {
    local os=$(detect_os)
    
    if [[ "$os" == "linux" ]]; then
        print_status "Uninstalling Linux systemd service..."
        sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true
        sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || true
        sudo rm -f "/etc/systemd/system/${SERVICE_NAME}.service"
        sudo systemctl daemon-reload
        print_status "Service uninstalled successfully!"
        
    elif [[ "$os" == "macos" ]]; then
        print_status "Uninstalling macOS launchd daemon..."
        PLIST_FILE="$HOME/Library/LaunchAgents/com.solsphere.utility.plist"
        launchctl unload "$PLIST_FILE" 2>/dev/null || true
        rm -f "$PLIST_FILE"
        print_status "Daemon uninstalled successfully!"
        
    else
        print_error "Unsupported operating system"
        exit 1
    fi
}

setup_virtual_environment() {
    print_status "Setting up Python virtual environment..."
    
    if [[ ! -d "$SCRIPT_DIR/.venv" ]]; then
        python3 -m venv "$SCRIPT_DIR/.venv"
        print_status "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate and install dependencies
    source "$SCRIPT_DIR/.venv/bin/activate"
    pip install -r "$SCRIPT_DIR/requirements.txt"
    print_status "Dependencies installed"
}

main() {
    print_status "SolSphere Utility Daemon Installer"
    print_status "Detected OS: $(detect_os)"
    
    if [[ "$1" == "uninstall" ]]; then
        uninstall_service
        exit 0
    fi
    
    # Check if running as root (not recommended for user services)
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root is not recommended for user services"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Setup virtual environment
    setup_virtual_environment
    
    # Install service based on OS
    local os=$(detect_os)
    
    if [[ "$os" == "linux" ]]; then
        install_linux_service
    elif [[ "$os" == "macos" ]]; then
        install_macos_daemon
    else
        print_error "Unsupported operating system: $os"
        exit 1
    fi
    
    print_status "Installation completed successfully!"
    print_status "The utility will now run automatically in the background"
}

# Run main function
main "$@" 