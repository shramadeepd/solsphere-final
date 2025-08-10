import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Monitor, 
  Clock, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  HelpCircle,
  ExternalLink
} from 'lucide-react';

const MachineCard = ({ machine }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'unhealthy':
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <HelpCircle className="h-5 w-5 text-gray-400" />;
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

  const formatLastSeen = (timestamp) => {
    if (!timestamp) return 'Never';
    
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString();
  };

  const getOSIcon = (osName) => {
    if (!osName) return <Monitor className="h-4 w-4" />;
    
    const os = osName.toLowerCase();
    if (os.includes('windows')) return <Monitor className="h-4 w-4 text-blue-500" />;
    if (os.includes('darwin') || os.includes('mac')) return <Monitor className="h-4 w-4 text-gray-500" />;
    if (os.includes('linux')) return <Monitor className="h-4 w-4 text-orange-500" />;
    
    return <Monitor className="h-4 w-4" />;
  };

  const status = machine.metadata?.overall_status || 'unknown';
  const lastSeen = machine.last_check_in;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            {getOSIcon(machine.os_name)}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 truncate">
                {machine.hostname || 'Unknown Hostname'}
              </h3>
              <p className="text-sm text-gray-500 font-mono">
                {machine.machine_id}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {getStatusIcon(status)}
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(status)}`}>
              {status}
            </span>
          </div>
        </div>

        {/* Machine Details */}
        <div className="space-y-3 mb-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">OS Version:</span>
            <span className="text-gray-900 font-medium">
              {machine.os_name || 'Unknown'} {machine.os_version || ''}
            </span>
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Last Seen:</span>
            <span className="text-gray-900 font-medium flex items-center">
              <Clock className="h-3 w-3 mr-1" />
              {formatLastSeen(lastSeen)}
            </span>
          </div>

          {machine.metadata?.cpu_usage && (
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">CPU Usage:</span>
              <span className="text-gray-900 font-medium">
                {machine.metadata.cpu_usage}%
              </span>
            </div>
          )}

          {machine.metadata?.memory_usage && (
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">Memory Usage:</span>
              <span className="text-gray-900 font-medium">
                {machine.metadata.memory_usage}%
              </span>
            </div>
          )}

          {machine.metadata?.disk_usage && (
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500">Disk Usage:</span>
              <span className="text-gray-900 font-medium">
                {machine.metadata.disk_usage}%
              </span>
            </div>
          )}
        </div>

        {/* Issues Summary */}
        {machine.metadata?.issues && machine.metadata.issues.length > 0 && (
          <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
            <div className="flex items-center space-x-2 mb-2">
              <AlertTriangle className="h-4 w-4 text-yellow-600" />
              <span className="text-sm font-medium text-yellow-800">
                {machine.metadata.issues.length} Issue{machine.metadata.issues.length !== 1 ? 's' : ''}
              </span>
            </div>
            <ul className="text-xs text-yellow-700 space-y-1">
              {machine.metadata.issues.slice(0, 2).map((issue, index) => (
                <li key={index} className="truncate">
                  • {issue}
                </li>
              ))}
              {machine.metadata.issues.length > 2 && (
                <li className="text-yellow-600">
                  +{machine.metadata.issues.length - 2} more...
                </li>
              )}
            </ul>
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-200">
          <Link
            to={`/machine/${machine.id}`}
            className="inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors"
          >
            View Details
            <ExternalLink className="h-3 w-3 ml-1" />
          </Link>
          
          <div className="text-xs text-gray-400">
            ID: {machine.id}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MachineCard; 