import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Monitor, 
  Clock, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  HelpCircle,
  Activity,
  HardDrive,
  Cpu,
  Network,
  Calendar,
  RefreshCw
} from 'lucide-react';
import { fetchMachineById } from '../services/api';

const MachineDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [machine, setMachine] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadMachine();
  }, [id]);

  const loadMachine = async () => {
    try {
      setLoading(true);
      const data = await fetchMachineById(id);
      setMachine(data);
      setError(null);
    } catch (err) {
      setError('Failed to load machine details');
      console.error('Error loading machine:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-6 w-6 text-green-500" />;
      case 'unhealthy':
        return <XCircle className="h-6 w-6 text-red-500" />;
      default:
        return <HelpCircle className="h-6 w-6 text-gray-400" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-100 text-green-800';
      case 'unhealthy':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'Never';
    return new Date(timestamp).toLocaleString();
  };

  const formatLastSeen = (timestamp) => {
    if (!timestamp) return 'Never';
    
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minutes ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    if (diffDays < 7) return `${diffDays} days ago`;
    
    return date.toLocaleDateString();
  };

  const getOSIcon = (osName) => {
    if (!osName) return <Monitor className="h-5 w-5" />;
    
    const os = osName.toLowerCase();
    if (os.includes('windows')) return <Monitor className="h-5 w-5 text-blue-500" />;
    if (os.includes('darwin') || os.includes('mac')) return <Monitor className="h-5 w-5 text-gray-500" />;
    if (os.includes('linux')) return <Monitor className="h-5 w-5 text-orange-500" />;
    
    return <Monitor className="h-5 w-5" />;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !machine) {
    return (
      <div className="text-center py-12">
        <AlertTriangle className="mx-auto h-12 w-12 text-danger-500 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Machine</h3>
        <p className="text-gray-500 mb-4">{error || 'Machine not found'}</p>
        <div className="space-x-3">
          <button
            onClick={loadMachine}
            className="btn btn-primary"
          >
            Try Again
          </button>
          <button
            onClick={() => navigate('/')}
            className="btn btn-secondary"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const status = machine.metadata?.overall_status || 'unknown';

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link
            to="/"
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-100"
          >
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {machine.hostname || 'Unknown Hostname'}
            </h1>
            <p className="text-sm text-gray-500 font-mono">
              {machine.machine_id}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          <button
            onClick={loadMachine}
            className="btn btn-secondary"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </button>
          <div className="flex items-center space-x-2">
            {getStatusIcon(status)}
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(status)}`}>
              {status}
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Information */}
        <div className="lg:col-span-2 space-y-6">
          {/* Basic Info Card */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <Monitor className="h-5 w-5 mr-2 text-gray-500" />
              Basic Information
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-500 mb-1">Hostname</label>
                <p className="text-sm text-gray-900">{machine.hostname || 'Unknown'}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-500 mb-1">Machine ID</label>
                <p className="text-sm text-gray-900 font-mono">{machine.machine_id}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-500 mb-1">Operating System</label>
                <div className="flex items-center space-x-2">
                  {getOSIcon(machine.os_name)}
                  <span className="text-sm text-gray-900">
                    {machine.os_name || 'Unknown'} {machine.os_version || ''}
                  </span>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-500 mb-1">Last Check-in</label>
                <div className="flex items-center space-x-2">
                  <Clock className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-900">{formatLastSeen(machine.last_check_in)}</span>
                </div>
              </div>
            </div>
          </div>

          {/* System Metrics */}
          {machine.metadata && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <Activity className="h-5 w-5 mr-2 text-gray-500" />
                System Metrics
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {machine.metadata.cpu_usage !== undefined && (
                  <div className="text-center">
                    <div className="flex items-center justify-center mb-2">
                      <Cpu className="h-8 w-8 text-blue-500" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">{machine.metadata.cpu_usage}%</p>
                    <p className="text-sm text-gray-500">CPU Usage</p>
                  </div>
                )}
                
                {machine.metadata.memory_usage !== undefined && (
                  <div className="text-center">
                    <div className="flex items-center justify-center mb-2">
                      <HardDrive className="h-8 w-8 text-green-500" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">{machine.metadata.memory_usage}%</p>
                    <p className="text-sm text-gray-500">Memory Usage</p>
                  </div>
                )}
                
                {machine.metadata.disk_usage !== undefined && (
                  <div className="text-center">
                    <div className="flex items-center justify-center mb-2">
                      <HardDrive className="h-8 w-8 text-orange-500" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">{machine.metadata.disk_usage}%</p>
                    <p className="text-sm text-gray-500">Disk Usage</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Issues */}
          {machine.metadata?.issues && machine.metadata.issues.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2 text-red-500" />
                Issues Detected
              </h2>
              <div className="space-y-3">
                {machine.metadata.issues.map((issue, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-red-50 border border-red-200 rounded-md">
                    <AlertTriangle className="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-red-800">{issue}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Check-in History */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <Calendar className="h-5 w-5 mr-2 text-gray-500" />
              Check-in History
            </h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <div className="flex items-center space-x-3">
                  <Clock className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-900">Last Check-in</span>
                </div>
                <span className="text-sm text-gray-600">{formatTimestamp(machine.last_check_in)}</span>
              </div>
              {machine.created_at && (
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                  <div className="flex items-center space-x-3">
                    <Calendar className="h-4 w-4 text-gray-400" />
                    <span className="text-sm text-gray-900">First Seen</span>
                  </div>
                  <span className="text-sm text-gray-600">{formatTimestamp(machine.created_at)}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Status Summary */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Status Summary</h3>
            <div className="space-y-4">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-center mb-2">
                  {getStatusIcon(status)}
                </div>
                <p className="text-sm font-medium text-gray-600">Overall Status</p>
                <p className="text-xl font-bold text-gray-900 capitalize">{status}</p>
              </div>
              
              {machine.metadata?.overall_score !== undefined && (
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-900">{machine.metadata.overall_score}/100</div>
                  <p className="text-sm text-blue-600">Health Score</p>
                </div>
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button className="w-full btn btn-primary">
                <RefreshCw className="h-4 w-4 mr-2" />
                Force Check-in
              </button>
              <button className="w-full btn btn-secondary">
                <Activity className="h-4 w-4 mr-2" />
                View Logs
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MachineDetail; 