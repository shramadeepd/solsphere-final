import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Monitor, 
  Shield, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  Filter,
  Search,
  Download,
  RefreshCw
} from 'lucide-react';
import MachineCard from './MachineCard';
import StatusSummary from './StatusSummary';
import { fetchMachines, exportData } from '../services/api';

const Dashboard = () => {
  const [machines, setMachines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    os: '',
    status: '',
    search: ''
  });

  useEffect(() => {
    loadMachines();
  }, []);

  const loadMachines = async () => {
    try {
      setLoading(true);
      const data = await fetchMachines();
      setMachines(data);
      setError(null);
    } catch (err) {
      setError('Failed to load machines');
      console.error('Error loading machines:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      await exportData();
    } catch (err) {
      console.error('Export failed:', err);
    }
  };

  const filteredMachines = machines.filter(machine => {
    if (filters.os && machine.os_name !== filters.os) return false;
    if (filters.status && machine.metadata?.overall_status !== filters.status) return false;
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      return (
        machine.hostname?.toLowerCase().includes(searchLower) ||
        machine.machine_id.toLowerCase().includes(searchLower) ||
        machine.os_name?.toLowerCase().includes(searchLower)
      );
    }
    return true;
  });

  const getStatusCounts = () => {
    const counts = { healthy: 0, unhealthy: 0, unknown: 0 };
    machines.forEach(machine => {
      const status = machine.metadata?.overall_status || 'unknown';
      counts[status]++;
    });
    return counts;
  };

  const getOSCounts = () => {
    const counts = {};
    machines.forEach(machine => {
      const os = machine.os_name || 'Unknown';
      counts[os] = (counts[os] || 0) + 1;
    });
    return counts;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <AlertTriangle className="mx-auto h-12 w-12 text-danger-500 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Dashboard</h3>
        <p className="text-gray-500 mb-4">{error}</p>
        <button
          onClick={loadMachines}
          className="btn btn-primary"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">System Health Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Monitor the health and compliance of all systems in your infrastructure
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button
            onClick={loadMachines}
            className="btn btn-secondary"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </button>
          <button
            onClick={handleExport}
            className="btn btn-primary"
          >
            <Download className="h-4 w-4 mr-2" />
            Export
          </button>
        </div>
      </div>

      {/* Status Summary */}
      <StatusSummary 
        totalMachines={machines.length}
        statusCounts={getStatusCounts()}
        osCounts={getOSCounts()}
      />

      {/* Filters */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                id="search"
                placeholder="Search by hostname, machine ID, or OS..."
                className="input pl-10"
                value={filters.search}
                onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
              />
            </div>
          </div>
          
          <div>
            <label htmlFor="os-filter" className="block text-sm font-medium text-gray-700 mb-1">
              Operating System
            </label>
            <select
              id="os-filter"
              className="input"
              value={filters.os}
              onChange={(e) => setFilters(prev => ({ ...prev, os: e.target.value }))}
            >
              <option value="">All OS</option>
              <option value="Windows">Windows</option>
              <option value="Darwin">macOS</option>
              <option value="Linux">Linux</option>
            </select>
          </div>
          
          <div>
            <label htmlFor="status-filter" className="block text-sm font-medium text-gray-700 mb-1">
              Health Status
            </label>
            <select
              id="status-filter"
              className="input"
              value={filters.status}
              onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
            >
              <option value="">All Statuses</option>
              <option value="healthy">Healthy</option>
              <option value="unhealthy">Unhealthy</option>
              <option value="unknown">Unknown</option>
            </select>
          </div>
        </div>
      </div>

      {/* Machines Grid */}
      {filteredMachines.length === 0 ? (
        <div className="text-center py-12">
          <Monitor className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No machines found</h3>
          <p className="text-gray-500">
            {filters.search || filters.os || filters.status 
              ? 'Try adjusting your filters or search terms.'
              : 'No machines have reported their status yet.'
            }
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredMachines.map((machine) => (
            <MachineCard key={machine.id} machine={machine} />
          ))}
        </div>
      )}

      {/* Pagination or Load More */}
      {filteredMachines.length > 0 && (
        <div className="text-center">
          <p className="text-sm text-gray-500">
            Showing {filteredMachines.length} of {machines.length} machines
          </p>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 