# SolSphere Quick Start

## Running the Application

You have two options to start both the backend server and frontend simultaneously:

### Option 1: Windows Batch Script (Recommended for most users)
```bash
start_app.bat
```

### Option 2: PowerShell Script
```powershell
.\start_app.ps1
```

## What These Scripts Do

1. **Start the FastAPI Backend Server** on port 8001
   - Activates the Python virtual environment
   - Runs the server with auto-reload enabled
   - Accessible at: http://localhost:8001

2. **Start the React Frontend** on port 3000
   - Runs the development server
   - Accessible at: http://localhost:3000

## Manual Startup (if scripts don't work)

### Backend Server
```bash
cd server
.venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Frontend
```bash
cd dashboard
npm start
```

## Troubleshooting

- Make sure you have Python and Node.js installed
- Ensure virtual environments are set up in both `server/` and `dashboard/` directories
- Check that all dependencies are installed (`pip install -r requirements.txt` and `npm install`)
- If you get permission errors, try running PowerShell as Administrator

## Access Points

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs 