# SolSphere System Utility

A cross-platform system health monitoring utility that runs as a background daemon/service and sends system health data to the SolSphere backend API.

## Features

- 🔍 **System Health Monitoring**: Monitors CPU, memory, disk, network, and security
- 🚀 **Background Daemon**: Runs automatically as a system service
- 📡 **API Integration**: Sends data to SolSphere backend
- 🔄 **Auto-restart**: Automatically restarts on failure
- 📊 **State Tracking**: Tracks system changes and reports only when needed
- 🛡️ **Cross-platform**: Windows, Linux, and macOS support

## Quick Start

### Windows Installation

1. **Install as Windows Service** (Recommended):
   ```cmd
   python install_service.py
   ```

2. **Manual Installation**:
   ```cmd
   cd utility
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python src\main.py
   ```

### Linux/macOS Installation

1. **Install as System Service**:
   ```bash
   chmod +x install_daemon.sh
   ./install_daemon.sh
   ```

2. **Manual Installation**:
   ```bash
   cd utility
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python3 src/main.py
   ```

## Configuration

### Environment Variables

Create a `.env` file in the utility directory:

```env
# Backend API Configuration
BACKEND_URL=http://localhost:8001
API_KEY=your_api_key_here
CHECK_INTERVAL_MINUTES=5

# Logging
LOG_LEVEL=INFO
LOG_FILE=utility.log

# System Checks
ENABLE_CPU_CHECK=true
ENABLE_MEMORY_CHECK=true
ENABLE_DISK_CHECK=true
ENABLE_NETWORK_CHECK=true
ENABLE_SECURITY_CHECK=true
```

### API Configuration

The utility automatically sends data to the configured backend API. Make sure your backend is running and accessible.

## Service Management

### Windows

```cmd
# Check service status
sc query SolSphereUtility

# Start service
sc start SolSphereUtility

# Stop service
sc stop SolSphereUtility

# Uninstall service
python install_service.py uninstall
```

### Linux

```bash
# Check service status
sudo systemctl status solsphere-utility

# Start service
sudo systemctl start solsphere-utility

# Stop service
sudo systemctl stop solsphere-utility

# Enable auto-start
sudo systemctl enable solsphere-utility

# View logs
sudo journalctl -u solsphere-utility -f
```

### macOS

```bash
# Check daemon status
launchctl list | grep solsphere

# Unload daemon
launchctl unload ~/Library/LaunchAgents/com.solsphere.utility.plist

# View logs
tail -f /tmp/solsphere-utility.log
```

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, Ubuntu 18.04+, macOS 10.14+
- **Memory**: Minimum 128MB RAM
- **Disk Space**: 50MB free space

## Dependencies

Core dependencies are automatically installed:

- `requests`: HTTP client for API calls
- `psutil`: Cross-platform system monitoring
- `python-dotenv`: Environment variable management
- `pywin32`: Windows-specific utilities (Windows only)

## Development

### Project Structure

```
utility/
├── src/
│   ├── main.py              # Main entry point
│   ├── utils/               # Utility modules
│   ├── checks/              # System check modules
│   └── daemon/              # Daemon-specific code
├── tests/                   # Test files
├── requirements.txt          # Python dependencies
├── setup.py                 # Package setup
├── install_service.py       # Windows service installer
├── install_daemon.sh        # Linux/macOS daemon installer
└── README.md                # This file
```

### Running Tests

```bash
cd utility
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

pytest tests/
```

### Building Package

```bash
cd utility
python setup.py sdist bdist_wheel
```

## Troubleshooting

### Common Issues

1. **Service won't start**:
   - Check logs in Event Viewer (Windows) or journalctl (Linux)
   - Verify Python path and virtual environment
   - Check permissions

2. **API connection failed**:
   - Verify backend URL in configuration
   - Check network connectivity
   - Verify API key

3. **High CPU usage**:
   - Adjust check interval in configuration
   - Disable unnecessary system checks

### Log Files

- **Windows**: Event Viewer → Windows Logs → Application
- **Linux**: `sudo journalctl -u solsphere-utility`
- **macOS**: `/tmp/solsphere-utility.log`

### Getting Help

1. Check the logs for error messages
2. Verify your configuration
3. Test the backend API manually
4. Check system resources

## Security Considerations

- The utility runs with user-level permissions
- API keys are stored in environment variables
- No sensitive system data is collected
- All communications use HTTPS (when configured)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the troubleshooting section 