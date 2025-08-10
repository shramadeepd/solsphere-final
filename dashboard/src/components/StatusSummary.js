import React from 'react';
import { 
  Monitor, 
  CheckCircle, 
  XCircle, 
  HelpCircle,
  TrendingUp,
  Activity
} from 'lucide-react';

const StatusSummary = ({ totalMachines, statusCounts, osCounts }) => {
  const getStatusPercentage = (count) => {
    if (totalMachines === 0) return 0;
    return Math.round((count / totalMachines) * 100);
  };

  const getOSIcon = (osName) => {
    if (!osName) return <Monitor className="h-4 w-4" />;
    
    const os = osName.toLowerCase();
    if (os.includes('windows')) return <Monitor className="h-4 w-4 text-blue-500" />;
    if (os.includes('darwin') || os.includes('mac')) return <Monitor className="h-4 w-4 text-gray-500" />;
    if (os.includes('linux')) return <Monitor className="h-4 w-4 text-orange-500" />;
    
    return <Monitor className="h-4 w-4" />;
  };

  const statusCards = [
    {
      title: 'Total Machines',
      value: totalMachines,
      icon: Monitor,
      color: 'bg-blue-500',
      textColor: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Healthy',
      value: statusCounts.healthy || 0,
      icon: CheckCircle,
      color: 'bg-green-500',
      textColor: 'text-green-600',
      bgColor: 'bg-green-50',
      percentage: getStatusPercentage(statusCounts.healthy || 0)
    },
    {
      title: 'Unhealthy',
      value: statusCounts.unhealthy || 0,
      icon: XCircle,
      color: 'bg-red-500',
      textColor: 'text-red-600',
      bgColor: 'bg-red-50',
      percentage: getStatusPercentage(statusCounts.unhealthy || 0)
    },
    {
      title: 'Unknown',
      value: statusCounts.unknown || 0,
      icon: HelpCircle,
      color: 'bg-gray-500',
      textColor: 'text-gray-600',
      bgColor: 'bg-gray-50',
      percentage: getStatusPercentage(statusCounts.unknown || 0)
    }
  ];

  const topOS = Object.entries(osCounts || {})
    .sort(([,a], [,b]) => b - a)
    .slice(0, 3);

  return (
    <div className="space-y-6">
      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statusCards.map((card) => {
          const Icon = card.icon;
          return (
            <div key={card.title} className={`${card.bgColor} rounded-lg p-6 border border-gray-200`}>
              <div className="flex items-center">
                <div className={`${card.color} p-3 rounded-lg`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{card.title}</p>
                  <div className="flex items-baseline">
                    <p className="text-2xl font-semibold text-gray-900">{card.value}</p>
                    {card.percentage !== undefined && (
                      <span className={`ml-2 text-sm font-medium ${card.textColor}`}>
                        ({card.percentage}%)
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* OS Distribution */}
      {topOS.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
            <Activity className="h-5 w-5 mr-2 text-gray-500" />
            Operating System Distribution
          </h3>
          <div className="space-y-4">
            {topOS.map(([os, count]) => {
              const percentage = getStatusPercentage(count);
              return (
                <div key={os} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {getOSIcon(os)}
                    <span className="text-sm font-medium text-gray-900">{os}</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-24 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-600 w-12 text-right">
                      {count} ({percentage}%)
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Health Trend */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
          <TrendingUp className="h-5 w-5 mr-2 text-gray-500" />
          Health Overview
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
            <CheckCircle className="h-8 w-8 text-green-600 mx-auto mb-2" />
            <p className="text-sm font-medium text-green-800">Healthy Systems</p>
            <p className="text-2xl font-bold text-green-900">{statusCounts.healthy || 0}</p>
            <p className="text-xs text-green-600">
              {getStatusPercentage(statusCounts.healthy || 0)}% of total
            </p>
          </div>
          
          <div className="text-center p-4 bg-red-50 rounded-lg border border-red-200">
            <XCircle className="h-8 w-8 text-red-600 mx-auto mb-2" />
            <p className="text-sm font-medium text-red-800">Unhealthy Systems</p>
            <p className="text-2xl font-bold text-red-900">{statusCounts.unhealthy || 0}</p>
            <p className="text-xs text-red-600">
              {getStatusPercentage(statusCounts.unhealthy || 0)}% of total
            </p>
          </div>
          
          <div className="text-center p-4 bg-gray-50 rounded-lg border border-gray-200">
            <HelpCircle className="h-8 w-8 text-gray-600 mx-auto mb-2" />
            <p className="text-sm font-medium text-gray-800">Unknown Status</p>
            <p className="text-2xl font-bold text-gray-900">{statusCounts.unknown || 0}</p>
            <p className="text-xs text-gray-600">
              {getStatusPercentage(statusCounts.unknown || 0)}% of total
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatusSummary; 