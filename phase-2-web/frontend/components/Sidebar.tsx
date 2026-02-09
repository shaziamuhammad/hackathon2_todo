/**
 * Sidebar Component
 * Filter and sort options for tasks
 */
'use client';

import React, { useState } from 'react';

interface FilterOptions {
  priority: string[];
  status: string[];
  tags: string[];
  dueDateRange: string;
  sortBy: string;
  sortOrder: 'asc' | 'desc';
}

interface SidebarProps {
  onFilterChange?: (filters: FilterOptions) => void;
  isOpen?: boolean;
  onClose?: () => void;
}

export default function Sidebar({ onFilterChange, isOpen = true, onClose }: SidebarProps) {
  const [filters, setFilters] = useState<FilterOptions>({
    priority: [],
    status: [],
    tags: [],
    dueDateRange: 'all',
    sortBy: 'created_at',
    sortOrder: 'desc'
  });

  const handleFilterChange = (key: keyof FilterOptions, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange?.(newFilters);
  };

  const toggleArrayFilter = (key: 'priority' | 'status' | 'tags', value: string) => {
    const currentArray = filters[key];
    const newArray = currentArray.includes(value)
      ? currentArray.filter(item => item !== value)
      : [...currentArray, value];
    handleFilterChange(key, newArray);
  };

  const clearFilters = () => {
    const defaultFilters: FilterOptions = {
      priority: [],
      status: [],
      tags: [],
      dueDateRange: 'all',
      sortBy: 'created_at',
      sortOrder: 'desc'
    };
    setFilters(defaultFilters);
    onFilterChange?.(defaultFilters);
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed md:static inset-y-0 left-0 z-50
          w-64 bg-white border-r border-gray-200
          transform transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
          overflow-y-auto
        `}
      >
        <div className="p-4">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
            <button
              onClick={clearFilters}
              className="text-sm text-purple-600 hover:text-purple-700"
            >
              Clear All
            </button>
          </div>

          {/* Priority Filter */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Priority</h3>
            <div className="space-y-2">
              {['urgent', 'high', 'medium', 'low'].map(priority => (
                <label key={priority} className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.priority.includes(priority)}
                    onChange={() => toggleArrayFilter('priority', priority)}
                    className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                  />
                  <span className="ml-2 text-sm text-gray-700 capitalize">
                    {priority}
                  </span>
                  <span className={`ml-auto px-2 py-0.5 text-xs rounded ${
                    priority === 'urgent' ? 'bg-red-100 text-red-800' :
                    priority === 'high' ? 'bg-orange-100 text-orange-800' :
                    priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {priority === 'urgent' ? '🔥' : priority === 'high' ? '⚠️' : priority === 'medium' ? '📌' : '📋'}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Status Filter */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Status</h3>
            <div className="space-y-2">
              {['pending', 'in-progress', 'complete'].map(status => (
                <label key={status} className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.status.includes(status)}
                    onChange={() => toggleArrayFilter('status', status)}
                    className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                  />
                  <span className="ml-2 text-sm text-gray-700 capitalize">
                    {status.replace('-', ' ')}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Due Date Filter */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Due Date</h3>
            <select
              value={filters.dueDateRange}
              onChange={(e) => handleFilterChange('dueDateRange', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="all">All Tasks</option>
              <option value="overdue">Overdue</option>
              <option value="today">Due Today</option>
              <option value="tomorrow">Due Tomorrow</option>
              <option value="this-week">This Week</option>
              <option value="next-week">Next Week</option>
              <option value="this-month">This Month</option>
              <option value="no-due-date">No Due Date</option>
            </select>
          </div>

          {/* Sort Options */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Sort By</h3>
            <select
              value={filters.sortBy}
              onChange={(e) => handleFilterChange('sortBy', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 mb-2"
            >
              <option value="created_at">Date Created</option>
              <option value="updated_at">Last Updated</option>
              <option value="due_date">Due Date</option>
              <option value="priority">Priority</option>
              <option value="title">Title (A-Z)</option>
            </select>

            <div className="flex space-x-2">
              <button
                onClick={() => handleFilterChange('sortOrder', 'asc')}
                className={`flex-1 px-3 py-2 text-sm rounded-md transition-colors ${
                  filters.sortOrder === 'asc'
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                ↑ Ascending
              </button>
              <button
                onClick={() => handleFilterChange('sortOrder', 'desc')}
                className={`flex-1 px-3 py-2 text-sm rounded-md transition-colors ${
                  filters.sortOrder === 'desc'
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                ↓ Descending
              </button>
            </div>
          </div>

          {/* Active Filters Summary */}
          {(filters.priority.length > 0 || filters.status.length > 0 || filters.dueDateRange !== 'all') && (
            <div className="mt-6 p-3 bg-purple-50 rounded-md">
              <h4 className="text-xs font-medium text-purple-900 mb-2">Active Filters</h4>
              <div className="flex flex-wrap gap-1">
                {filters.priority.map(p => (
                  <span key={p} className="px-2 py-1 text-xs bg-purple-200 text-purple-800 rounded">
                    {p}
                  </span>
                ))}
                {filters.status.map(s => (
                  <span key={s} className="px-2 py-1 text-xs bg-purple-200 text-purple-800 rounded">
                    {s}
                  </span>
                ))}
                {filters.dueDateRange !== 'all' && (
                  <span className="px-2 py-1 text-xs bg-purple-200 text-purple-800 rounded">
                    {filters.dueDateRange}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
